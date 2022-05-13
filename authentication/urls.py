from django.urls import path
from .views import login, register_admin, register_pemain, homepage, logout, login_dan_register

urlpatterns = [
	path('', homepage, name='home'),
	path('login-dan-register', login_dan_register, name='login_dan_register'),
	path('login', login, name='login'),
	path('logout', logout, name='logout'),
	path('register/admin', register_admin, name='register_admin'),
	path('register/pemain', register_pemain, name='register_pemain'),
]