from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection, IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse, HttpResponse

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def read_menjalankan_misi_utama_admin(request):
    if request.session['role'] == 'pemain':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM MENJALANKAN_MISI_UTAMA GROUP BY USERNAME_PENGGUNA, NAMA_TOKOH, NAMA_MISI, STATUS""")
        tabel = dictfetchall(cursor)
    context = {'menjalankanmisiutama': tabel}
    return render(request, 'read_menjalankan_misi_utama.html', context)

def read_menjalankan_misi_utama_pemain(request):
    if request.session['role'] == 'admin':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM MENJALANKAN_MISI_UTAMA WHERE USERNAME_PENGGUNA = %s;", [request.session['username']])
        tabel = dictfetchall(cursor)
    context = {'menjalankanmisiutama': tabel}
    return render(request, 'read_menjalankan_misi_utama.html', context)