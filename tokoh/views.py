from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection, IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT NAMA, ID_MATA, ID_RAMBUT, ID_RUMAH, WARNA_KULIT, PEKERJAAN FROM TOKOH 
                        WHERE""")
        tabel = dictfetchall(cursor)
    context = {'semuatokoh': tabel}
    return render(request, 'action.html', context)

@csrf_exempt
def create_tokoh(request):
    if request.session['role'] == 'admin':
        messages.add_message(request, messages.WARNING, f"Hanya pemain yang dapat menambahkan tokoh")
        return redirect("/")
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO TOKOH VALUES 
                    ('{request.session['username']}',
                    '{request.POST['nama_tokoh']}',
                    '{request.POST['jenis_kelamin']}',
                    'Aktif',
                    0,
                    100,
                    0,
                    0,
                    '{request.POST['warna_kulit']}',
                    1,
                    'Kreatif',
                    '{request.POST['pekerjaan']}',
                    'RB001',
                    'MT001',
                    'RM001')
                """)
                messages.add_message(request, messages.SUCCESS, "Data tokoh berhasil disimpan!")

                return redirect("tokoh:create_tokoh")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data tokoh dengan nama {request.POST['nama_tokoh']} sudah terdaftar")

    with connection.cursor() as cursor:
        cursor.execute("SELECT KODE FROM WARNA_KULIT")
        context = {"list_warna_kulit" : cursor.fetchall()}
        cursor.execute("SELECT NAMA FROM PEKERJAAN")
        context["list_pekerjaan"] = cursor.fetchall()

        return render(request, "create_tokoh.html", context)