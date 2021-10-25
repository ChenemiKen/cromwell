from django.core.exceptions import MiddlewareNotUsed
from django.http import request
from django.shortcuts import render
from cromwellapp import models
import threading

from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from crawell.crawell.spiders import projects_spider
from scrapy.utils.log import configure_logging

# Create your views here.
def index(request):
    crawlPPH()
    return render(request, template_name='app/index.html')

def switchOn(request):
    # request.session['switch']= True
    # switch = request.session['switch']
    switch = models.Configs.objects.get(name = 'settings').switch
    print("switch: %s" %switch)
    session = request.session
    # crawlPPH()
    return render(request, template_name='app/index.html')

def switchOff(request):
    request.session['switch']= False
    switch = request.session['switch']
    print("switch: %s" %switch) 
    return render(request, template_name='app/index.html')

def crawlPPH():
    def crawl():
        switch = models.Configs.objects.get(name = 'settings').switch
        print("switch: %s" %switch)
        
        if switch:
            try:
                configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
                runner = CrawlerRunner()
                d = runner.crawl(projects_spider.ProjectsSpider)
                # d.addBoth(lambda _: reactor.stop())
                reactor.run(installSignalHandlers=False)
            except Exception as e:
                print(e)
        # else:
        #     try:
        #         d.addBoth(lambda _: reactor.stop())
        #     except Exception as e:
        #         print(e)

    
    threading.Timer(2*60 , crawlPPH).start()
    crawl()

# def printit():
#     threading.Timer(1.0, printit).start()
#     print('hello world')
    