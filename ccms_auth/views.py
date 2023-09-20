from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ccms_auth.models import User
from ccms_auth.serializers import RegistrationSerializer
from django.contrib.auth.hashers import check_password


class RegistrationView(APIView):
    """
    #* 계정 신청 API
    """
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입이 완료되었습니다.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    #* 로그인 API
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()

        if not user:
            return Response({'message': '존재하지 않는 사용자입니다.'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_locked:
            return Response({'message': '관리자에게 연락하세요.'}, status=status.HTTP_403_FORBIDDEN)

        if not check_password(password, user.password):
            user.login_failures += 1
            user.last_login_attempt = timezone.now()
            user.save()

            if user.login_failures >= 5:
                user.is_locked = True
                user.save()
                return Response({'message': '로그인을 5회 실패하여 로그인을 할 수 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'message': '로그인 실패'}, status=status.HTTP_401_UNAUTHORIZED)

        # 로그인 성공
        user.login_failures = 0
        user.last_login_attempt = None
        user.save()
        return Response({'message': '로그인 성공'})


class PasswordChangeView(APIView):
    def get(self, request):
        return Response({'message': '비밀번호 변경 페이지로 이동'})
