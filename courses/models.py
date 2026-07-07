from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان دوره")
    description = models.TextField(verbose_name="توضیحات دوره")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="قیمت")
    capacity = models.PositiveIntegerField(verbose_name="ظرفیت دوره")
    
    # متصل کردن دوره به استادی که آن را ساخته است
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_courses',
        limit_choices_to={'role': 'ORGANIZER'}, # فقط کاربرانی با نقش استاد بتوانند دوره بسازند
        verbose_name="مدرس"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title