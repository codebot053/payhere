from django.urls import path
from user import views

urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view(), name='signup'),
    path('login/', views.LogInAPIView.as_view(), name='login'), 
]
