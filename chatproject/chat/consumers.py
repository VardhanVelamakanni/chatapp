# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user ID from the URL path
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the chat room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the chat room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        user_id = text_data_json['user_id']

        # Get the recipient user
        recipient = User.objects.get(id=self.room_name)
        
        # Save the message in the database
        message = Message.objects.create(
            sender=self.scope["user"],
            recipient=recipient,
            content=message_content
        )

        # Send the message to the WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': self.scope["user"].username,
            }
        )

    # Receive message from group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
