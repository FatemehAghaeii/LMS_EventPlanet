from rest_framework import serializers
from .models import Course, CourseStep, Feedback, Enrollment

class CourseStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStep
        fields = ['id', 'title', 'order']

class FeedbackSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Feedback
        fields = ['id', 'student_name', 'rating', 'comment', 'created_at']

class EnrolledStudentSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Enrollment
        fields = ['student_name']

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.ReadOnlyField(source='instructor.username')
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    
    steps = CourseStepSerializer(many=True, read_only=True)
    feedbacks = FeedbackSerializer(many=True, read_only=True)
    enrolled_students = EnrolledStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'price', 'capacity', 
            'image', 'duration_hours', 'prerequisites', 'level', 'level_display',
            'status', 'status_display',
            'instructor', 'instructor_name', 'steps', 'feedbacks', 'enrolled_students', 'created_at'
        ]
        read_only_fields = ['instructor', 'created_at']