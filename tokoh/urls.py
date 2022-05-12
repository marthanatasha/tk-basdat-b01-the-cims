from django.urls import path
from .views import read_tokoh_admin, read_tokoh_pemain, create_tokoh

urlpatterns = [
	path('read_tokoh_admin/', read_tokoh_admin, name='read_tokoh_admin'),
	path('read_tokoh_pemain/', read_tokoh_pemain, name='read_tokoh_pemain'),
	path('create_tokoh/', create_tokoh, name='create_tokoh'),
]