from rest_framework import serializers
from .models import User, TestNSI, TestResult
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Поле для ввода пароля (не сохраняется в БД)
    class Meta:
        model = User
        fields = ['username', 'password', 'age', 'education', 'speciality', 'residence', 'height', 'weight', 'lead_hand', 'diseases', 'smoking', 'alcohol', 'sport', 'insomnia', 'current_health', 'gaming']
        

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Создаём пользователя
        user = User(**validated_data)
        # Хэшируем пароль и сохраняем его
        user.password_hash= make_password(password)
        user.save()
        return user

class TestNSISerializer(serializers.ModelSerializer):
    class Meta:
        model = TestNSI
        fields = '__all__'

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()