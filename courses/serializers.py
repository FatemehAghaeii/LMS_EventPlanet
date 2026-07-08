from rest_framework import serializers
from .models import Course, CourseStep, Feedback, Enrollment, Attribute, CourseAttributeValue, CourseResult

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

class CourseAttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.ReadOnlyField(source='attribute.name')

    class Meta:
        model = CourseAttributeValue
        fields = ['id', 'attribute_name', 'value']

# 🌟 سریالایزر جدید برای متادیتا و نتایج نهایی رویداد
class CourseResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResult
        fields = ['id', 'content', 'created_at']

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.ReadOnlyField(source='instructor.username')
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    
    steps = CourseStepSerializer(many=True, read_only=True)
    feedbacks = FeedbackSerializer(many=True, read_only=True)
    enrolled_students = EnrolledStudentSerializer(many=True, read_only=True)
    dynamic_attributes = CourseAttributeValueSerializer(many=True, read_only=True)
    
    #  متصل شدن بخش نتایج به سریالایزر اصلی دوره
    result = CourseResultSerializer(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'price', 'capacity', 
            'image', 'duration_hours', 'status', 'status_display', 
            'instructor', 'instructor_name', 'steps', 'feedbacks', 
            'enrolled_students', 'dynamic_attributes', 'result', 'created_at'
        ]
        read_only_fields = ['instructor', 'created_at']