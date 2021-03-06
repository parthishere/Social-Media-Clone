from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add (
            self.room_group_name,
            self.channel_name
        )
        
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": 'text_massage',
                'massage': "hello world"
            } 
        )
       
        
    async def tester_massage(self, event):
        tester = event['massage']
        
        await self.send(text_data = json.dumps({
            'tester':tester
            })
        )
     

        
    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )