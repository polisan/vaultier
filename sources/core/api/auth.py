from django.contrib.auth import authenticate, login, logout
from rest_framework.fields import EmailField, CharField
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from core.api import ApiException
from core.api.user import UserSerializer
from rest_framework.response import Response
from rest_framework import serializers


class UserView(CreateModelMixin, UpdateModelMixin, GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request):
        return self.status(request)

    def status(self, request):
        user = request.user
        if (user.is_authenticated()):
            serialized = UserSerializer(user).data;
            return Response(serialized)
        else:
            return Response({'detail': 'Anonymous user'}, status=HTTP_403_FORBIDDEN)


class AuthSerializer(serializers.Serializer):
    email = EmailField(required=True)
    signature = CharField(required=True)


class AuthView(APIView):
    def auth(self, request):
        serializer = AuthSerializer(data=request.DATA)
        if serializer.is_valid():
            try:
                user = authenticate(email=serializer.data.get('email'),
                                    signature=serializer.data.get('signature'))
                if user:
                    login(request, user)
                    serialized = UserSerializer(user).data;
                    return Response(serialized)
                else:
                    return Response({'result': False})
            except Exception as e:
                raise ApiException(exception=e)

        raise ApiException(detail=serializer.errors)

    def post(self, request):
        return self.auth(request)


class LogoutView(APIView):
    def logout(self, request):
        try:
            logout(request)
            response = Response({'result': True})
            response.delete_cookie('sessionid', '/', '.')
            return response
        except Exception as e:
            raise ApiException(exception=e)

    def post(self, request):
        return self.logout(request)

