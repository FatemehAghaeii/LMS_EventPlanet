from django.urls import path
from .views import RegisterView, LoginView, AuthPageView ,UserProfileView

urlpatterns = [
    path('auth/sign-in/', RegisterView.as_view(), name='register'), # ثبت‌نام
    path('auth/sign-up/', LoginView.as_view(), name='login'),      # ورود
    path('auth/profile/', UserProfileView.as_view(), name='user_profile'), # آدرس جدید پروفایل
    
]