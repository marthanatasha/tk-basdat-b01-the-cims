from django.urls import path
from .views import login, register_admin, register_pemain, homepage, logout

urlpatterns = [
	path('', homepage, name='home'),
	path('login', login, name='login'),
	path('logout', logout, name='logout'),
	path('register/admin', register_admin, name='register_admin'),
	path('register/pemain', register_pemain, name='register_pemain'),
]