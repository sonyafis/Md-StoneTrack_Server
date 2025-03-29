from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg, F, ExpressionWrapper, DurationField

class SuperUser(AbstractUser):
    id_super_user = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20)
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
    order_number = models.IntegerField(unique=True)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    id_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    id_client = models.ForeignKey(SuperUser, on_delete=models.CASCADE, related_name="client_orders")
    id_courier = models.ForeignKey(SuperUser, on_delete=models.CASCADE, related_name="courier_orders", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Фиксация времени создания заказа
    delivered_at = models.DateTimeField(blank=True, null=True)  # Фиксация времени доставки

    def __str__(self):
        return f"Order {self.order_number} - {self.address}"


class Feedback(models.Model):
    id_feedback_user = models.AutoField(primary_key=True)
    user_fullname = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    type_feedback = models.CharField(max_length=50)  # Например, "complaint", "suggestion"
    #
    id_super_user = models.ForeignKey(SuperUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Feedback from {self.user_fullname}"


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
