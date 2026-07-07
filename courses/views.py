from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseSerializer
from django.shortcuts import render


class CourseListCreateView(APIView):
    # برای این بخش حتماً کاربر باید توکن معتبر داشته باشد (احراز هویت شده باشد)
    permission_classes = [IsAuthenticated]

    # ۱. مشاهده لیست تمام دوره‌ها (مخصوص همه کاربران لاگین شده)
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    # ۲. ساخت دوره جدید (فقط مخصوص نقش ORGANIZER یعنی استاد)
    def post(self, request):
        # بررسی نقش کاربر
        if request.user.role != 'ORGANIZER':
            return Response(
                {"detail": "فقط اساتید (Organizer) مجاز به ساخت دوره هستند."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            # دوره را ذخیره و استاد را کاربرِ فعلی قرار می‌دهیم
            serializer.save(instructor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    # ویو مربوط به رندر کردن صفحه اصلی دوره‌ها در فرانت
class CoursePageView(APIView):
    def get(self, request):
        return render(request, 'courses/main.html')