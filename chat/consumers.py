import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.chat_id = self.scope['url_route']['kwargs'].get('chat_id', None)
        # self.chat_group_name = f"chat_{self.chat_id}"
        self.chat_group_name = 'testing_websocket_group'

        print(self.scope['user'])

        # Присоединение к группе чата
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединение от группы чата
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # Обработчик события от клиента
    async def receive(self, text_data):
        user = self.scope['user']
        print(user)
        if not user.is_authenticated:
            await self.send_error('User not authenticated')
            return

        data = json.loads(text_data)

        message_type = data.get('type', None)
        if not message_type:
            await self.send_error('Не определен тип сообщения')
            return

        if message_type == 'chat.created':
            # message = data.get('name', None)
            await self.create_chat(data)
        elif message_type == 'chat.message':
            await self.send_message(data)
            # message = data['text']
            #
            # await self.send(text_data=json.dumps({
            #         'type': message_type,
            #         'text': message,
            #     }))
            # Отправка сообщения обратно в группу чата
            # await self.channel_layer.group_send(
            #     self.chat_group_name,
            #     {
            #         'type': message_type,
            #         'text': message,
            #     }
            # )

    async def create_chat(self, event):
        chat_name = event['name']

        chat = await sync_to_async(Chat.objects.create)(name=chat_name)
        await sync_to_async(chat.members.set)([self.scope['user']])
        response_data = {
            'type': 'chat.created',
            'chat_id': chat.id,
            'name': chat_name,
        }

        # Отправка сообщения обратно клиенту
        await self.send(text_data=json.dumps(response_data))

    async def send_message(self, data):
        chat_id = data['chatId']
        message = data['text']

        # Сохранение сообщения в базе данных
        await sync_to_async(Message.objects.create)(
            chat_id=chat_id,
            text=message,
            sender=self.scope['user']
        )

        await self.send(text_data=json.dumps({
            'type': 'chat.message',
            'text': message,
        }))

        # Отправка сообщения в группу чата
        # await self.channel_layer.group_send(
        #     f'chat_{chat_id}',
        #     {
        #         'type': 'chat.message',
        #         'message': message_content,
        #         'user_id': user_id,
        #     }
        # )

    # Обработчик события от группы чата
    async def chat_message(self, event):
        message = event['text']

        # Отправка сообщения клиенту
        await self.send(text_data=json.dumps({
            'type': 'chat.message',
            'text': message,
        }))

    async def send_error(self, error_message):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'error_message': error_message
        }))
