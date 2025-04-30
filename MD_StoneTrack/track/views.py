from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet

from .models import Status, Order, Feedback, CourierAnalytics
from .permissons import IsAdmin, IsCourier, IsClient
from .serializers import StatusSerializer, OrderSerializer, FeedbackSerializer, CourierAnalyticsSerializer, OrderUpdateSerializer

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
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_client', 'id_courier']  # Фильтрация по клиенту и курьеру

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            return [IsAuthenticated()]  # Запрещаем доступ анонимным пользователям

        if self.action in ['list', 'retrieve']:
            if self.request.user.type_user == 'courier':
                return [IsAuthenticated(), IsCourier()]
            elif self.request.user.type_user == 'client':
                return [IsAuthenticated(), IsClient()]
        elif self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]

        return super().get_permissions()

    def get_queryset(self):
        queryset = Order.objects.all()

        if self.request.user.type_user == 'client':
            return queryset.filter(id_client=self.request.user)

        if self.request.user.type_user == 'courier':
            return queryset.filter(id_courier=self.request.user)

        return queryset  # Администраторы видят все заказы

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_super_user', 'user_type']

class CourierAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = CourierAnalytics.objects.all()
    serializer_class = CourierAnalyticsSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
