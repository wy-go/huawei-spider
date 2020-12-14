from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider
import scrapy

from huawei_spider.items import HuaweiSpiderItem
from scrapy_splash import SplashRequest

lua_script = '''
function main(splash, args)
    local num_scrolls = 10
    local scroll_delay = 0.5

    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )

    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)
    
    local categories = {}
    index = splash.args.index
    if  index == 1 then
        splash:select('[class="childtab textClicked"]'):mouse_click()
    else 
        categories = splash:select_all('[class="childtab text"]')
        categories[index - 1]:mouse_click()
    end
    
    for i = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end 

    return splash:html()    
end
'''


class AppGallerySpider(scrapy.Spider):
    name = 'hwapp_spider'
    allowed_domains = ["huawei.com"]
    start_url = 'https://appgallery.huawei.com/#/Apps/'
    max_categ = 16
    categ_i = 1

    def start_requests(self):
        yield SplashRequest(self.start_url,
                            endpoint='execute',
                            args={'wait': 1, 'index': self.categ_i, 'lua_source': lua_script},
                            cache_args=['lua_source'],
                            callback=self.parse)

    def parse(self, response):
        print(self.categ_i, response.css('[class="childtab textClicked"]::text').get())

        # selectors = response.xpath('//div[@class="item"]')
        # tselectors = selectors.xpath('.//div[@class="labelbox"]')
        # num = 0
        # for tselector in tselectors:
        #     app_name = tselector.xpath('.//span[@class="name"]/text()').get()
        #     app_label = tselector.xpath('.//span[@class="mwText"]/text()').get()
        #     app_detail = tselector.xpath('.//span[@class="detail"]/text()').get()
        #     num = num + 1
        #     print(num, app_name, app_label, app_detail)

        if self.categ_i == self.max_categ:
            return
        self.categ_i = self.categ_i + 1
        yield SplashRequest(self.start_url,
                            endpoint='execute',
                            args={'wait': 1, 'index': self.categ_i, 'lua_source': lua_script},
                            cache_args=['lua_source'],
                            callback=self.parse)
