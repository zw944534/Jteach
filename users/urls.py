'''
Created on 2022年2月13日

@author: chu
'''
from django.urls import path
from .views import home, profile, RegisterView,permissionDeniedView,product,productArticle

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('mem_product/',product,name='product-form'),
    path(
           'permissionDenied/',permissionDeniedView,name='user_permissions'
    ),
    path('product_article/',productArticle,name='product_article')
]