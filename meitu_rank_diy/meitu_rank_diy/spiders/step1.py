import scrapy
import re
import csv as csv1


""" csv """
fn1 = 'mid.csv'
f1 = open(file=fn1, mode='w', encoding='utf-8', newline='')
w1 = csv1.writer(f1)
fields = ['M.ID']
w1.writerow(fields)


class Step1Spider(scrapy.Spider):
    name = 'step1'
    allowed_domains = []
    start_urls = ['https://www.meitu131.com/nvshen/']

    def parse(self, response, **kwargs):
        mxpu = response.xpath('//*[@id="pages"]/a[text()="尾页"]/@href').extract_first()
        mxp = int(re.sub(pattern='([^0-9])', repl='', string=mxpu))
        for i in range(1, mxp+1):
            if i == 1:
                mlpu = response.urljoin('index' + '.html')
            else:
                mlpu = response.urljoin('index_' + str(i) + '.html')
            yield response.follow(url=mlpu, callback=self.parse_mlp)

    @staticmethod
    def parse_mlp(response):
        mli = response.xpath('/html/body/div[1]/div[2]/ul/li/div[2]')
        for i in mli:
            mu = i.xpath('p[1]/a/@href').extract_first()
            mid = int(re.sub(pattern='([^0-9])', repl='', string=mu))
            rows = [[mid]]
            w1.writerows(rows)

    def __del__(self):
        f1.close()
