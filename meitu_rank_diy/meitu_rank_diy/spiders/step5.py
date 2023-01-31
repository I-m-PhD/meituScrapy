import scrapy
import pathlib
import pandas as pd
from meitu_rank_diy.items import MeituRankDiyItem
import re


class Step5Spider(scrapy.Spider):
    name = 'step5'
    allowed_domains = []
    start_urls = ['https://www.meitu131.com/']

    def parse(self, response, **kwargs):
        if pathlib.Path('model_sorted.csv').exists():
            d = pd.read_csv('model_sorted.csv', encoding='utf-8')

            """
            How many models you want to collect?
            Change the integers below as you wish: y should be larger than x.
            Refer to the line numbers in model_sorted.csv file: 
            when x=0, it gets you the model in line 2.
            e.g. x=145 will get you all albums and photos of 古月 in line 147
            """

            x = 145
            y = 146
            for i in range(x, y):
                mn = d.iloc[i]['M.NAME']
                ms = d.iloc[i]['M.SCORE']
                mu = d.iloc[i]['M.URL']
                yield response.follow(url=mu,
                                      callback=self.parse_alist,
                                      meta={'mn': mn,
                                            'ms': ms, })

    def parse_alist(self, response):
        mn = response.meta['mn']
        ms = response.meta['ms']

        al = response.xpath('/html/body/div[3]/div[2]/ul/li/div[2]/a')
        if al:
            for i in al:
                au = i.xpath('@href').extract_first()
                ah = re.sub(pattern='([^0-9\u4e00-\u9fff\u0041-\u005a\u0061-\u007a])',
                            repl='',
                            string=i.xpath('text()').extract_first())
                yield response.follow(url=au,
                                      callback=self.parse_album,
                                      meta={'mn': mn,
                                            'ms': ms,
                                            'ah': ah, })

    def parse_album(self, response):
        mn = response.meta['mn']
        ms = response.meta['ms']
        ah = response.meta['ah']

        mpu = response.xpath('//*[@id="pages"]/a[text()="尾页"]/@href').extract_first()
        a = mpu.find('_')
        b = mpu.find('.html')
        mp = int(mpu[a + 1:b])

        for i in range(1, mp+1):
            if i == 1:
                ipu = response.urljoin('index.html')
            else:
                ipu = response.urljoin('index_' + str(i) + '.html')
            yield response.follow(url=ipu,
                                  callback=self.parse_img,
                                  meta={'mn': mn,
                                        'ms': ms,
                                        'ah': ah, })

    @staticmethod
    def parse_img(response):
        item = MeituRankDiyItem()
        item['model_name'] = response.meta['mn']
        item['model_score'] = response.meta['ms']
        item['album_head'] = response.meta['ah']
        item['img_url'] = response.xpath('//*[@id="main-wrapper"]/div[2]/p/a/img/@src').extract_first()
        if item['img_url']:
            yield item
        else:
            print('!*'*9, 'Not get image url at page:', response.url)
