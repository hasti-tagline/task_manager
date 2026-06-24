import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import User
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]

        self.group_name = f"chat_{self.user_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        print(f"User {self.user_id} connected to chat")



    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )



    async def receive(self, text_data):

        data = json.loads(text_data)

        sender_id = data["sender_id"]
        receiver_id = data["receiver_id"]
        message = data["message"]

        await self.save_message(
            sender_id,
            receiver_id,
            message
        )

        await self.channel_layer.group_send(
            f"chat_{receiver_id}",
            {
                "type": "chat_message",
                "sender_id": sender_id,
                "message": message
            }
        )



    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "sender_id": event["sender_id"],
                "message": event["message"]
            })
        )



    @database_sync_to_async
    def save_message(
        self,
        sender_id,
        receiver_id,
        message
    ):

        sender = User.objects.get(
            id=sender_id
        )

        receiver = User.objects.get(
            id=receiver_id
        )

        Message.objects.create(
            sender=sender,
            receiver=receiver,
            message=message
        )