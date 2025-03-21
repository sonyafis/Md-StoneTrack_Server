from django.contrib import admin
from .models import SuperUser, Status, Order, Feedback, CourierAnalytics

# Регистрируем все модели в админке
admin.site.register(SuperUser)
admin.site.register(Status)
admin.site.register(Order)
admin.site.register(Feedback)
admin.site.register(CourierAnalytics)
