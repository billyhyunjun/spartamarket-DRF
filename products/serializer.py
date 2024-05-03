from rest_framework import serializers
from .models import Product, Comment, Hashtag, Category
from accounts.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("product")
        ret['author'] = UserSerializer(instance.author).data
        return ret


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('tag',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    like_users = UserSerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ("image",)

    def to_representation(self, value):
        ret = super().to_representation(value)
        ret['author'] = UserSerializer(value.author).data
        return ret


class ProductDetailSerializer(ProductSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(
        source="comments.count", read_only=True)
