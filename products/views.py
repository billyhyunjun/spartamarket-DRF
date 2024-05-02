from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import Product, Comment, Hashtag, Category
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializer import ProductSerializer, ProductDetailSerializer, CommentSerializer
from accounts.models import User
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination


class ProductsView(APIView):
    pagination_class = PageNumberPagination
    # 한 페이지에 보여줄 항목 수 설정
    pagination_class.page_size = 10
    
    # 상점 목록 보기
    def get(self, request):
        # 정렬 조건이 있다면 정렬해서 표기
        sort = request.data.get("sort")
        if sort:
            if sort == "like_users":
                products = Product.objects.annotate(
                    num_likes=Count(sort)).order_by("-num_likes")
            else:
                return Response({"Error": "Wrong sort tag"}, status=status.HTTP_400_BAD_REQUEST)
        # 정렬 조건이 없으면 모든 글 보여주기
        else:
            products = Product.objects.all()  # 전부 다 가져와
            
        # 페이지네이션 적용
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(products, request)
        
        serializer = ProductSerializer(result_page, many=True)  # 형식에 맞추어 데이터 생성
        return paginator.get_paginated_response(serializer.data)

    # 로그인 상태에서만 가능, 상점 게시글 생성

    @permission_classes([IsAuthenticated])
    def post(self, request):
        # 클라이언트에서 받아온 해시태그, 카테고리, 작성자아이디.
        categories = request.data.get("categories")
        hashtags = request.data.get("hashtags")
        request.data["author"] = request.user.id
        serializer = ProductSerializer(data=request.data)
        # 유효성 검사
        if serializer.is_valid(raise_exception=True):
            # 일단 해시태그가 없는 값으로 먼저 저장
            serializer.save()
            # 방금 저장했던 게시글 가져오기
            product = Product.objects.all().last()
            # 해시태그 하나씩 꺼내서 중복 검사하고 게시글에 저장
            if hashtags:
                for hashtag_data in hashtags:
                    hashtag_data['tag'] = hashtag_data['tag'].upper()
                    hashtag, _ = Hashtag.objects.get_or_create(
                        tag=hashtag_data['tag'])
                    product.hashtags.add(hashtag)
            if categories:
                # 카테고리도 마찬가지로 중복검사 및 저장
                for category_data in categories:
                    category, _ = Category.objects.get_or_create(
                        name=category_data['name'])
                    product.categories.add(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def search(request):
    key = request.data.get("key")
    value = request.data.get("value")
    if key == "author":
        user = User.objects.get(username=value)
        products = Product.objects.filter(author=user.id)
    elif key == "title":
        products = Product.objects.filter(title__icontains=value)
    elif key == "content":
        products = Product.objects.filter(content__icontains=value)
    elif key == "hashtags":  # 해시태그 검색
        products = Product.objects.filter(hashtags__tag=value)
    elif key == "categories":  # 해시태그 검색
        products = Product.objects.filter(categories__name=value)
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

        if "content" in request.data:
            request.data["author"] = request.user.id
            request.data["product"] = product.id
            serializer = CommentSerializer(data=request.data)
            # 유효성 검사
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"Message": "Make product comment successfully!"}, status=status.HTTP_200_OK)

        else:
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
        if product.author == request.user:  # 수정자와 작성자가 같은 지 확인
            # 새로운 내용이 들어온다면 기존 해시태그, 카테고리 삭제
            categories = request.data.get("categories")
            if categories:
                product.categories.clear()

            hashtags = request.data.get("hashtags")
            if hashtags:
                product.hashtags.clear()

            serializer = ProductDetailSerializer(
                product, data=request.data, partial=True)
            # 유효성 검사
            if serializer.is_valid(raise_exception=True):
                # 일단 해시태그가 없는 값으로 먼저 저장
                serializer.save()
                # 방금 저장했던 게시글 가져오기
                product = Product.objects.get(pk=product_id)
                # 해시태그 하나씩 꺼내서 중복 검사하고 게시글에 저장
                for hashtag_data in hashtags:
                    hashtag_data['tag'] = hashtag_data['tag'].upper()
                    hashtag, _ = Hashtag.objects.get_or_create(
                        tag=hashtag_data['tag'])
                    product.hashtags.add(hashtag)
                # 카테고리도 마찬가지로 중복검사 및 저장
                for category_data in categories:
                    category, _ = Category.objects.get_or_create(
                        name=category_data['name'])
                    product.categories.add(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:  # 수정자와 작성자가 다를 시 오류메세지
            return Response({"Error": "Another token id."}, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request, product_id):
        product = self.get_object(product_id)
        if product.author == request.user:  # 현재 아이디가 작성자가 같은 지 확인
            product.delete()
            return Response({"Message": "Comment delete successfully!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Error": "Another token id."}, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):

    permission_classes = [IsAuthenticated]

    def get_comment_odject(self, comment_id):
        return get_object_or_404(Comment, pk=comment_id)

    def put(self, request, comment_id):
        comment = self.get_comment_odject(comment_id)
        # 댓글 작성자 검사
        if comment.author == request.user:
            serializer = CommentSerializer(
                comment, data=request.data, partial=True)
            # 유효성 검사
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"Message": "Product comment update successfully!"}, status=status.HTTP_200_OK)
        else:  # 수정자와 작성자가 다를 시 오류메세지
            return Response({"Error": "Another token id."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = self.get_comment_odject(comment_id)
        if comment.author == request.user:
            comment.delete()
            return Response({"Message": "Comment delete successfully!"}, status=status.HTTP_204_NO_CONTENT)
        else:  # 수정자와 작성자가 다를 시 오류메세지
            return Response({"Error": "Another token id."}, status=status.HTTP_400_BAD_REQUEST)
