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

@csrf_exempt
def create_misi_utama(request):
    # if request.session['role'] == 'pemain':
    #     messages.add_message(request, messages.WARNING, f"Hanya admin yang dapat menambahkan level")
    #     return redirect("/")
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO MISI VALUES 
                    ('{request.POST['nama_misi']}',
                    '{request.POST['efek_energi']}',
                    '{request.POST['efek_hub_sosial']}',
                    '{request.POST['efek_kelaparan']}',
                    '{request.POST['syarat_energi']}',
                    '{request.POST['syarat_hub_sosial']}',
                    '{request.POST['syarat_kelaparan']}',
                    '{request.POST['completion_time']}',
                    '{request.POST['reward_koin']}',
                    '{request.POST['reward_xp']}',
                    '{request.POST['deskripsi']}')
                """)
                cursor.execute(f"""
                    INSERT INTO MISI_UTAMA VALUES 
                    ('{request.POST['nama_misi']}')""")
                return redirect("misi_utama:read_misi_utama_admin")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data misi dengan nama {request.POST['nama_misi']} sudah terdaftar")


    context = {}
    return render(request, "create_misi_utama.html", context)
