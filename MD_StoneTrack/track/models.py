from django.contrib.auth.models import AbstractUser
from django.db import models


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

    type_user = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=CLIENT,
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
    order_number = models.CharField(max_length=20, unique=True, blank=True)

    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    id_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    id_client = models.ForeignKey(SuperUser, on_delete=models.CASCADE, related_name="client_orders")
    id_courier = models.ForeignKey(SuperUser, on_delete=models.CASCADE, related_name="courier_orders", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            prefix = "ORD-"
            last_order = Order.objects.filter(order_number__startswith=prefix).order_by('-order_number').first()

            if last_order and last_order.order_number:
                try:
                    last_num = int(last_order.order_number.split("-")[-1])
                    next_num = last_num + 1
                except (ValueError, IndexError):
                    next_num = 1001
            else:
                next_num = 1001

            self.order_number = f"{prefix}{next_num:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.address}"



class Feedback(models.Model):
    id_feedback_user = models.AutoField(primary_key=True)
    user_fullname = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    TYPE_FEEDBACK_CHOICES = [
        ('complaint', 'Жалоба'),
        ('suggestion', 'Пожелания'),
        ('inquiry', 'Вопрос'),
        ('praise', 'Похвала'),
        ('issue', 'Проблема'),
        ('request', 'Заявка'),
        ('feedback', 'Отзыв'),
    ]

    type_feedback = models.CharField(max_length=50, choices=TYPE_FEEDBACK_CHOICES)

    # Пользователь и его тип
    USER_TYPE_CHOICES = [
        ('courier', 'Курьер'),
        ('client', 'Клиент'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=True, null=True)

    id_super_user = models.ForeignKey(SuperUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.id_super_user:
            self.user_type = self.id_super_user.type_user
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Обратная связь от {self.user_fullname} ({self.user_type})"

