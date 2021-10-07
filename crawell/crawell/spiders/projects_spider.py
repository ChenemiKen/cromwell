import scrapy
from datetime import date, datetime
import pprint
import re
import json


class QuotesSpider(scrapy.Spider):
    name = "projects"

    def start_requests(self):
        urls = [
            'https://www.peopleperhour.com/freelance-jobs',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # pattern = re.compile(r"KBB\.Vehicle\.Pages\.PricingOverview\.Buyers\.setup\(.*?data: ({.*?}),\W+adPriceRanges", re.MULTILINE | re.DOTALL)
        script= response.xpath("//script[contains(.,'window.PPHReact')]/text()").get()
        script = re.findall(r"window.PPHReact.initialState={.*};\n", script)[0]
        script_strip = re.sub(r";\n", "", script)
        initialState = script_strip.split("initialState=")[1]
        initialState = json.loads(initialState)
        projects = initialState['entities']['projects']
        projects_data={}
        for key,value in projects.items():
            projects_data[key]={
                'id': value['id'],
                'title': value['attributes']['title'],
                'category': {
                    'cate_id':value['attributes']['category']['cate_id'], 
                    'cate_name':value['attributes']['category']['cate_name'] 
                },
                'proj_desc': value['attributes']['proj_desc'],
                'posted_date':value['attributes']['posted_dt'],
            }
        with open('initialState.log','w')as log_file:
            for key, value in projects_data.items():
                log_file.write('%s:%s\n' %(key,value))


        time = datetime.now()
        filename = f'projects.html'
        script_strip=script_strip.encode("utf-8")
        with open(filename, 'wb') as f:
            f.write(script_strip)
        self.log(f'Saved file {filename}')