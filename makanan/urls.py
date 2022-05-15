from django.urls import path
from .views import *
app_name = 'makanan'

urlpatterns = [
    path('read_makanan_admin/', read_makanan_admin, name='read_makanan_admin'),
    path('read_makanan_pemain/', read_makanan_pemain, name='read_makanan_pemain'),
    path('create_makanan/', create_makanan, name='create_makanan'),
    path('update_makanan/<str:nama_makanan>', update_makanan, name='update_makanan'),
    path('delete_makanan/>', delete_makanan, name='delete_makanan'),
]