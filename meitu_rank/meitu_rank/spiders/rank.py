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
                callback=self.parse_albumlist,
                meta={
                    'mn': mn,
                },
            )

    def parse_albumlist(self, response):
        al = response.xpath('/html/body/div[3]/div[2]/ul/li/div[2]/a')
        if al:
            for i in al:
                at = re.sub(
                    pattern='([^\u4e00-\u9fff\u0041-\u005a\u0061-\u007a])',
                    repl='',
                    string=i.xpath('text()').extract_first()
                )
                au = i.xpath('@href').extract_first()
                yield scrapy.Request(
                    url=response.urljoin(au),
                    callback=self.parse_album,
                    meta={
                        'mn': response.meta['mn'],
                        'at': at,
                    },
                )

    def parse_album(self, response):
        mn = response.meta['mn']
        at = response.meta['at']

        mpu = response.xpath('//*[@id="pages"]/a[text()="尾页"]/@href').extract_first()
        a = mpu.find('_')
        b = mpu.find('.html')
        mp = int(mpu[a + 1:b])

        for i in range(1, mp+1):
            if i == 1:
                ipu = response.urljoin('index.html')
            else:
                ipu = response.urljoin('index_' + str(i) + '.html')
            yield response.follow(url=ipu, callback=self.parse_photo, meta={'mn': mn, 'at': at})

    @staticmethod
    def parse_photo(response):
        i = MeituRankItem()
        i['model_name'] = response.meta['mn']
        i['album_title'] = response.meta['at']
        i['image_urls'] = response.xpath('/html/body/div[1]/div[2]/p/a/img/@src').extract_first()
        if i['image_urls']:
            yield i
        else:
            print('!*' * 9, 'Not get image url at page:', response.url)

        print(i)
