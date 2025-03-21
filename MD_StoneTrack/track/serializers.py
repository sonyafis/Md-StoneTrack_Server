from rest_framework import serializers
from .models import SuperUser, Status, Order, Feedback, CourierAnalytics

class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperUser
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    id_status = StatusSerializer(read_only=True)
    id_client = SuperUserSerializer(read_only=True)
    id_courier = SuperUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    id_super_user = SuperUserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = "__all__"


class CourierAnalyticsSerializer(serializers.ModelSerializer):
    id_courier = SuperUserSerializer(read_only=True)

    class Meta:
        model = CourierAnalytics
        fields = "__all__"
