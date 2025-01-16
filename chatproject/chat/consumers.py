
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'chat_{self.room_name}'

        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        
        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        user_id = text_data_json['user_id']

        
        recipient = User.objects.get(id=self.room_name)
        
        
        message = Message.objects.create(
            sender=self.scope["user"],
            recipient=recipient,
            content=message_content
        )

        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': self.scope["user"].username,
            }
        )

    
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
