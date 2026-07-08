from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.core.exceptions import ValidationError
from .models import Course, Enrollment, CourseStep, Feedback, Attribute, CourseAttributeValue
from .serializers import CourseSerializer, CourseStepSerializer, FeedbackSerializer

class CourseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', '')
        
        if request.user.role == 'PARTICIPANT':
            base_courses = Course.objects.exclude(status='DRAFT')
        else:
            base_courses = Course.objects.filter(instructor=request.user)

        if search_query:
            courses = base_courses.filter(title__icontains=search_query) | base_courses.filter(description__icontains=search_query)
        else:
            courses = base_courses
            
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'ORGANIZER':
            return Response({"detail": "فقط اساتید (Organizer) مجاز به ساخت دوره هستند."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(instructor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user)
        courses = [e.course for e in enrollments]
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "دوره مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        if course.status != 'PUBLISHED':
            return Response({"detail": "ثبت‌نام در این رویداد در حال حاضر مقدور نیست (فقط رویدادهای منتشرشده)."}, status=status.HTTP_400_BAD_REQUEST)

        if course.capacity <= 0:
            return Response({"detail": "ظرفیت این دوره تکمیل شده است!"}, status=status.HTTP_400_BAD_REQUEST)

        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response({"detail": "شما قبلاً در این دوره ثبت‌نام کرده‌اید."}, status=status.HTTP_400_BAD_REQUEST)

        course.capacity -= 1
        course.save()

        Enrollment.objects.create(student=request.user, course=course)
        return Response({"detail": "پرداخت آنلاین موفقیت‌آمیز بود و دوره فعال شد!"}, status=status.HTTP_200_OK)


class AddCourseStepView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "دوره یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        if course.instructor != request.user:
            return Response({"detail": "شما مدرس این دوره نیستید و اجازه ثبت سرفصل ندارید."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CourseStepSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "دوره یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        if course.status != 'FINISHED':
            return Response({"detail": "تنها پس از پایان یافتن رویداد مجاز به ثبت بازخورد هستید."}, status=status.HTTP_400_BAD_REQUEST)

        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response({"detail": "شما در این دوره ثبت‌نام نکرده‌اید و مجاز به ثبت نظر نیستید."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(course=course, student=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response({"detail": "شما قبلاً بازخورد خود را برای این دوره ثبت کرده‌اید."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCourseStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "دوره یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        if course.instructor != request.user:
            return Response({"detail": "شما مالک این رویداد نیستید."}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        if not new_status:
            return Response({"detail": "وضعیت جدید ارسال نشده است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course.change_status(new_status)
            return Response({"detail": f"وضعیت رویداد با موفقیت تغییر یافت.", "status": course.status})
        except ValidationError as e:
            return Response({"detail": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)


class CoursePageView(APIView):
    def get(self, request):
        return render(request, 'courses/main.html')