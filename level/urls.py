from django.urls import path
from .views import read_level, create_level, update_level
app_name = 'level'

urlpatterns = [
	path('create_level/', create_level, name='create_level'),
    path('read_level/', read_level, name='read_level'),
    path('update_level/<int:level>', update_level, name='update_level'),
]