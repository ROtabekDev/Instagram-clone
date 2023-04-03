import json
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.user.models import Message
from channels.db import database_sync_to_async
from datetime import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json["type"]
        message = text_data_json["message"]
        chat_id = text_data_json["chat_id"]
        user_id = text_data_json["user_id"]

        if type == "chat_message":

            # Add message to database
            result, msg = await database_sync_to_async(self.add_message)(chat_id, user_id, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "chat_id": chat_id, "user_id": user_id, "message": message, "result": result,
                 "created_at": datetime.now().strftime("%B %d, %Y, %I:%M %p")}
            )
        else:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "get_typing", "chat_id": chat_id, "user_id": user_id, "message": message}
            )

    # Receive message from room group
    async def chat_message(self, event):

        data = {
            "type": "chat_message",
            "chat_id": event["chat_id"],
            "user_id": event["user_id"],
            "message": event["message"],
            "result": event["result"],
            "created_at": event["created_at"]
        }

        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))

    async def get_typing(self, event):

        data = {
            "type": "get_typing",
            "chat_id": event["chat_id"],
            "user_id": event["user_id"],
            "message": event["message"]
        }

        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))

    # add message to db
    def add_message(self, chat_id, user_id, message):
        try:
            msg = Message.objects.create(chat_id=chat_id, sender_id=user_id, msg=message)
            return 'success', msg
        except Exception as e:
            return 'error', e
