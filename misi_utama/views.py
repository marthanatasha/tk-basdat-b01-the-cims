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

def read_misi_utama_admin(request):
    if request.session['role'] == 'pemain':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT NAMA
         FROM MISI M, MISI_UTAMA MU
         WHERE M.NAMA = MU.NAMA_MISI""")
        tabel = dictfetchall(cursor)
    context = {'listmisiutama': tabel}
    return render(request, 'read_misi_utama.html', context)

def read_misi_utama_pemain(request):
    if request.session['role'] == 'admin':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT NAMA
         FROM MISI M, MISI_UTAMA MU
         WHERE M.NAMA = MU.NAMA_MISI""")
        tabel = dictfetchall(cursor)
    context = {'listmisiutama': tabel}
    return render(request, 'read_misi_utama.html', context)


# def detail_misi(request):
#     with connection.cursor() as cursor:
#         cursor.execute(f"""SELECT *
#         FROM MISI M, MISI_UTAMA MU
#         WHERE M.NAMA = MU.NAMA_MISI""")
#         tabel = dictfetchall(cursor)
#     context = {'detailmisi': tabel}
#     return render(request, 'detail.html', context)

def detail_misi(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT * FROM MISI WHERE NAMA='{request.POST['nama_misi']}'""")
            tabel = dictfetchall(cursor)
        context = {'detailmisi': tabel}
        return render(request, 'detail.html', context)
