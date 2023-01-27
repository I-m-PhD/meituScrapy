from scrapy import cmdline

cmdline.execute('scrapy crawl rank -s LOG_FILE=all.log'.split())
