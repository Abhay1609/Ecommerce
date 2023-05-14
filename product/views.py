from django.shortcuts import render
from .seralizers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Product,Category,Cart,ProductInCart
from django.http import Http404,HttpResponse
from rest_framework.generics import ListAPIView,CreateAPIView,ListCreateAPIView
from account.models import User
# Create your views here.
class LatestProductList(APIView):
    def get(self,request, format=None):
        product=Product.objects.all()[0:4]
        serializer=ProductSerializer(product,many=True)
        return Response(serializer.data)
# class LatestProductList(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = AddProductSerializer

class ProductDetail(APIView):
    def get_object(self,category_slug,product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug,product_slug,format=None):
        product=self.get_object(category_slug,product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self,category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist:
            raise Http404
    def get(self, request, category_slug,format=None):
        category=self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query=request.data.get('query','')
    if query:
        product=Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
        serializer=ProductSerializer(product,many=True)
        return Response(serializer.data)
    else:
        return Response({"products":[]})

class AddProduct(CreateAPIView):


    queryset = Product.objects.all()
    serializer_class = AddProductSerializer
class AddCart(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
class PlaceOrder(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
class ProducttoCart(CreateAPIView):
    queryset = ProductInCart.objects.all()
    serializer_class = ProductCartSerializer
@api_view(['GET'])
def viewcart(request):
    user=request.user
    usermodel=User.objects.all()
    if user in usermodel :
        cart=Cart.objects.get(user=request.user)
        cart_id=cart.cart_id
        # print(cart_id)
        product=ProductInCart.objects.filter(cart_id=cart_id)
        serializers=ProductCartSerializer(product,many=True)

        return Response(serializers.data)

    else:
        return Response('Login First')
