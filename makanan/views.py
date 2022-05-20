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

def read_makanan_admin(request):
    if request.session['role'] == 'pemain':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT *, 
        CASE WHEN NAMA NOT IN (
                SELECT NAMA_MAKANAN FROM MAKAN
        ) THEN true else false
        END AS DELETABLE 
        FROM MAKANAN""")
        tabel = dictfetchall(cursor)
    context = {'makanan': tabel}
    return render(request, 'read_makanan.html', context)

def read_makanan_pemain(request):
    if request.session['role'] == 'admin':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM MAKANAN""")
        tabel = dictfetchall(cursor)
    context = {'makanan': tabel}
    return render(request, 'read_makanan.html', context)

@csrf_exempt
def create_makanan(request):
    # if request.session['role'] == 'pemain':
    #     messages.add_message(request, messages.WARNING, f"Hanya admin yang dapat menambahkan level")
    #     return redirect("/")
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO MAKANAN VALUES 
                    ('{request.POST['nama_makanan']}',
                    '{request.POST['harga']}',
                    '{request.POST['tingkat_energi']}',
                    '{request.POST['tingkat_kelaparan']}')
                """)

                return redirect("makanan:read_makanan_admin")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data makanan dengan nama {request.POST['nama_makanan']} sudah terdaftar")

    with connection.cursor() as cursor:
        context = {}
        return render(request, "create_makanan.html", context)

def update_makanan(request, nama_makanan):
    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM MAKANAN WHERE NAMA='{}'".format(nama_makanan))
            data = cursor.fetchall()

    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE MAKANAN
                    SET harga='{request.POST['harga']}',
                    tingkat_energi='{request.POST['tingkat_energi']}',
                    tingkat_kelaparan='{request.POST['tingkat_kelaparan']}'
                    WHERE nama = '{nama_makanan}'
                """)
                return redirect("makanan:read_makanan_admin")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data makanan tersebut sudah terdaftar")

    if len(data)<=0:
        return HttpResponse("<h1>Page not found</h1>", status=404)
    return render(request, "update_makanan.html", {"data":data[0]})


def delete_makanan(request):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    DELETE FROM MAKANAN
                    WHERE NAMA = '{request.POST['nama_makanan']}'
                """)
                return redirect("makanan:read_makanan_admin")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data makanan dengan nama '{request.POST['nama_misi']}' sudah direfer")