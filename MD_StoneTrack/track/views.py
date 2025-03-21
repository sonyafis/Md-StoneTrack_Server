from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import SuperUser, Status, Order, Feedback, CourierAnalytics
from .serializers import SuperUserSerializer, StatusSerializer, OrderSerializer, FeedbackSerializer, CourierAnalyticsSerializer

# 🚀 CRUD для SuperUser
class SuperUserViewSet(viewsets.ModelViewSet):
    queryset = SuperUser.objects.all()
    serializer_class = SuperUserSerializer

# 🚀 CRUD для Status
class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

# 🚀 CRUD для Order
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# 🚀 CRUD для Feedback
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

# 🚀 CRUD для CourierAnalytics
class CourierAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = CourierAnalytics.objects.all()
    serializer_class = CourierAnalyticsSerializer


# 🔥 Дополнительное API для получения заказов конкретного пользователя
class UserOrdersAPIView(APIView):
    def get(self, request, user_id):
        orders = Order.objects.filter(id_client__id_super_user=user_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 🔥 API для аналитики конкретного курьера
class CourierAnalyticsAPIView(APIView):
    def get(self, request, courier_id):
        try:
            analytics = CourierAnalytics.objects.get(id_courier__id_super_user=courier_id)
            serializer = CourierAnalyticsSerializer(analytics)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CourierAnalytics.DoesNotExist:
            return Response({"error": "Аналитика не найдена"}, status=status.HTTP_404_NOT_FOUND)
