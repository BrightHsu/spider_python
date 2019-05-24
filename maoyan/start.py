from scrapy import cmdline


cmdline.execute('scrapy crawl movies -o movies.json'.split())