from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newbooking/', views.newbooking, name='newbooking'),
    path('newsearch/', views.newsearch, name='newsearch'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about')
]
