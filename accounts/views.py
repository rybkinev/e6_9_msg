import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from accounts.serializers import UserSerializer
from .forms import LoginForm


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        user = request.user

        avatar = request.FILES.get('avatar', None)

        if avatar:
            user.account.avatar = avatar
        # if
        user.save()
        return Response(json.dumps({'message': "Uploaded"}), status=200)


class LoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('chat'))
            else:
                return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        # Дополнительные действия после выхода пользователя, если необходимо
        return redirect('login')


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        return super().form_valid(form)
