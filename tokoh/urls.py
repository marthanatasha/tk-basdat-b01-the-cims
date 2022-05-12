from django.urls import path
from .views import read_tokoh

urlpatterns = [
	path('read_tokoh/', read_tokoh, name='read_tokoh'),
]