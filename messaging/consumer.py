import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import database_sync_to_async
from .models import Message, Customer

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("message_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("message_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'new_message' in data:
            customer_id = data['customer_id']
            content = data['content']
            await self.create_message(customer_id, content)
            await self.channel_layer.group_send(
                "message_group",
                {
                    'type': 'new_message_notification',
                    'content': content,
                    'customer_id': customer_id
                }
            )
        else:
            response = data['response']
            message_id = data['message_id']
            await self.save_response(message_id, response)
            await self.channel_layer.group_send(
                "message_group",
                {
                    'type': 'message_response',
                    'message': f"Response saved for message {message_id}",
                    'message_id': message_id,
                    'response': response
                }
            )

    async def new_message_notification(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def create_message(self, customer_id, content):
        customer = Customer.objects.get(id=customer_id)
        Message.objects.create(customer=customer, content=content, status='open')

    @database_sync_to_async
    def save_response(self, message_id, response):
        message = Message.objects.get(id=message_id)
        message.response = response
        message.status = 'closed'
        message.save()
