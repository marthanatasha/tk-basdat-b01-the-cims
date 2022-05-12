from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def read_tokoh_admin(request):
    if request.session['role'] == 'pemain':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM TOKOH")
        tabel = dictfetchall(cursor)
    context = {'semuatokoh': tabel}
    return render(request, 'read_tokoh_admin.html', context)

def read_tokoh_pemain(request):
    if request.session['role'] == 'admin':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM TOKOH WHERE USERNAME_PENGGUNA = %s;", [request.session['username']])
        tabel = dictfetchall(cursor)
    context = {'semuatokohpemain': tabel}
    return render(request, 'read_tokoh_pemain.html', context)    

def action_read_tokoh(request):
    if request.session['role'] == 'pemain':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute("SELECT NAMA, ID_MATA, ID_RAMBUT, ID_RUMAH, WARNA_KULIT, PEKERJAAN FROM TOKOH")
        tabel = dictfetchall(cursor)
    context = {'semuatokoh': tabel}
    return render(request, 'action.html', context)