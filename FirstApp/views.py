from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserUpdateSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .models import CustomUser
from .serializers import ProductSerializer

from .models import Product
from .serializers import ProductUpdateSerializer

from .models import Product, Cart, Wishlist

from .serializers import CartSerializer

from .serializers import WishlistSerializer

from .models import Category
from .serializers import CategorySerializer


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message':"successfully logged in"
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




from rest_framework.authtoken.models import Token
from .serializers import ChangePasswordSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)

    if serializer.is_valid():
        # Check old password
        if not user.check_password(serializer.data.get('old_password')):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(serializer.data.get('new_password'))
        user.save()
        # Update token if it exists
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({'message': 'Password changed successfully', 'token': token.key}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    if request.user.role == CustomUser.Role.DEALER:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dealer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You are not authorized to add products.'}, status=status.HTTP_403_FORBIDDEN)





@api_view(['GET'])
def product_list(request):
    """
    List all products.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    """
    Update a product.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user.role == CustomUser.Role.DEALER and request.user == product.dealer:
        serializer = ProductUpdateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You are not authorized to update this product.'}, status=status.HTTP_403_FORBIDDEN)




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    """
    Delete a product.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user.role == CustomUser.Role.DEALER and request.user == product.dealer:
        product.delete()
        return Response({'product delete successfully'},status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'You are not authorized to delete this product.'}, status=status.HTTP_403_FORBIDDEN)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_id):  # Ensure the view accepts product_id
    if request.method == 'POST':
        user = request.user
        quantity = request.data.get('quantity', 1)  # Default quantity is 1
        
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, product_id):  
    if request.method == 'POST':
        user = request.user
        
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)
        if not created:
            
            wishlist_item.save()
            return Response({'message': 'Product already exists in wishlist'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Product added to wishlist successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, wishlist_item_id):
    try:
        wishlist_item = Wishlist.objects.get(pk=wishlist_item_id)
        if wishlist_item.user != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        wishlist_item.delete()
        return Response({'message': 'Item removed from wishlist successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Wishlist.DoesNotExist:
        return Response({'error': 'Wishlist item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_list(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wishlist_items(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    serializer = WishlistSerializer(wishlist_items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = Cart.objects.get(pk=cart_item_id)
        if cart_item.user != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        cart_item.delete()
        return Response({'message': 'Item removed from cart successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, wishlist_item_id):
    try:
        wishlist_item = Wishlist.objects.get(pk=wishlist_item_id)
        if wishlist_item.user != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        wishlist_item.delete()
        return Response({'message': 'Item removed from wishlist successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Wishlist.DoesNotExist:
        return Response({'error': 'Wishlist item not found'}, status=status.HTTP_404_NOT_FOUND)
    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        return create_category(request)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Category delete successfully'}, status=status.HTTP_204_NO_CONTENT)

