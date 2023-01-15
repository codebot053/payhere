from django.urls import path
from user import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup')
]
