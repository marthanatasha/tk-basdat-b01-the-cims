from django.urls import path
from .views import read_tokoh_admin, read_tokoh_pemain

urlpatterns = [
	path('read_tokoh_admin/', read_tokoh_admin, name='read_tokoh_admin'),
	path('read_tokoh_pemain/', read_tokoh_pemain, name='read_tokoh_pemain'),
]