from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        chat_name = request.data.get('name')
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        members_data = request.data.get('members')
        members = [request.user]
        if not chat_name:
            # Если не задано имя, значит это не групповой чат, значит в members лежит id User
            recipient = User.objects.get(id=int(members_data))
            chat_name = recipient
            members.append(recipient)
        else:
            for i in members_data:
                recipient = User.objects.get(id=int(i))
                members.append(recipient)

        # Пример: создание чата и добавление пользователя в чат
        chat = Chat.objects.create(name=chat_name)
        # chat = Chat(name=chat_name)
        chat.members.set(members)

        # chat.save()

        serializer = self.get_serializer(chat, data=request.data)

        # Вызовите is_valid с raise_exception=True, чтобы получить исключение при ошибке валидации
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessagesViewSet(viewsets.ModelViewSet):
    # queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)

    # def create(self, request, *args, **kwargs):
    #     chat_id = request.data.get('chatId')
    #
    #     if not request.user.is_authenticated:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #
    #     message = Message.objects.create(
    #         chat_id=chat_id,
    #         text=request.data.get('text'),
    #         sender=request.user
    #     )
    #
    #     serializer = self.get_serializer(message, data=request.data)
    #
    #     # Вызовите is_valid с raise_exception=True, чтобы получить исключение при ошибке валидации
    #     serializer.is_valid(raise_exception=True)
    #
    #     serializer.save()
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatView(LoginRequiredMixin, TemplateView):
    # template_name = 'chat.html'
    login_url = '/accounts/login/'

    def get_template_names(self):
        return ['chat.html']
