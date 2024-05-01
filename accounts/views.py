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
from rest_framework_simplejwt.tokens import RefreshToken


class AccountAPI(APIView):
    # 회원가입
    def post(self, request):
        if request.data["username"] not in ["login","password","refresh","logout"]:
            serializer = UserSerializer(data=request.data)  # 유저 폼에 맞추어 데이터 넣기
            if serializer.is_valid(raise_exception=True):  # 유효성 검사
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error": "Can't use this username."}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    # 로그인상태
    permission_classes = [IsAuthenticated]

    # 로그아웃 처리
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            RefreshToken(refresh_token).blacklist()
            # 클라이언트의 쿠기 삭제
            response = Response({
                "message": "Logout success"
                }, status=status.HTTP_202_ACCEPTED)
            response.delete_cookie("accessToken")
            response.delete_cookie("refreshToken")
            return response
        except Exception as e:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)

        


class AccountUserAPI(APIView):
    # 로그인상태
    permission_classes = [IsAuthenticated]

    # db에서 username 자료 가져오기
    def get_object(self, username):
        return get_object_or_404(User, username=username)

    # 유저 프로필 확인
    def get(self, request, username):
        user = self.get_object(username)  # username에 맞는 데이터 가져오기
        serializer = UserSerializer(user)  # serializer 형식에 맞추어서 데이터 생성
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 팔로잉
    def post(self, request, username):
        user = self.get_object(username)
        if user != request.user:
            if user in request.user.following.all():
                # 이미 팔로우 중인 경우 팔로우 취소
                request.user.following.remove(user)
                return Response({"Message": "User unfollowed successfully!"}, status=status.HTTP_200_OK)
            else:
                # 아직 팔로우 중이 아닌 경우 팔로우
                request.user.following.add(user)
                return Response({"Message": "User followed successfully!"}, status=status.HTTP_200_OK)
        else:
            # 로그인 정보가 같다면 에러
            return Response({"Error": "Same token id."}, status=status.HTTP_400_BAD_REQUEST)

    # 유저 프로필 수정
    def put(self, request, username):
        user = self.get_object(username)
        if user == request.user:  # 현재 수정할려는 username의 정보와 내 로그인 정보가 같은지
            # user 정보에 내가 입력한 데이터 request.data의 값을 넣고 공란은 기존의 값으로
            serializer = UserSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):  # 유효성 틀리면 알아서 에러 메세지 나옴
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # 로그인 정보가 다르다면 에러
            return Response({"Error": "Another token id."}, status=status.HTTP_400_BAD_REQUEST)

    # 회원 탈퇴
    def delete(self, request, username):
        user = self.get_object(username)
        if user == request.user:  # 현재 로그인아이디랑 같은지
            user.delete()
            return Response({"Message": "User account delete successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"Error": "Another token id."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])  # put입력만 받기
@permission_classes([IsAuthenticated])  # 지금 로그인 중인지
def password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    # 현재 비밀번호 확인
    if not check_password(current_password, user.password):
        return Response({"Error": "Incorrect current password"}, status=status.HTTP_400_BAD_REQUEST)

    # 새로운 비밀번호와 기존 비밀번호 확인
    if new_password == current_password:
        return Response({"Error": "New password and current_password match"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 새로운 비밀번호와 확인용 비밀번호 일치 여부 확인
    if new_password != confirm_password:
        return Response({"Error": "New password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)

    # 새로운 비밀번호 설정
    user.set_password(new_password)
    user.save()

    return Response({"Message": "Password changed successfully!"}, status=status.HTTP_200_OK)
