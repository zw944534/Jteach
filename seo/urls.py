'''
Created on 2021�~10��18��

@author: chu
'''
from django.conf.urls import include, url
from django.urls import path
from . import view


urlpatterns = [
    path('',view.index,name='index'),
    path('product/',view.product,name='product'),
    path('search/',view.searchProduct,name='productSearch'),
    path('social/',view.facebook,name='socialContent'),
    path('ig/',view.Ig,name='IgContent'),
    path('article/',view.ArticleView,name='article'),
    path('editTemplate/',view.editTemplate,name='editTemplate')
]