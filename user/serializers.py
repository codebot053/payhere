from rest_framework import serializers
from .models import User
from moneybook.models import MoneyBook


class UserCreateSerializer(serializers.ModelSerializer):
    '''유저 생성을 위한 ModelSerializer'''
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        '''user를 생성하면서 해당 user의 moneybook object도 같이 생성'''
        email = validated_data.get("email")
        name = validated_data.get("name")
        password = validated_data.get("password")
        user = User(email=email, name=name)
        user.set_password(password)
        user.save()

        user_moneybook = MoneyBook.objects.create(user=user)
        user_moneybook.save()
        return user
