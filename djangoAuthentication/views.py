from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import get_object_or_404


@api_view(['POST'])
def login(request):
    user = get_object_or_404(UserProfile, username=request.data['username'])

    if "load_count" in request.session:
        count = request.session["load_count"]
    else:
        count = 0

    count += 1
    request.session["load_count"] = count
    print(f"count: {count}")
    if count >= 5:
        print(f"count: {count}")
        user.is_active = False
        user.save()
        return Response({"detail": "Account locked"}, status=status.HTTP_403_FORBIDDEN)
    if user.check_password(request.data['password']):
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        return Response({"token": token.key, "user": serializer.data})
    else:
        return Response({"detail": "Wrong username or password"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():  # 유효성 검사
        serializer.save()  # 저장
        user = UserProfile.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))
