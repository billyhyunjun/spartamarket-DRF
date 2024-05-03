from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductsView.as_view(), name="products"),
    path("comment/<int:comment_id>/", views.CommentView.as_view(), name="comments"),
    path("search/", views.search, name="search"),
    path("<int:product_id>/", views.ProductDetailView.as_view(), name="detail")
]
