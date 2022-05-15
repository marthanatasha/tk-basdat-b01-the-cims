from django.urls import path
from .views import *
app_name = 'menjalankan_misi_utama'

urlpatterns = [
    path('read_menjalankan_misi_utama_admin/', read_menjalankan_misi_utama_admin, name='read_menjalankan_misi_utama_admin'),
    path('read_menjalankan_misi_utama_pemain/', read_menjalankan_misi_utama_pemain, name='read_menjalankan_misi_utama_pemain'),
    path('create_menjalankan_misi_utama/', create_menjalankan_misi_utama, name='create_menjalankan_misi_utama'),
    path('create_menjalankan_misi_utama/get_misi_utama/', get_misi_utama, name='get_misi_utama'),
    path('update_menjalankan_misi_utama/<str:username_pemain>/<str:nama_tokoh>/<str:nama_misi_utama>', update_menjalankan_misi_utama, name='update_menjalankan_misi_utama'),
]