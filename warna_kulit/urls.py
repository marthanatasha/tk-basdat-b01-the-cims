from django.urls import path
from .views import read_warna_kulit, create_warna_kulit
app_name = 'warna_kulit'

urlpatterns = [
	path('create_warna_kulit/', create_warna_kulit, name='create_warna_kulit'),
    path('read_warna_kulit/', read_warna_kulit, name='read_warna_kulit'),
]