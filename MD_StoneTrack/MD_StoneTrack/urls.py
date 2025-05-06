from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from track.views import *

router = DefaultRouter()
router.register("statuses", StatusViewSet, basename="status")
router.register("orders", OrderViewSet, basename="order")
router.register("feedbacks", FeedbackViewSet, basename="feedback")
router.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/users/reset_password_confirm/<uid>/<token>/',
        TemplateView.as_view(template_name='password_reset_confirm.html')),
    path('auth/users/reset_password_confirm/',
        UserViewSet.as_view({'post': 'reset_password_confirm'})),
]
