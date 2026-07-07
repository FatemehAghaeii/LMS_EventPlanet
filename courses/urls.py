from django.urls import path
from .views import CourseListCreateView, EnrollCourseView, CoursePageView, AddCourseStepView, AddFeedbackView, UpdateCourseStatusView

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course_list_create'),
    path('courses/enroll/', EnrollCourseView.as_view(), name='my_courses'), 
    path('courses/enroll/<int:course_id>/', EnrollCourseView.as_view(), name='enroll_course'), 
    path('courses/<int:course_id>/steps/', AddCourseStepView.as_view(), name='add_course_step'),
    path('courses/<int:course_id>/feedback/', AddFeedbackView.as_view(), name='add_course_feedback'),
    
    #  آدرس جدید تغییر وضعیت توسط استاد:
    path('courses/<int:course_id>/update-status/', UpdateCourseStatusView.as_view(), name='update_course_status'),
    
    path('dashboard/', CoursePageView.as_view(), name='course_dashboard'),
]