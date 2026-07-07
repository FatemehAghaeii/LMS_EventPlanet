from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    # نام استاد را هم به صورت خواندنی نمایش می‌دهیم
    instructor_name = serializers.ReadOnlyField(source='instructor.username')

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'capacity', 'instructor', 'instructor_name', 'created_at']
        # فیلد استاد را read_only می‌کنیم تا خودکار از روی کاربری که لاگین کرده برداشته شود
        read_only_fields = ['instructor', 'created_at']