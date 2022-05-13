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

def read_menggunakan_apparel_admin(request):
    if request.session['role'] == 'pemain':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT USERNAME_PENGGUNA, 
        NAMA_TOKOH, 
        NAMA, 
        WARNA_APPAREL, 
        NAMA_PEKERJAAN, 
        KATEGORI_APPAREL 
        FROM MENGGUNAKAN_APPAREL MP, APPAREL P, KOLEKSI_JUAL_BELI KJB
        WHERE MP.ID_KOLEKSI = P.ID_KOLEKSI
        AND MP.ID_KOLEKSI = KJB.ID_KOLEKSI
        AND P.ID_KOLEKSI = KJB.ID_KOLEKSI""")
        tabel = dictfetchall(cursor)
    context = {'semuamenggunakan_apparel': tabel}
    return render(request, 'read_menggunakan_apparel_admin.html', context)

def read_menggunakan_apparel_pemain(request):
    if request.session['role'] == 'admin':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT USERNAME_PENGGUNA, 
        NAMA_TOKOH, 
        NAMA, 
        WARNA_APPAREL, 
        NAMA_PEKERJAAN, 
        KATEGORI_APPAREL 
        FROM MENGGUNAKAN_APPAREL MP, APPAREL P, KOLEKSI_JUAL_BELI KJB
        WHERE MP.ID_KOLEKSI = P.ID_KOLEKSI
        AND MP.ID_KOLEKSI = KJB.ID_KOLEKSI
        AND P.ID_KOLEKSI = KJB.ID_KOLEKSI
        AND USERNAME_PENGGUNA = '{request.session['username']}'""")
        tabel = dictfetchall(cursor)
    context = {'semuamenggunakan_apparelpemain': tabel}
    return render(request, 'read_menggunakan_apparel_pemain.html', context)    

@csrf_exempt
def create_menggunakan_apparel(request):
    if request.session['role'] == 'admin':
        messages.add_message(request, messages.WARNING, f"Hanya pemain yang dapat menambahkan menggunakan_apparel")
        return redirect("/")
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO MENGGUNAKAN_APPAREL VALUES 
                    ('{request.session['username']}',
                    '{request.POST['nama_tokoh']}',
                    '{request.POST['id_koleksi']}')
                """)

                return redirect("menggunakan_apparel:read_menggunakan_apparel_pemain")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data menggunakan_apparel dengan nama {request.POST['nama_menggunakan_apparel']} sudah terdaftar")

    with connection.cursor() as cursor:
        cursor.execute("SELECT NAMA_TOKOH FROM MENGGUNAKAN_APPAREL WHERE USERNAME_PENGGUNA = %s;", [request.session['username']])
        context = {"list_nama" : cursor.fetchall()}
        cursor.execute("SELECT DISTINCT ID_KOLEKSI FROM KOLEKSI_TOKOH WHERE ID_KOLEKSI LIKE 'AP%' ORDER BY ID_KOLEKSI ASC")
        context["list_apparel"] = cursor.fetchall()

        return render(request, "create_menggunakan_apparel.html", context)