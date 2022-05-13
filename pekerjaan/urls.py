from django.urls import path
from .views import create_pekerjaan, read_pekerjaan, update_pekerjaan, create_bekerja, read_bekerja

urlpatterns = [
	path('create/pekerjaan', create_pekerjaan, name='create_pekerjaan'),
	path('read/pekerjaan', read_pekerjaan, name='read_pekerjaan'),
	path('update/pekerjaan/<str:nama>', update_pekerjaan, name='update_pekerjaan'),
	path('create/bekerja', create_bekerja, name='create_bekerja'),
	path('read/bekerja', read_bekerja, name='read_bekerja'),
]