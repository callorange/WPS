from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer


class UserCreate(APIView):
    """
    signup 했을때 유저 생성
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                json['password'] = ''
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthTokenView(APIView):
    """
    id/password에 따라 token을 return 해주는 view
    """

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']

            token, _ = Token.objects.get_or_create(user=user)
            json = UserSerializer(user).data
            print(json)
            json['token'] = token.key
            return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
