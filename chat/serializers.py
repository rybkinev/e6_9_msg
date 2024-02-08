from .models import *
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        # fields = '__all__'
        fields = [
            'id',
            'text',
            'sender',
            'sender_username',
            'chat',
        ]
        read_only_fields = [
            'sender'
        ]


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = [
            'id',
            'name',
        ]
