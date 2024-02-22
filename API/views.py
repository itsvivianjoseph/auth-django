from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerialzer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from django.contrib.auth import authenticate

@api_view(['POST'])
def login(request):
    provided_token = request.data.get('token')
    user_data = request.data.get('user')

    if provided_token and user_data:
        try:
            token = Token.objects.get(key=provided_token)
            user = authenticate(username=user_data['username'], password=user_data['password'])

            if user and user == token.user:
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials or token"}, status=status.HTTP_401_UNAUTHORIZED)

        except Token.DoesNotExist:
            return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({"message": "Token and user data required"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup(request):
    serialzer = UserSerialzer(data=request.data)
    if serialzer.is_valid():
        serialzer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serialzer.data}, status=status.HTTP_201_CREATED)
    return Response(serialzer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def test_token(request):
    provided_token = request.data.get('token')
    
    if provided_token:
        try:
            token = Token.objects.get(key=provided_token)
            # print(f"Request User: {request.user}")
            # print(f"Token User: {token.user}")
            # print(type(request.data.get('user').get('username')))
            # print(type(token.user))
            # serialzer = UserSerialzer(data=request.data)
            # print()
            if str(token.user) == request.data.get('user').get('username'):
                return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Token does not match authenticated user"}, status=status.HTTP_401_UNAUTHORIZED)

        except Token.DoesNotExist:
            return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)