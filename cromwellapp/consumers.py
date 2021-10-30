import json
import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'cromwell_alert'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        self.send(text_data=json.dumps({
            'type':'new.project',
            'project':{
                'proj_id':'value[id]',
                'title':'value[title]',
                'cate_id':'value[category][cate_id]',
                'cate_name':'value[category][cate_name]',
                'proj_description':'value[proj_desc]',
                'posted_date':'value[posted_date]',
            }
        }))


    def disconnect(self, close_code):
        # 
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    def chat_message(self, event):
        # message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': 'new project'
        }))

    # Handles broadcast of new project
    def new_project(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': 'new project',
            'project': event['project']
        }))