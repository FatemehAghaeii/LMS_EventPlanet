from django.urls import path
from .views import RegisterView, LoginView, AuthPageView

urlpatterns = [
    path('auth/sign-in/', RegisterView.as_view(), name='register'), # ثبت‌نام
    path('auth/sign-up/', LoginView.as_view(), name='login'),      # ورود
    
]