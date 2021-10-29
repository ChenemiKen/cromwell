import threading
from django.http import request

from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from crawell.crawell.spiders import projects_spider
from scrapy.utils.log import configure_logging
from multiprocessing import Process, Queue

# def printit():
#     threading.Timer(1.0, printit).start()
#     print('hello world')

# printit()

def crawl():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()
    d = runner.crawl(projects_spider.ProjectsSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run(installSignalHandlers=False)
    
def crawlPPH():
    def crawl(int=int):
        d = ''
        if int>0:
            try:
                configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
                runner = CrawlerRunner()
                d = runner.crawl(projects_spider.ProjectsSpider)
                # d.addBoth(lambda _: reactor.stop())
                reactor.run(installSignalHandlers=False)
            except Exception as e:
                print(e)
        else:
            try:
                d.addBoth(lambda _: reactor.stop())
            except Exception as e:
                print(e)

    
    threading.Timer(20.0, crawlPPH).start()
    crawl()

    
    # q = Queue()
    # p = Process(target=crawl)
    # p.start()
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    # runner = CrawlerRunner()
    # d = runner.crawl(projects_spider.ProjectsSpider)
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run(installSignalHandlers=False)

def run():
    threading.Timer(20.0, run).start()
    crawlPPH()

crawlPPH()