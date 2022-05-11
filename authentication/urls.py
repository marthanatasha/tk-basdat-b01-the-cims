from django.urls import path
from .views import login, register_admin, register_pemain

urlpatterns = [
	path('login', login, name='login'),
	path('register/admin', register_admin, name='register_admin'),
	path('register/pemain', register_pemain, name='register_pemain'),
]