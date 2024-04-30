from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import Product, Comment
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializer import ProductSerializer, ProductDetailSerializer


# Create your views here.
class ProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        print(request.user.username)
        # 요청을 보낸 사용자의 정보를 사용하여 작성자 값을 설정합니다.
        request.data["author"] = request.user.id
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#########################카테고리, 테그, 좋아요 하는법 물어보자.


class ProductDetailView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_object(self, product_id):
        return get_object_or_404(Product, pk=product_id)
    
    def get(self, request, product_id):
        product = self.get_object(product_id)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, product_id):
        product = self.get_object(product_id)
        if product.author == request.user:
            serializer = ProductDetailSerializer(
                product, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Error: Please conform to the format", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Error: Another token id", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, product_id):
        product = self.get_object(product_id)
        if product.author == request.user:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Error: Another token id", status=status.HTTP_400_BAD_REQUEST)

