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

from asgiref.sync import sync_to_async, async_to_sync
from channels.layers import get_channel_layer

# Create your views here.
def index(request):
    return render(request, template_name='app/index.html')

def new(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'cromwell_alert',
        {'type': 'chat.message', 'message': 'message'}
    )
    return render(request, template_name='app/index.html')

def startCrawler(request):
    settings = models.Config.objects.get(name='settings')
    settings.switch = True
    settings.save()
    crawlPPH()
    return render(request, template_name='app/index.html')
    

def stopCrawler(request):
    settings = models.Config.objects.get(name='settings')
    settings.switch = False
    settings.save()
    return render(request, template_name='app/index.html')  

def pphSwitchOn(request):
    request.session['pph_switch'] = True
    pph_switch = request.session['pph_switch']
    print("PPH switch: %s" %pph_switch)
    return render(request, template_name='app/index.html')

def pphSwitchOff(request):
    request.session['pph_switch']= False
    pph_switch = request.session['pph_switch']
    print("PPH switch: %s" %pph_switch) 
    return render(request, template_name='app/index.html')

def crawlPPH():
    def crawl():
        switch = models.Config.objects.get(name = 'settings').switch
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

    threading.Timer(5*60 , crawlPPH).start()
    crawl()

    