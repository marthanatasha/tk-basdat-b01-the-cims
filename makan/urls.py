from django.urls import path
from .views import *
app_name = 'makan'

urlpatterns = [
    path('read_makan_admin/', read_makan_admin, name='read_makan_admin'),
    path('read_makan_pemain/', read_makan_pemain, name='read_makan_pemain'),
    path('create_makan/', create_makan, name='create_makan'),
    path('create_makan/get_makanan/', get_makanan, name='get_makanan')
]