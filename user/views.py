from rest_framework import generics
from .models import User
from .serializers import UserCreateSerializer

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer