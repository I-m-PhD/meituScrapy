import scrapy
import re
from meitu_rank.items import MeituRankItem


class RankSpider(scrapy.Spider):
    name = 'rank'
    allowed_domains = []
    start_urls = ['https://www.meitu131.com/rank/nvshen/']
    # https://www.meitu131.com/rank/nvshen/
    # https://www.meitu131.com/nvshen/574/`
    # https://www.meitu131.com/meinv/8221/

    def parse(self, response, **kwargs):
        ml = response.xpath('/html/body/div[1]/div[2]/div/ul/li')
        #                    /html/body/div[1]/div[2]/div/ul/li/div[1]/span[1]
        #                    /html/body/div[1]/div[2]/div/ul/li/div[3]/div[1]/a
        for i in ml:
            mr = i.xpath('div[1]/span[1]/text()').extract_first()
            mn = mr + '-' + i.xpath('div[3]/div[1]/a/text()').extract_first()
            mu = i.xpath('div[3]/div[1]/a/@href').extract_first()
            yield scrapy.Request(
                url=response.urljoin(mu),
                callback=self.parse_album,
                meta={
                    'model_name': mn,  # here 'model_name' must be the same as defined in items.py
                },
            )

    def parse_album(self, response):
        al = response.xpath('/html/body/div[3]/div[2]/ul/li/div[2]/a')
        for i in al:
            at = re.sub(
                pattern='([^\u4e00-\u9fff\u0041-\u005a\u0061-\u007a])',
                repl='',
                string=i.xpath('text()').extract_first()
            )
            au = i.xpath('@href').extract_first()
            yield scrapy.Request(
                url=response.urljoin(au),
                callback=self.parse_photo,
                meta={
                    'model_name': response.meta['model_name'],
                    'album_title': at,  # here 'album_title' must be the same as defined in items.py
                },
            )

    def parse_photo(self, response):
        i = MeituRankItem()
        i['model_name'] = response.meta['model_name']
        i['album_title'] = response.meta['album_title']
        i['image_urls'] = response.xpath('/html/body/div[1]/div[2]/p/a/img/@src').extract_first()
        yield i

        np = response.xpath('/html/body/div[1]/div[3]/a[text()="下一页"]/@href').extract_first()
        if np:
            yield scrapy.Request(
                url=response.urljoin(np),
                callback=self.parse_photo,
                meta={
                    'model_name': i['model_name'],
                    'album_title': i['album_title'],
                },
            )
        else:
            print('===============================\n=======Done and move on!=======\n===============================')
