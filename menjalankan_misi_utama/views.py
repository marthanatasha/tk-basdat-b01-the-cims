from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection, IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from collections import namedtuple

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def namedtuplefetchall(cursor):
    """Return all rows from a cursor as a namedtuple"""
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

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
        cursor.execute("SELECT * , CASE WHEN STATUS = 'selesai' THEN false else true END AS UPDATABLE FROM MENJALANKAN_MISI_UTAMA WHERE USERNAME_PENGGUNA = %s;", [request.session['username']])
        tabel = dictfetchall(cursor)
    context = {'menjalankanmisiutama': tabel}
    return render(request, 'read_menjalankan_misi_utama.html', context)

@csrf_exempt
def create_menjalankan_misi_utama(request):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                nama_tokoh = request.POST['nama_tokoh']
                nama_misiutama = request.POST['nama_misiutama']
                syarat_e = ''
                syarat_hubsos =''
                syarat_k = ''
                tingkat_e = ''
                tingkat_hubsos = ''
                tingkat_k = ''

                cursor.execute(f"""select * from misi where nama = '{nama_misiutama}'""")
                misi = namedtuplefetchall(cursor)
                for row in misi:
                    syarat_e = row[4]
                    syarat_hubsos = row[5]
                    syarat_k = row[6]
                    break
                cursor.execute(f"""select * from tokoh where nama = '{nama_tokoh}'""")
                misi = namedtuplefetchall(cursor)
                for row in misi:
                    tingkat_e = row[5]
                    tingkat_hubsos = row[7]
                    tingkat_k = row[6]
                    break

                if (int(tingkat_e) >= int(syarat_e) & int(tingkat_hubsos) >= int(syarat_hubsos) & int(tingkat_k) <= int(syarat_k)):
                    cursor.execute(f"""INSERT INTO MENJALANKAN_MISI_UTAMA VALUES 
                    ('{request.session['username']}',
                    '{nama_tokoh}',
                    '{nama_misiutama}',
                     'in progress')
                    """)
                    return redirect("menjalankan_misi_utama:read_menjalankan_misi_utama_pemain")
                
                else:
                    messages.add_message(request, messages.WARNING, "Syarat misi utama tidak mencukupi sehingga misi utama tidak dapat dijalankan")
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT nama FROM tokoh WHERE username_pengguna='{}'".format(request.session['username']))
                        tokoh = cursor.fetchall()
                        cursor.execute ("SELECT nama_misi FROM MISI_UTAMA")
                        misi = dictfetchall(cursor)

                    return render(request, "create_menjalankan_misi_utama.html", {"tokoh":tokoh, "misi":misi})
                    #return redirect("menjalankan_misi_utama:create_menjalankan_misi_utama.html")
                    #return redirect("menjalankan_misi_utama:read_menjalankan_misi_utama_pemain")
                # return redirect("menjalankan_misi_utama:read_menjalankan_misi_utama_pemain")
        except:
            messages.add_message(request, messages.WARNING, "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu")

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
        except:
            messages.add_message(request, messages.WARNING, "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu")

    context = {"nama_tokoh":nama_tokoh, "nama_misi":nama_misi}
    return render(request, "update_menjalankan_misi_utama.html", context)
