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

@csrf_exempt
def create_menjalankan_misi_utama(request):
    # if request.session['role'] == 'admin':
    #     messages.add_message(request, messages.WARNING, f"Hanya pemain yang dapat menambahkan menggunakan_apparel")
    #     return redirect("/")
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO MENJALANKAN_MISI_UTAMA VALUES 
                    ('{request.session['username']}',
                    '{request.POST['nama_tokoh']}',
                    '{request.POST['nama_misiutama']}',
                     'in progress')
                """)

                return redirect("menjalankan_misi_utama:read_menjalankan_misi_utama_pemain")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data menjalankan misi dengan nama {request.POST['nama_misi']} sudah terdaftar")

    with connection.cursor() as cursor:
        cursor.execute("SELECT nama FROM tokoh WHERE username_pengguna='{}'".format(request.session['username']))
        tokoh = cursor.fetchall()
        cursor.execute ("SELECT nama_misi FROM MISI_UTAMA")
        misi = dictfetchall(cursor)

    return render(request, "create_menjalankan_misi_utama.html", {"tokoh":tokoh, "misi":misi})

@csrf_exempt
def get_misi_utama(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("SELECT nama_misi FROM MISI_UTAMA")
            misiutama = cursor.fetchall()
        return JsonResponse({'misiutama': misiutama})
    return HttpResponse("<h1>Method not allowed</h1>", status=405)


def update_menjalankan_misi_utama(request, nama_tokoh, nama_misi):

    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE MENJALANKAN_MISI_UTAMA 
                    SET status='{request.POST['update_status']}'
                    WHERE nama_tokoh = '{nama_tokoh}'
                    AND nama_misi = '{nama_misi}'
                """)
                return redirect("menjalankan_misi_utama:read_menjalankan_misi_utama_pemain")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data Menjalankan misi utama tersebut sudah terdaftar")

    context = {"nama_tokoh":nama_tokoh, "nama_misi":nama_misi}
    return render(request, "update_menjalankan_misi_utama.html", context)
