import time

from scrapy import cmdline


s1 = 'scrapy crawl step1'
s2 = 'python meitu_rank_diy/step2.py'
s3 = 'scrapy crawl step3'
s4 = 'python meitu_rank_diy/step4.py'
s5 = 'scrapy crawl step5'


def main():
    p1 = cmdline.os.system(s1)
    time.sleep(1)
    p2 = cmdline.os.system(s2)
    time.sleep(1)
    p3 = cmdline.os.system(s3)
    time.sleep(1)
    p4 = cmdline.os.system(s4)
    time.sleep(1)
    p5 = cmdline.os.system(s5)
    time.sleep(1)


if __name__ == '__main__':
    main()
