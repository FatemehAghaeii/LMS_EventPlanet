from django.contrib import admin
from .models import Course, Enrollment, CourseStep, Feedback, Attribute, CourseAttributeValue

class CourseAttributeValueInline(admin.TabularInline):
    model = CourseAttributeValue
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'status', 'price']
    inlines = [CourseAttributeValueInline]

admin.site.register(Attribute)
admin.site.register(Enrollment)
admin.site.register(CourseStep)
admin.site.register(Feedback)
admin.site.register(CourseAttributeValue)