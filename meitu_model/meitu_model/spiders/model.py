import scrapy

import re
from meitu_model.items import MeituModelItem


class ModelSpider(scrapy.Spider):
    name = 'model'
    allowed_domains = []
    start_urls = ['https://www.meitu131.com/nvshen/']

    def parse(self, response, **kwargs):
        # print('/'*8, response.url, '/'*8, 'LIST sent')
        yield response.follow(
            url=response.url,
            callback=self.parse_model,
            dont_filter=True
        )
        npu = response.xpath('/html/body/div[3]/a[text()="下一页"]/@href').extract_first()
        if npu:
            yield response.follow(
                url=npu,
                callback=self.parse,
                dont_filter=True
            )

    def parse_model(self, response):
        # print('>'*8, response.url, '>'*8, 'LIST received')
        ml = response.xpath('/html/body/div[1]/div[2]/ul/li/div[2]')
        # x = 0
        for i in ml:
            # x += 1
            mu = i.xpath('p[1]/a/@href').extract_first()
            mo = i.xpath('p[2]/a/text()').extract_first()
            mn = i.xpath('p[1]/a/text()').extract_first()
            # print(x, mo, mn, mu)
            yield response.follow(
                url=mu,
                callback=self.parse_album,
                dont_filter=True,
                meta={'mo': mo, 'mn': mn}
            )

    def parse_album(self, response):
        mo = response.meta['mo']
        mn = response.meta['mn']
        al = response.xpath('/html/body/div[3]/div[2]/ul/li/div[2]/a')
        # x = 0
        for i in al:
            # x += 1
            au = i.xpath('@href').extract_first()
            ahr = i.xpath('text()').extract_first()
            ah = re.sub(pattern='([^0-9\u4e00-\u9fff\u0041-\u005a\u0061-\u007a])', repl='', string=ahr)
            # print('(', x, ')', mo, mn, ah)
            yield response.follow(
                url=au,
                callback=self.parse_img,
                dont_filter=True,
                meta={'model_origin': mo, 'model_name': mn, 'album_head': ah}
            )

    def parse_img(self, response):
        mo = response.meta['model_origin']
        mn = response.meta['model_name']
        ah = response.meta['album_head']
        iu = response.xpath('//*[@id="main-wrapper"]/div[2]/p/a/img/@src').extract_first()
        t = MeituModelItem()
        t['model_origin'] = mo
        t['model_name'] = mn
        t['album_head'] = ah
        t['img_url'] = iu
        yield t
        print(t)
        npu = response.xpath('//*[@id="pages"]/a[text()="下一页"]/@href').extract_first()
        if npu:
            yield response.follow(
                url=npu,
                callback=self.parse_img,
                dont_filter=True,
                meta={'model_origin': mo, 'model_name': mn, 'album_head': ah}
            )
