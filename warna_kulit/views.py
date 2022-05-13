from django.shortcuts import render

# Create your views here.
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

def read_warna_kulit(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM WARNA_KULIT")
        tabel = dictfetchall(cursor)
    context = {'semuawarnakulit': tabel}
    return render(request, 'read_warna_kulit.html', context)
 
@csrf_exempt
def create_warna_kulit(request):
    if request.session['role'] == 'pemain':
        messages.add_message(request, messages.WARNING, f"Hanya admin yang dapat menambahkan warna_kulit")
        return redirect("/")
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO WARNA_KULIT VALUES 
                    ('{request.POST['kode_warna_kulit']}')
                """)

                return redirect("warna_kulit:read_warna_kulit")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data warna_kulit dengan nama {request.POST['nama_warna_kulit']} sudah terdaftar")

    with connection.cursor() as cursor:
        context = {}
        return render(request, "create_warna_kulit.html", context)