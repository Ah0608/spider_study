// ==UserScript==
// @name         proquest_journal_pure_websocket_rpc
// @namespace    your-namespace
// @version      1.0
// @description  拦截指定URL并进行处理
// @match        https://www.proquest.com/*
// @exclude      https://www.proquest.com/saveasdownloadprogress/*
// @run-at       document-end
// ==/UserScript==

(function () {
    'use strict';

    function JsClient(wsURL) {
        this.wsURL = wsURL;
        this.handlers = {};
        this.socket = {};
        if (!wsURL) {
            throw new Error('wsURL can not be empty!!')
        }
        this.webSocketFactory = this.resolveWebSocketFactory();
        this.connect()
    }

    JsClient.prototype.resolveWebSocketFactory = function () {
        if (typeof window === 'object') {
            var theWebSocket = window.WebSocket ? window.WebSocket : window.MozWebSocket;
            return function (wsURL) {

                function WindowWebSocketWrapper(wsURL) {
                    this.mSocket = new theWebSocket(wsURL);
                }

                WindowWebSocketWrapper.prototype.close = function () {
                    this.mSocket.close();
                };

                WindowWebSocketWrapper.prototype.onmessage = function (onMessageFunction) {
                    this.mSocket.onmessage = onMessageFunction;
                };

                WindowWebSocketWrapper.prototype.onopen = function (onOpenFunction) {
                    this.mSocket.onopen = onOpenFunction;
                };
                WindowWebSocketWrapper.prototype.onclose = function (onCloseFunction) {
                    this.mSocket.onclose = onCloseFunction;
                };

                WindowWebSocketWrapper.prototype.send = function (message) {
                    this.mSocket.send(message);
                };

                return new WindowWebSocketWrapper(wsURL);
            }
        }
        if (typeof weex === 'object') {
            try {
                console.log("test webSocket for weex");
                var ws = weex.requireModule('webSocket');
                console.log("find webSocket for weex:" + ws);
                return function (wsURL) {
                    try {
                        ws.close();
                    } catch (e) {
                    }
                    ws.WebSocket(wsURL, '');
                    return ws;
                }
            } catch (e) {
                console.log(e);
            }
        }
        if (typeof WebSocket === 'object') {
            return function (wsURL) {
                return new theWebSocket(wsURL);
            }
        }
        throw new Error("the js environment do not support websocket");
    };

    JsClient.prototype.connect = function () {
        console.log('jsclient begin of connect to wsURL: ' + this.wsURL);
        var _this = this;
        try {
            this.socket = this.webSocketFactory(this.wsURL);
        } catch (e) {
            console.log("jsclient create connection failed,reconnect after 2s");
            setTimeout(function () {
                _this.connect()
            }, 2000)
        }

        this.socket.onmessage(function (event) {
            _this.handleJsClientRequest(event.data)
        });

        this.socket.onopen(function (event) {
            console.log('jsclient open a connection')
        });

        this.socket.onclose(function (event) {
            console.log('jsclient disconnected ,reconnection after 2s');
            setTimeout(function () {
                _this.connect()
            }, 2000)
        });
    };

    JsClient.prototype.handleJsClientRequest = function (requestJson) {
        console.log("receive request: " + requestJson);
        var request = JSON.parse(requestJson);
        var seq = request['__uuid_seq__'];

        if (!request['action']) {
            this.sendFailed(seq, 'need request param {action}');
            return
        }
        var action = request['action'];
        if (!this.handlers[action]) {
            this.sendFailed(seq, 'no action handler: ' + action + ' defined');
            return
        }

        var theHandler = this.handlers[action];
        var _this = this;
        try {
            theHandler(request, function (response) {
                try {
                    _this.sendSuccess(seq, response)
                } catch (e) {
                    _this.sendFailed(seq, "e:" + e);
                }
            }, function (errorMessage) {
                _this.sendFailed(seq, errorMessage)
            })
        } catch (e) {
            console.log("error: " + e);
            _this.sendFailed(seq, ":" + e);
        }
    };

    function prependStringToBlob(blob, str) {
        return new Blob([str, blob], {type: blob.type});
    }

    JsClient.prototype.sendSuccess = function (seq, response) {
        var responseJson = {}
        if (response instanceof Blob) {
            var newBlob = prependStringToBlob(response, seq + '=-=+=');
            console.log("response :", newBlob);
            this.socket.send(newBlob);
        } else {
            responseJson.data = response;
            responseJson.status = 1;
            responseJson.__uuid_seq__ = seq;
            var responseText = JSON.stringify(responseJson);
            console.log("response :" + responseText);
            this.socket.send(responseText);
        }
    };

    JsClient.prototype.sendFailed = function (seq, errorMessage) {
        if (typeof errorMessage != 'string') {
            errorMessage = JSON.stringify(errorMessage);
        }
        var responseJson = {};
        responseJson.data = errorMessage;
        responseJson.status = -1;
        responseJson.__uuid_seq__ = seq;
        var responseText = JSON.stringify(responseJson);
        console.log("jsclient response :" + responseText);
        this.socket.send(responseText)
    };

    JsClient.prototype.registerAction = function (action, handler) {
        if (typeof action !== 'string') {
            throw new Error("an action must be string");
        }
        if (typeof handler !== 'function') {
            throw new Error("a handler must be function");
        }
        console.log("jsclient register action: " + action);
        this.handlers[action] = handler;
        return this;
    };

    function requestGet(request, resolve, reject) {
        let articleURl = request.url;
        fetch(articleURl, {
            "credentials": "include",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "method": "GET"
        }).then(response => {
            if (response.redirected) {
                console.log('重定向到:', response.url);
            }
            return response;
        }).then(res => {
            if (res.ok) {
                return res.blob()
            } else {
                reject('请求失败, 状态码--' + res.status)
            }
        }).then(blob => {
            resolve(blob);
        }).catch(error => {
            console.error('无法下载文件:', error);
            resolve('请求失败...' + error)
        });
    }
    function browserGetPdf(request, resolve, reject) {
        let articleURl = request.url;
        console.log('pdfUrl: ' + articleURl)
        // 定义新窗口的位置和大小
        var windowFeatures = 'width=1,height=1,left=-1000,top=-1000';
        window.esNewTab = window.open(articleURl, '_blank', windowFeatures);

        resolve('开始下载')
    }
    //demo
    var client = new JsClient("ws://localhost:5378/register?group=test&clientId=" + Math.random());
    client.registerAction("closeNewTab", function (request, resolve, reject) {
        window.esNewTab.close();
        resolve('newTab已关闭');
    });
    client.registerAction("browserGetPdf", function (request, resolve, reject) {
        browserGetPdf(request, resolve, reject)
    });
    client.registerAction("requestGet", function (request, resolve, reject) {
        requestGet(request, resolve, reject)
    });
    client.registerAction("reload", function (request, resolve, reject) {
        location.reload();
    });
    client.registerAction("getCookie", function (request, resolve, reject) {
        resolve(document.cookie);
    });
    client.registerAction("getState", function (request, resolve, reject) {
        if (window.success === 1) {
            resolve('刷新成功');
        } else {
            resolve('刷新ing');
        }
    });
    window.onload = function () {
        console.log('所有请求已完成');
        window.success = 1
    };
})();