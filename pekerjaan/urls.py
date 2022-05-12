from django.urls import path
from .views import create_pekerjaan, read_pekerjaan, update_pekerjaan

urlpatterns = [
	path('create/pekerjaan', create_pekerjaan, name='create_pekerjaan'),
	path('read/pekerjaan', read_pekerjaan, name='read_pekerjaan'),
	path('update/pekerjaan/<str:nama>', update_pekerjaan, name='update_pekerjaan'),
]