# استفاده از پایتون رسمی و سبک به عنوان پایه
FROM python:3.11-slim

# تنظیم متغیرهای محیطی برای عملکرد بهتر پایتون در داکر
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تعیین پوشه کاری داخل کانتینر
WORKDIR /app

# نصب ابزارهای مورد نیاز سیستم برای پورتگرس و ابزارهای کامپایل
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# کپی کردن ابزارهای مورد نیاز پایتون و نصب آنها (کتابخانه pillow اضافه شد)
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir django djangorestframework psycopg2-binary django-environ pillow

# کپی کردن کل کدهای پروژه به داخل کانتینر
COPY . /app/

# اجرای اسکریپت آماده‌سازی و ران کردن سرور
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]