import scrapy
import pathlib
import pandas as pd
from meitu_rank_diy.items import MeituRankDiyItem


class Step5Spider(scrapy.Spider):
    name = 'step5'
    allowed_domains = []
    start_urls = ['https://www.meitu131.com/']

    def parse(self, response, **kwargs):
        if pathlib.Path('model_sorted.csv').exists():
            d = pd.read_csv('model_sorted.csv', encoding='utf-8')

            """
            How many models you want to collect?
            Change the x value below as you wish.
            """

            x = 2
            for i in range(0, x):
                mn = d.iloc[i]['M.NAME']
                ms = d.iloc[i]['M.SCORE']
                mu = d.iloc[i]['M.URL']
                yield response.follow(url=mu,
                                      callback=self.parse_al,
                                      meta={'mn': mn,
                                            'ms': ms, })
    def parse_al(self, response):
        mn = response.meta['mn']
        ms = response.meta['ms']
        al = response.xpath('/html/body/div[3]/div[2]/ul/li/div[2]/a')
        if al:
            for i in al:
                au = i.xpath('@href').extract_first()
                ah = i.xpath('text()').extract_first()
                yield response.follow(url=au,
                                      callback=self.parse_img,
                                      meta={'model_name': mn,
                                            'model_score': ms,
                                            'album_head': ah, })

    def parse_img(self, response):
        item = MeituRankDiyItem()
        item['model_name'] = response.meta['model_name']
        item['model_score'] = response.meta['model_score']
        item['album_head'] = response.meta['album_head']
        item['img_url'] = response.xpath('//*[@id="main-wrapper"]/div[2]/p/a/img/@src').extract_first()
        yield item

        npu = response.xpath('//*[@id="pages"]/a[text()="下一页"]/@href').extract_first()
        if npu:
            yield response.follow(url=npu,
                                  callback=self.parse_img,
                                  meta={'model_name': item['model_name'],
                                        'model_score': item['model_score'],
                                        'album_head': item['album_head'], })
