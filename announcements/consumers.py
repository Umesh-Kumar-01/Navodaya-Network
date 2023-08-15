import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import AnnouncementGroup, Announcement
from channels.db import database_sync_to_async
from datetime import datetime

class AnnouncementConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user = self.scope["user"]
            self.groups = []

            groups = await self.get_all_group_names()
            for group in groups:
                await self.channel_layer.group_add(group.name, self.channel_name)
                self.groups.append(group.name)
            
            await self.accept()
                
    @database_sync_to_async
    def get_all_group_names(self):
        return list(AnnouncementGroup.objects.all())
    
    @database_sync_to_async
    def is_admin_of_group(self, group_name):
        return self.user.admin_groups.filter(name=group_name).exists()
        
    async def disconnect(self, code):
        for group in self.groups:
            await self.channel_layer.group_discard(group, self.channel_name)
    
    @database_sync_to_async
    def get_group(self, group_name):
        return AnnouncementGroup.objects.get(name=group_name)
    
    @database_sync_to_async
    def save_announcement(self, group, user, message):
        announcement = Announcement(group=group, content=message, created_by=user)
        announcement.save()
        return announcement
    
    async def create_announcement(self, group_name, message):
        group = await self.get_group(group_name)
        user = self.scope["user"]
        announcement = await self.save_announcement(group, user, message)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        group_name = data['group']
        if await self.is_admin_of_group(group_name):
            # Only administrators of the specific group can send messages
            await self.create_announcement(group_name, message)
            await self.channel_layer.group_send(
                group_name,
                {
                    'type': 'send_announcement',
                    'message': message,
                    'group': group_name,
                }
            )
        
    
    async def send_announcement(self, event):
        sender = self.scope["user"].username
        announcement = event["message"]
        group = event["group"]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        await self.send(text_data=json.dumps({
            'sender': sender,
            'announcement': announcement,
            'timestamp': timestamp,
            'group':group
        }))