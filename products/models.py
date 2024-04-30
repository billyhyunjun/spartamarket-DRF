from django.db import models
from django.conf import settings

# Create your models here.
class Hashtag(models.Model):
    tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    price = models.PositiveIntegerField()   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="image/", blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stores")
    
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_articles")
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name="products_hashtag")
    categories = models.ManyToManyField(Category, blank=True, related_name="products_categorie")
    
    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)