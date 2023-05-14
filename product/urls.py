from django.urls import path,include
from product import views

urlpatterns =[
    path('latest-product/',views.LatestProductList.as_view()),
    path('search/',views.search),
    path('incart/',views.viewcart),
    path('db/<slug:category_slug>/<slug:product_slug>/',views.ProductDetail.as_view()),
    path('db/<slug:category_slug>/',views.CategoryDetail.as_view()),
    path('add/',views.AddProduct.as_view()),
    path('cart/',views.AddCart.as_view()),
    path('order/',views.PlaceOrder.as_view()),
    path('addtocart/',views.ProducttoCart.as_view()),
]
