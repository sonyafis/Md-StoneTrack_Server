from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import SuperUser, Status, Order, Feedback, CourierAnalytics

User = get_user_model()

class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperUser
        fields = ['id_super_user', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'type_user']

class RegisterSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'password', 'password2', 'type_user')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        if 'type_user' not in validated_data:
            validated_data['type_user'] = 'client'  # По умолчанию

        print("✅ Сохраняем данные пользователя:", validated_data)  # Для отладки

        return User.objects.create_user(**validated_data)





class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    id_status = StatusSerializer(read_only=True)
    id_client = SuperUserSerializer(read_only=True)  # Сериализуем пользователя как "client"
    id_courier = SuperUserSerializer(read_only=True)  # Сериализуем пользователя как "courier"

    class Meta:
        model = Order
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    id_super_user = SuperUserSerializer(read_only=True)  # Показываем информацию о пользователе
    type_user = serializers.CharField(source="id_super_user.type_user", read_only=True)  # Отображаем тип пользователя

    class Meta:
        model = Feedback
        fields = "__all__"



class CourierAnalyticsSerializer(serializers.ModelSerializer):
    id_courier = SuperUserSerializer(read_only=True)  # Сериализуем курьера

    class Meta:
        model = CourierAnalytics
        fields = "__all__"

