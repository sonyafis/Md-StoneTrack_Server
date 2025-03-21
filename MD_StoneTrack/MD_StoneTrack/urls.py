from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from track.views import *

# 🚀 Создаем и настраиваем роутер
router = DefaultRouter()
router.register("superusers", SuperUserViewSet, basename="superuser")
router.register("statuses", StatusViewSet, basename="status")
router.register("orders", OrderViewSet, basename="order")
router.register("feedbacks", FeedbackViewSet, basename="feedback")
router.register("courier-analytics", CourierAnalyticsViewSet, basename="courier-analytics")

# 📌 Определяем маршруты
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),  # Включаем маршруты из роутера
    path("api/user-orders/<int:user_id>/", UserOrdersAPIView.as_view(), name="user-orders"),
    path("api/courier-analytics/<int:courier_id>/", CourierAnalyticsAPIView.as_view(), name="courier-analytics"),
]
