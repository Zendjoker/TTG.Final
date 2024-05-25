import json
import base64
from django.core.files.base import ContentFile
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers import serialize
from django.core.cache import cache
from asgiref.sync import sync_to_async
from .models import Message, Room
from Users.models import CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.customuser_id = self.scope['user'].id

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.set_user_online()

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.set_user_offline()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", None)
            file_data = text_data_json.get("file_data", None)

            message_instance = None
            if message:
                message_instance = await self.save_message(message)

            if file_data:
                await self.save_file(message_instance, file_data)

            if message_instance:
                serialized_message = serialize('json', [message_instance])
                await self.channel_layer.group_send(
                    self.room_group_name, {
                        "type": "chat.message",
                        "message": message,
                        "username": self.scope['user'].username,
                        "instance": serialized_message,
                    }
                )
        except json.JSONDecodeError:
            await self.send_error_message("Invalid JSON format")
        except ValueError as e:
            await self.send_error_message(str(e))
        except Exception as e:
            await self.send_error_message("An error occurred: " + str(e))

    async def chat_message(self, event):
        message = event["message"]
        serialized_message = event["instance"]
        username = event["username"]

        try:
            user_id = json.loads(event["instance"])[0]["fields"]["user"]
            pfp_url = await self.get_user_pfp(user_id)

            await self.send(text_data=json.dumps({
                "message": message,
                "username": username,
                "pfp": pfp_url,
                "instance": serialized_message
            }))
        except Exception as e:
            print("An error occurred:", str(e))

    async def get_user_pfp(self, user_id):
        try:
            custom_user = await sync_to_async(CustomUser.objects.get)(id=user_id)
            return custom_user.pfp.url if custom_user.pfp else None
        except CustomUser.DoesNotExist:
            print("CustomUser does not exist for the given user_id:", user_id)
            return None
        except Exception as e:
            print("An error occurred while fetching profile picture:", str(e))
            return None

    async def save_message(self, message):
        customuser = await self.get_user()
        if customuser:
            room = await self.get_room(self.room_name)
            saved_message = await sync_to_async(Message.objects.create)(user=customuser, room=room, content=message)
            return saved_message

    async def get_user(self):
        try:
            custom_user = await sync_to_async(CustomUser.objects.get)(id=self.customuser_id)
            return custom_user
        except CustomUser.DoesNotExist:
            print("CustomUser does not exist for the given customuser_id:", self.customuser_id)
            return None
        except Exception as e:
            print("An error occurred while fetching CustomUser:", str(e))
            return None

    async def get_room(self, room_name):
        try:
            room = await sync_to_async(Room.objects.get)(name=room_name)
            return room
        except Room.DoesNotExist:
            print("Room does not exist for the given room_name:", room_name)
            return None
        except Exception as e:
            print("An error occurred while fetching Room:", str(e))
            return None

    async def send_error_message(self, error_message):
        await self.send(text_data=json.dumps({"error": error_message}))

    async def set_user_online(self):
        cache.set(f'user_{self.customuser_id}_online', True, timeout=30)

    async def set_user_offline(self):
        cache.delete(f'user_{self.customuser_id}_online')

    async def save_file(self, message_instance, file_data):
        try:
            file_content = base64.b64decode(file_data["content"])
            file_name = file_data["filename"]
    
            # Use sync_to_async for file operations
            await sync_to_async(self.save_file_sync)(message_instance, file_name, file_content)
        except Exception as e:
            print("An error occurred while saving file:", str(e))
    
    # Define a synchronous method to save the file
    def save_file_sync(self, message_instance, file_name, file_content):
        try:
            message_instance.file.save(file_name, ContentFile(file_content))
        except Exception as e:
            print("An error occurred while saving file synchronously:", str(e))
