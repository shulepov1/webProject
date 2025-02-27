from django.shortcuts import render

from rest_framework import viewsets
from .models import User, TestNSI, TestResult
from .serializers import UserSerializer, TestNSISerializer, TestResultSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TestNSIViewSet(viewsets.ModelViewSet):
    queryset = TestNSI.objects.all()
    serializer_class = TestNSISerializer

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TestResult
from .serializers import TestResultSerializer

class TestResultCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TestResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
