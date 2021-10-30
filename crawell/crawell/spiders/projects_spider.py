import scrapy
from datetime import date, datetime
import pprint
import re
import json
import threading
import time
from cromwellapp.models import Project
from cromwellapp.consumers import ChatConsumer
from asgiref.sync import sync_to_async, async_to_sync
from channels.layers import get_channel_layer


class ProjectsSpider(scrapy.Spider):
    name = "projects"

    def start_requests(self):
        urls = [
            'https://www.peopleperhour.com/freelance-jobs',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def send_notification(self, last_proj_id, proj_data):
        channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     'cromwell_alert',
        #     {'type': 'chat.message', 'message': 'message'}
        # )
        for key, value in proj_data.items():
            if int(key)> last_proj_id:
                async_to_sync(channel_layer.group_send)(
                    'cromwell_alert',
                    {
                        'type':'new.project',
                        'project':{
                            'proj_id':value['id'],
                            'title':value['title'],
                            'cate_id':value['category']['cate_id'],
                            'cate_name':value['category']['cate_name'],
                            'proj_description':value['proj_desc'],
                            'posted_date':value['posted_date'],
                        }
                    }
                )
                time.sleep(15)
            


    # @sync_to_async
    def save_to_db(self, proj_data):
        db_projects = Project.objects.order_by('-proj_id')
        if len(db_projects) > 0:
            last_proj_id = db_projects[0].proj_id
        else:
            last_proj_id = 0
        # send out notification 
        threading.Thread(target=self.send_notification, args=(last_proj_id, proj_data)).start()

        for key, value in proj_data.items():
            if int(key) > last_proj_id:
                project = Project()
                project.proj_id = value['id']
                project.title = value['title']
                project.cate_id = value['category']['cate_id']
                project.cate_name = value['category']['cate_name']
                project.proj_description = value['proj_desc']
                project.posted_date = value['posted_date']
                project.save()
         

    async def parse(self, response):
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
        print (projects_data)
        threading.Thread(target=self.save_to_db, args=(projects_data,)).start()
        # time = str(datetime.now().date())+str(datetime.now().time())
        # filename = f'islog'
        # with open(filename,'w')as log_file:
        #     for key, value in projects_data.items():
        #         log_file.write('%s:%s\n' %(key,value))
        # self.log(f'Saved projects to {filename}')
