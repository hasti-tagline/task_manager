import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User,Task,Message,Notification





# Task Consumer
class TaskConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.user_id = self.scope["url_route"]["kwargs"].get("user_id")

        if not self.user_id:
            await self.close()
            return

        self.group_name = f"user_{self.user_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        print(f"User {self.user_id} connected")


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )


    async def task_assigned(self, event):

        await self.send(text_data=json.dumps(event["data"]))


    async def task_updated(self, event):

        await self.send(
            text_data=json.dumps({
                "event": "task_updated",
                "task_id": event["data"]["task_id"],
                "status": event["data"]["status"]
            })
        )

    async def submission_uploaded(self, event):
        await self.send(
            text_data=json.dumps({
                "event": "submission_uploaded",
                "task_id": event["data"]["task_id"],
                "file_name": event["data"]["file_name"],
                "uploaded_by": event["data"]["uploaded_by"]
            })
         )
        

    async def new_chat_notification(self, event):

        await self.send(
            text_data=json.dumps({
                "event": "new_chat_notification",
                "task_id": event["data"]["task_id"],
                "sender_id": event["data"]["sender_id"],
                "message": event["data"]["message"]
            })
        )






# Chat Consumer
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.task_id = self.scope["url_route"]["kwargs"].get("task_id")

        if not self.task_id:
            await self.close()
            return

        self.group_name = f"task_{self.task_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        print(f"Chat connected for task {self.task_id}")


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )



        
    # gets all task users except the sender.
    @database_sync_to_async
    def get_receivers(self, sender_id):
        task = Task.objects.get(id=self.task_id)

        users = list(task.assigned_to.all())
        users.append(task.created_by)

        return [u.id for u in users if u.id != int(sender_id)]



    # create chat notification in database
    @database_sync_to_async
    def create_chat_notification(self, receiver_id, task_id, sender_name):

        task = Task.objects.get(id=task_id)

        Notification.objects.create(
            user_id=receiver_id,
            task=task,      
            title="New Chat Message",
            message=f"{sender_name} sent a message in task '{task.title}'"
        )


    # get sender id 
    @database_sync_to_async
    def get_sender(self, sender_id):
        return User.objects.get(id=sender_id)


    # recieve data from frontend
    async def receive(self, text_data):
        data = json.loads(text_data)

        sender_id = data["sender_id"]
        message = data["message"]
        sender = await self.get_sender(sender_id)

        await self.save_message(sender_id, self.task_id, message)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "sender_id": sender_id,
                "message": message,
            }
        )

        receivers = await self.get_receivers(sender_id)

        for receiver_id in receivers:
            await self.create_chat_notification(
                    receiver_id,
                    self.task_id,
                    sender.username
                )   

            await self.channel_layer.group_send(
                f"user_{receiver_id}",
                {
                    "type": "new_chat_notification",
                    "data": {
                        "task_id": self.task_id,
                        "sender_id": sender_id,
                        "message": "New message received"
                    }
                }
            )


    # send data to frontend
    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                "sender_id": event["sender_id"],
                "message": event["message"]
            })
        )


    # save message in database.
    @database_sync_to_async
    def save_message(self, sender_id, task_id, message):

        print("task_id received:", task_id)
        print("task_id type:", type(task_id))

        sender = User.objects.get(id=sender_id)
        task = Task.objects.get(id=task_id)

        Message.objects.create(
            sender=sender,
            task=task,
            message=message
    )
