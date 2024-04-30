from rest_framework import serializers
from .models import CustomUser
from .models import Product
from .models import Cart
from .models import Wishlist
from .models import Category



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role', 'first_name', 'last_name']  # Add more fields here
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            first_name=validated_data.get('first_name', ''),  # Get first_name from validated_data or default to empty string
            last_name=validated_data.get('last_name', ''),    # Get last_name from validated_data or default to empty string
            # date_of_birth=validated_data.get('date_of_birth', None)  # Get date_of_birth from validated_data or default to None
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)




class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']  # Add or modify fields as needed



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'rating', 'discount', 'comments' ]



class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'rating', 'discount', 'comments']



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product id']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity']


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

