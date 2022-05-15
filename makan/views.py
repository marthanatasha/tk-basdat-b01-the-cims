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

def read_makan_admin(request):
    if request.session['role'] == 'pemain':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM MAKAN""")
        tabel = dictfetchall(cursor)
    context = {'makanan': tabel}
    return render(request, 'read_makan.html', context)

def read_makan_pemain(request):
    if request.session['role'] == 'admin':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM MAKAN WHERE USERNAME_PENGGUNA = %s;", [request.session['username']])
        tabel = dictfetchall(cursor)
    context = {'makanan': tabel}
    return render(request, 'read_makan.html', context)

@csrf_exempt
def create_makan(request):
    # if request.session['role'] == 'admin':
    #     messages.add_message(request, messages.WARNING, f"Hanya pemain yang dapat menambahkan menggunakan_apparel")
    #     return redirect("/")
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO MAKAN VALUES 
                    ('{request.session['username']}',
                    '{request.POST['nama_tokoh']}',
                    CURRENT_TIMESTAMP,
                    '{request.POST['nama_makanan']}')
                """)

                return redirect("makan:read_makan_pemain")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data makan dengan nama {request.POST['nama_makan']} sudah terdaftar")

    with connection.cursor() as cursor:
        cursor.execute("SELECT nama FROM tokoh WHERE username_pengguna='{}'".format(request.session['username']))
        tokoh = cursor.fetchall()
        cursor.execute ("SELECT nama FROM MAKANAN")
        makanan = dictfetchall(cursor)

    return render(request, "create_makan.html", {"tokoh":tokoh, "makanan":makanan})

@csrf_exempt
def get_makanan(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("SELECT nama FROM MAKANAN")
            makanan = cursor.fetchall()
        return JsonResponse({'makanan': makanan})
    return HttpResponse("<h1>Method not allowed</h1>", status=405)
