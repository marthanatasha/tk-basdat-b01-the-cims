from django.urls import path
from .views import create_menggunakan_barang, read_menggunakan_barang, get_barang

urlpatterns = [
	path('create/menggunakan-barang', create_menggunakan_barang, name='create_menggunakan_barang'),
	path('create/menggunakan-barang/get-barang', get_barang, name='get_barang'),
	path('read/menggunakan-barang', read_menggunakan_barang, name='read_menggunakan_barang'),
]