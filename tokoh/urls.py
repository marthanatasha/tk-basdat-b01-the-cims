from django.urls import path

from level.views import delete_level
from .views import read_tokoh_admin, read_tokoh_pemain, create_tokoh, detail_tokoh, update_tokoh
app_name = 'tokoh'

urlpatterns = [
	path('read_tokoh_admin/', read_tokoh_admin, name='read_tokoh_admin'),
	path('read_tokoh_pemain/', read_tokoh_pemain, name='read_tokoh_pemain'),
	path('create_tokoh/', create_tokoh, name='create_tokoh'),
	path('detail_tokoh/', detail_tokoh, name='detail_tokoh'),
	path('update_tokoh/<str:nama_tokoh>', update_tokoh, name='update_tokoh'),
]