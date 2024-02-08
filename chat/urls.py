from django.urls import path, include
from rest_framework import routers

from . import views
from chat.routing import websocket_urlpatterns

router = routers.DefaultRouter()
router.register(r'chats', views.ChatViewSet, basename='chats')
router.register(r'messages', views.MessagesViewSet, basename='messages')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', include(websocket_urlpatterns)),
    path('', views.ChatView.as_view(), name='chat'),
    path('api/chats/<int:chat_id>/messages/',
         views.MessagesViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='chat-messages-list'
     ),
]
