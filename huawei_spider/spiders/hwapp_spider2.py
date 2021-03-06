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
    
    -- click category
    local categories = {}
    ci = splash.args.categ_index
    if  ci == 1 then
        splash:select('[class="childtab textClicked"]'):mouse_click()
    else 
        categories = splash:select_all('[class="childtab text"]')
        categories[ci - 1]:mouse_click()
    end
    splash:wait(splash.args.wait)
    
    -- scroll page
    for i = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end 
    
    -- click app
    ai = splash.args.app_index
    apps = splash:select_all('[class="item"]')
    apps[ai]:mouse_click()
    splash:wait(splash.args.wait)
    
    return splash:html()    
end
'''


class AppGallerySpider(scrapy.Spider):
    name = 'hwapp_spider2'
    allowed_domains = ["huawei.com"]
    start_url = 'https://appgallery.huawei.com/#/Apps/'
    max_categ = 16
    max_app = 200
    categ_i = 1
    app_i = 1

    def start_requests(self):
        yield SplashRequest(self.start_url,
                            endpoint='execute',
                            args={'wait': 1, 'categ_index': self.categ_i, 'app_index': self.app_i, 'lua_source': lua_script},
                            cache_args=['lua_source'],
                            callback=self.parse)

    def parse(self, response):
        # print(self.categ_i, response.css('[class="childtab textClicked"]::text').get())
        item = HuaweiSpiderItem()
        selector = response.xpath('//div[@class="box"]')
        item["id"] = selector.xpath('//div[@class="componentContainer"]/div[2]/@appid').get()
        item["name"] = selector.xpath('.//div[@class="center_info"]/div[@class="title"]/text()').get()
        item["detail"] = selector.xpath('.//div[@class="detaileditorrecommendcard"]/div[@class="title"]/text()').get()
        item["img"] = selector.xpath('.//img[@class="left_logo"]/@src').get()
        item["intro"] = selector.xpath('.//div[@class="detailappintrocard"]//div[@class="left"]/text()').get()
        base_url = 'https://appgallery.huawei.com/#/app/'
        id = item["id"]
        if id:
            item["url"] = base_url + id

        yield item
        # print(item["name"], item["img"], item["detail"], item["intro"], item["url"])

        if self.app_i == self.max_app:
            self.app_i = 0
            self.categ_i = self.categ_i + 1
            if self.categ_i == self.max_categ:
                return

        self.app_i = self.app_i + 1
        yield SplashRequest(self.start_url,
                            endpoint='execute',
                            args={'wait': 1, 'categ_index': self.categ_i, 'app_index': self.app_i, 'lua_source': lua_script},
                            cache_args=['lua_source'],
                            callback=self.parse)
