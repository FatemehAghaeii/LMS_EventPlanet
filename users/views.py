from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated

# ۱. ویو ثبت‌نام (Sign In)
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.get_or_create(user=user)
            return Response({
                "message": "User registered successfully!",
                "token": token.key,
                "role": user.role
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ۲. ویو ورود (Sign Up)
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            "token": token.key,
            "username": token.user.username,
            "role": token.user.role
        })

# ۳. ویو رندر کردن صفحه فرانت
class AuthPageView(APIView):
    def get(self, request):
        return render(request, 'users/auth.html')  # حالا با فاصله درست و ایمپورت 
    

# ویو جدید برای ارسال مشخصات کاربر فعلی به فرانت‌اِند
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "role": request.user.role
        })