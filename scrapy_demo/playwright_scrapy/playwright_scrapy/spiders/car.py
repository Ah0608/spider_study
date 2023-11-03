import scrapy


class CarSpider(scrapy.Spider):
    name = "car"

    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            # "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        # "CONCURRENT_REQUESTS": 32,
        # "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 4,
        # "CLOSESPIDER_ITEMCOUNT": 100,
        # "FEEDS": {
        #     "books.json": {"format": "json", "encoding": "utf-8", "indent": 4},
        # },
    }

    def start_requests(self):

        # GET request
        yield scrapy.Request("https://www.dongchedi.com/auto/library/x-x-x-x-x-x-4-x-x-x-x", meta={"playwright": True})
        # POST request
        # yield scrapy.FormRequest(
        #     url="https://httpbin.org/post",
        #     formdata={"foo": "bar"},
        #     meta={"playwright": True},
        # )

    def parse(self, response):
        # 'response' contains the page as seen by the browser
        print(response.url)