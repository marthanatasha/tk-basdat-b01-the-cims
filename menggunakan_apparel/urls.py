from django.urls import path
from .views import get_apparel, read_menggunakan_apparel_pemain, create_menggunakan_apparel, read_menggunakan_apparel_admin, delete_menggunakan_apparel
app_name = 'menggunakan_apparel'

urlpatterns = [
	path('create_menggunakan_apparel/', create_menggunakan_apparel, name='create_menggunakan_apparel'),
    path('read_menggunakan_apparel_pemain/', read_menggunakan_apparel_pemain, name='read_menggunakan_apparel_pemain'),
    path('read_menggunakan_apparel_admin/', read_menggunakan_apparel_admin, name='read_menggunakan_apparel_admin'),
    path('create_menggunakan_apparel/get_apparel/', get_apparel, name='get_apparel'),
    path('delete_menggunakan_apparel/', delete_menggunakan_apparel, name='delete_menggunakan_apparel'),
]