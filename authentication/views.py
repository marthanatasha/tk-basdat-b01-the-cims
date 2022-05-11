from django.shortcuts import render
from django.db import connection

def	login(request):
  return render(request, "login.html")

def register_admin(request):
  return render(request, "register_admin.html")

def register_pemain(request):
  return render(request, "register_pemain.html")
