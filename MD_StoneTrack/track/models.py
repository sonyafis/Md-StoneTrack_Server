import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg, F, ExpressionWrapper, DurationField

class SuperUser(AbstractUser):
    id_super_user = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']
    ADMIN = 'admin'
    COURIER = 'courier'
    CLIENT = 'client'

    TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (COURIER, 'Courier'),
        (CLIENT, 'Client'),
    ]

    # Добавляем поле type_user с выбором
    type_user = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=CLIENT,  # Можно по умолчанию сделать 'client'
    )

    def __str__(self):
        return self.username


class Status(models.Model):
    id_status = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50)

    def __str__(self):
        return self.status_name


class Order(models.Model):
    id_order = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=20, unique=True, blank=True)  # Изменено с IntegerField на CharField

    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    id_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    id_client = models.ForeignKey(SuperUser, on_delete=models.CASCADE, related_name="client_orders")
    id_courier = models.ForeignKey(SuperUser, on_delete=models.CASCADE, related_name="courier_orders", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            today = datetime.date.today().strftime('%Y%m%d')
            prefix = f"ORD-{today}"
            last_order = Order.objects.filter(order_number__startswith=prefix).order_by('-order_number').first()

            if last_order and last_order.order_number:
                last_num = int(last_order.order_number.split("-")[-1])
                next_num = last_num + 1
            else:
                next_num = 1

            self.order_number = f"{prefix}-{next_num:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.address}"



class Feedback(models.Model):
    id_feedback_user = models.AutoField(primary_key=True)
    user_fullname = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Добавляем choices для типа отзыва на русском языке
    TYPE_FEEDBACK_CHOICES = [
        ('complaint', 'Жалоба'),
        ('suggestion', 'Предложение'),
        ('inquiry', 'Запрос'),
        ('praise', 'Похвала'),
        ('issue', 'Проблема'),
        ('request', 'Заявка'),
        ('feedback', 'Обратная связь'),
    ]

    type_feedback = models.CharField(max_length=50, choices=TYPE_FEEDBACK_CHOICES)  # Поле с выбором типа отзыва

    # Пользователь и его тип
    USER_TYPE_CHOICES = [
        ('courier', 'Курьер'),
        ('client', 'Клиент'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=True, null=True)  # Тип пользователя

    # Связь с пользователем
    id_super_user = models.ForeignKey(SuperUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Автоматически заполняем user_type на основе id_super_user"""
        if self.id_super_user:
            self.user_type = self.id_super_user.type_user  # Заполняем тип пользователя
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Обратная связь от {self.user_fullname} ({self.user_type})"


class CourierAnalytics(models.Model):
    id_courier_analytics = models.AutoField(primary_key=True)
    id_courier = models.OneToOneField(SuperUser, on_delete=models.CASCADE, related_name="analytics")
    total_orders = models.IntegerField(default=0)
    avg_delivery_time = models.DurationField(blank=True, null=True)  # Среднее время доставки
    last_updated = models.DateTimeField(auto_now=True)

    def update_analytics(self):
        """Обновление аналитики по курьеру."""
        from django.utils.timezone import now
        from datetime import timedelta

        # Получаем все заказы с зафиксированным временем доставки
        orders = Order.objects.filter(id_courier=self.id_courier, delivered_at__isnull=False)

        # Обновляем количество заказов
        self.total_orders = orders.count()

        # Вычисляем среднее время доставки
        avg_time = orders.aggregate(avg_time=Avg(ExpressionWrapper(
            F("delivered_at") - F("created_at"),
            output_field=DurationField()
        )))["avg_time"]

        self.avg_delivery_time = avg_time if avg_time else timedelta(0)  # Если нет данных, то 0

        self.last_updated = now()
        self.save()

    def __str__(self):
        return f"Analytics for {self.id_courier.first_name}"
