from django.urls import path
from .views import CourseListCreateView ,CoursePageView 

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course_list_create'),
    path('dashboard/', CoursePageView.as_view(), name='course_dashboard'), 
]