from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider
import scrapy

from huawei_spider.items import HuaweiSpiderItem
from scrapy_splash import SplashRequest

lua_script = '''
function main(splash, args)
    local num_scrolls = 20
    local scroll_delay = 1

    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)

    for i = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end        
    return splash:html()
end
'''

class AppGallerySpider(scrapy.Spider):
    name = 'hwtop_spider'
    allowed_domains = ["huawei.com"]
    start_urls = ['https://appgallery.huawei.com/#/Top/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                endpoint='execute',
                                args={'wait': 2, 'lua_source': lua_script},
                                cache_args=['lua_source'],
                                callback=self.parse)

    def parse(self, response):
        i = 1;
        selectors = response.xpath('//div[contains(@class,"tem tem-l")]')
        tselects = selectors.xpath('.//div[@class="intro_left"]')
        for tselect in tselects:
            app_name = tselect.xpath('./p[1]/text()').get()
            app_label = tselect.xpath('./span/span/text()').get()
            app_detail = tselect.xpath('./p[2]/text()').get()
            i = i+1
            print(i,app_name,app_label,app_detail)