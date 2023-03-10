import scrapy
import re
# import csv as csv1
import pandas as pd

# class CreateCsv:
#     """ csv """
#     fn1 = 'mid.csv'
#     f1 = open(file=fn1, mode='w', encoding='utf-8', newline='')
#     w1 = csv1.writer(f1)
#     fields = ['M.ID']
#     w1.writerow(fields)


class Step1Spider(scrapy.Spider):
    name = 'step1'
    allowed_domains = []
    start_urls = ['https://www.meitu131.com/nvshen/']

    def parse(self, response, **kwargs):
        mxpu = response.xpath('//*[@id="pages"]/a[text()="尾页"]/@href').extract_first()
        mxp = int(re.sub(pattern='([^0-9])', repl='', string=mxpu))

        for i in range(1, mxp + 1):
            if i == 1:
                mlpu = response.urljoin('index' + '.html')
            else:
                mlpu = response.urljoin('index_' + str(i) + '.html')
            yield response.follow(url=mlpu, callback=self.parse_mlp)

        df1 = pd.DataFrame(columns=['M.ID'])
        df1.to_csv('mid.csv', index=False)

    @staticmethod
    def parse_mlp(response):
        mli = response.xpath('/html/body/div[1]/div[2]/ul/li/div[2]')
        for i in mli:
            mu = i.xpath('p[1]/a/@href').extract_first()
            mid = int(re.sub(pattern='([^0-9])', repl='', string=mu))
            # """ csv """
            # rows = [[mid]]
            # CreateCsv.w1.writerows(rows)
            """ csv, using pandas instead of csv """
            df1 = pd.read_csv('mid.csv')
            df1.loc[len(df1) + 1] = mid
            df1.to_csv('mid.csv', index=False, mode='w', encoding='utf-8')

    # def __del__(self):
    # CreateCsv.f1.close()
