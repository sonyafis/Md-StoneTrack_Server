from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from track.views import *  # Убедитесь, что у вас есть все нужные представления

router = DefaultRouter()
router.register("statuses", StatusViewSet, basename="status")
router.register("orders", OrderViewSet, basename="order")
router.register("feedbacks", FeedbackViewSet, basename="feedback")
router.register("courier-analytics", CourierAnalyticsViewSet, basename="courier-analytics")
router.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Проверка API пути
    path('auth/', include('djoser.urls')),  # djoser API
    path('auth/', include('djoser.urls.jwt')),  # JWT эндпоинты
]
