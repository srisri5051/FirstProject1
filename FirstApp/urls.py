from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register_user, name='register'),

    path('login/', views.login, name='login'),

    path('change-password/', views.change_password, name='change_password'),

    path('profile/', views.user_profile, name='profile'),

    path('add_product/', views.add_product, name='add-product'),

    path('product_list/', views.product_list, name= 'product-list'),
    path('update_products/<int:pk>/', views.update_product, name= 'update-product'),

    path('products/<int:pk>/delete/', views.delete_product, name='delete-product'),

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name= 'add-to-cart'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name= 'add-to-whishlist'),
    

    path('cart_list/', views.cart_list, name='cart_list'),
    path('wishlist_items/', views.wishlist_items, name='wishlist_items'),

    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-from-wishlist/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('categories/create/', views.create_category, name='create_category'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    





]
