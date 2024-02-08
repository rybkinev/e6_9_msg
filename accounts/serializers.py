from .models import *
from rest_framework import serializers


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         # fields = '__all__'
#         fields = ['id', 'username', 'first_name', 'account_avatar']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['avatar']  # Укажите нужные поля


class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'account']
        read_only_fields = ['username']

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        user = User.objects.create(**validated_data)
        # Account.objects.create(system_user=user, **account_data)
        return user
