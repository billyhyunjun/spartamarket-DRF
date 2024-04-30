from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken # 어떻게 하는거야....


class AccountAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 비밀번호를 해싱하여 설정
            password = request.data.get('password')
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(slfe, request):
        if request.auth:
            # 블랙리스트에 토큰 추가
            token = request.auth
            token.blacklist()

            # 로그아웃 처리 후 추가 작업 수행
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No token provided."}, status=status.HTTP_400_BAD_REQUEST)


class AccountUserAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, username):
        return get_object_or_404(User, username=username)

    def get(self, request, username):
        user = self.get_object(username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        user = self.get_object(username)
        if user == request.user:
            serializer = UserSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Error: Please conform to the format", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Error: Another token id", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        user = self.get_object(username)
        if user == request.user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("Error: Another token id", status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    # 현재 비밀번호 확인
    if not check_password(current_password, user.password):
        return Response("Error: Incorrect current password", status=status.HTTP_400_BAD_REQUEST)

    # 새로운 비밀번호와 확인용 비밀번호 일치 여부 확인
    if new_password != confirm_password:
        return Response("Error: New password and confirm password do not match", status=status.HTTP_400_BAD_REQUEST)

    # 새로운 비밀번호 설정
    user.set_password(new_password)
    user.save()

    return Response("Message: Password changed successfully!", status=status.HTTP_200_OK)
