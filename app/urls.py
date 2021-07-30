from django.urls import path, include
from . import views

app_name = "app"

urlpatterns = [
    path('', views.readFile, name='index'),
    path('products', views.products, name='products'),
    path('pieChart', views.pieChart, name='pieChart'),
    path('barChart', views.barChart, name='barChart')
]
