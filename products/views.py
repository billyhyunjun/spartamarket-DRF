from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import Product, Comment, Hashtag, Category
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializer import ProductSerializer, ProductDetailSerializer
from accounts.models import User


class ProductsView(APIView):
    # 상점 목록 보기
    def get(self, request):
        products = Product.objects.all()  # 전부 다 가져와
        serializer = ProductSerializer(products, many=True)  # 형식에 맞추어 데이터 생성
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # 로그인 상태에서만 가능, 상점 게시글 생성
    @permission_classes([IsAuthenticated])
    def post(self, request):
        # 요청을 보낸 사용자의 정보를 사용하여 작성자 값을 설정합니다.
        categories = request.data.get("categories")
        hashtags = request.data.get("hashtags")
        request.data["author"] = request.user.id
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            product = Product.objects.all().last()
            for hashtag_data in hashtags:
                hashtag, _ = Hashtag.objects.get_or_create(tag=hashtag_data['tag'])
                product.hashtags.add(hashtag)
            
            for category_data in categories:
                category, _ = Category.objects.get_or_create(name=category_data['name'])
                product.categories.add(category)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search(request):
    key = request.data.get("key")
    value = request.data.get("value")
    if key == "author":
        user = User.objects.get(username=value)
        products = Product.objects.filter(author=user.id)
    elif key == "title":
        products = Product.objects.filter(title=value)
    elif key == "content":
        products = Product.objects.filter(content=value)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetailView(APIView):
    # 로그인 상태 확인
    permission_classes = [IsAuthenticated]

    # 게시물 product_id 로 글 가져오기
    def get_object(self, product_id):
        return get_object_or_404(Product, pk=product_id)

    # 게시글 확인
    def get(self, request, product_id):
        product = self.get_object(product_id)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 좋아요
    def post(self, request, product_id):
        product = self.get_object(product_id)
        if product.author != request.user:
            if request.user in product.like_users.all():
                # 이미 좋아요 중인 경우 좋아요 취소
                product.like_users.remove(request.user)
                return Response({"Message": "Product dislike successfully!"}, status=status.HTTP_200_OK)
            else:
                # 아직 좋아요 중이 아닌 경우 팔로우
                product.like_users.add(request.user)
                return Response({"Message": "Product like successfully!"}, status=status.HTTP_200_OK)
        else:
            # 로그인 정보가 같다면 에러
            return Response({"Error": "Same token id."}, status=status.HTTP_400_BAD_REQUEST)
    
    # 게시글 수정
    def put(self, request, product_id):
        product = self.get_object(product_id)
        if product.author == request.user: # 수정자와 작성자가 같은 지 확인
            serializer = ProductDetailSerializer(
                product, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else: # 수정자와 작성자가 다를 시 오류메세지
            return Response("Error: Another token id", status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request, product_id):
        product = self.get_object(product_id)
        if product.author == request.user: # 현재 아이디가 작성자가 같은 지 확인
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Error: Another token id", status=status.HTTP_400_BAD_REQUEST)
