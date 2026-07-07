from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Course(models.Model):
    class CourseLevel(models.TextChoices):
        BEGINNER = 'BEGINNER', 'مقدماتی'
        INTERMEDIATE = 'INTERMEDIATE', 'متوسط'
        ADVANCED = 'ADVANCED', 'پیشرفته'

    # 🌟 وضعیت‌های چهارگانه خواسته‌شده در داک استاد
    class CourseStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'پیش‌نویس (Draft)'
        PUBLISHED = 'PUBLISHED', 'منتشر شده (Published)'
        CLOSED = 'CLOSED', 'ثبت‌نام بسته شده (Closed)'
        FINISHED = 'FINISHED', 'به پایان رسیده (Finished)'

    title = models.CharField(max_length=255, verbose_name="عنوان دوره")
    description = models.TextField(verbose_name="توضیحات دوره")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="قیمت")
    capacity = models.PositiveIntegerField(verbose_name="ظرفیت دوره")
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, verbose_name="تصویر دوره")
    duration_hours = models.PositiveIntegerField(default=0, verbose_name="طول دوره (ساعت)")
    prerequisites = models.CharField(max_length=255, default="ندارد", verbose_name="پیش‌نیازها")
    level = models.CharField(max_length=20, choices=CourseLevel.choices, default=CourseLevel.BEGINNER, verbose_name="سطح دوره")
    
    # 🌟 فیلد وضعیت جدید (وضعیت پیش‌فرض روی Draft است)
    status = models.CharField(max_length=20, choices=CourseStatus.choices, default=CourseStatus.DRAFT, verbose_name="وضعیت رویداد")

    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_courses', limit_choices_to={'role': 'ORGANIZER'}, verbose_name="مدرس")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # 🌟 متد منطقی قفل کردن تغییر وضعیت‌ها (Enforce Status Flow)
    def change_status(self, new_status):
        allowed_transitions = {
            self.CourseStatus.DRAFT: [self.CourseStatus.PUBLISHED],
            self.CourseStatus.PUBLISHED: [self.CourseStatus.CLOSED],
            self.CourseStatus.CLOSED: [self.CourseStatus.FINISHED],
            self.CourseStatus.FINISHED: []  # رویداد تمام شده دیگر تغییر نمی‌کند
        }
        
        if new_status not in allowed_transitions.get(self.status, []):
            raise ValidationError(f"تغییر وضعیت غیرمجاز از {self.get_status_display()} به {new_status}!")
        
        self.status = new_status
        self.save()


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_students')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')


class CourseStep(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='steps', verbose_name="دوره")
    title = models.CharField(max_length=255, verbose_name="عنوان مرحله/سرفصل")
    order = models.PositiveIntegerField(default=1, verbose_name="ترتیب نمایش")

    class Meta:
        ordering = ['order']


class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks', verbose_name="دوره")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="دانشجو")
    rating = models.PositiveIntegerField(verbose_name="امتیاز (از ۱ تا ۵)")
    comment = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')