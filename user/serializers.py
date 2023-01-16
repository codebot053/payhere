from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from moneybook.models import MoneyBook



class UserCreateSerializer(serializers.ModelSerializer):
    """유저 생성을 위한 ModelSerializer"""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "name", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        """user를 생성하면서 해당 user의 moneybook object도 같이 생성"""

        email = validated_data.get("email")
        name = validated_data.get("name")
        password = validated_data.get("password")
        user = User(email=email, name=name)
        user.set_password(password)
        user.save()

        user_moneybook = MoneyBook.objects.create(user=user)
        user_moneybook.save()
        return user

class UserLogInSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email", "name"]