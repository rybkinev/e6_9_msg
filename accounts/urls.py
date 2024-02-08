from django.urls import path, include
from rest_framework import routers

from accounts import views

router = routers.DefaultRouter()
router.register(r'accounts', views.UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('accounts/update', views.UserViewSet.as_view({'put': 'update'})),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
]
