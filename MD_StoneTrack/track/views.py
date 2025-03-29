from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Status, Order, Feedback, CourierAnalytics
from .permissons import IsAdmin, IsCourier, IsClient
from .serializers import StatusSerializer, OrderSerializer, FeedbackSerializer, CourierAnalyticsSerializer

User = get_user_model()

class CustomUserViewSet(UserViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type_user']

    def get_queryset(self):
        print("Request query params:", self.request.query_params)  # Для отладки
        queryset = User.objects.all()
        type_user = self.request.query_params.get("type_user")

        if type_user:
            queryset = queryset.filter(type_user=type_user)

        return queryset


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            if self.request.user.type_user == 'courier':
                return [IsAuthenticated(), IsCourier()]
            elif self.request.user.type_user == 'client':
                return [IsAuthenticated(), IsClient()]
        elif self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class CourierAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = CourierAnalytics.objects.all()
    serializer_class = CourierAnalyticsSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
