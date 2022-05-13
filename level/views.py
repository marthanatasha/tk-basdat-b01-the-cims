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

def read_level(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM LEVEL")
        tabel = dictfetchall(cursor)
    context = {'semualevel': tabel}
    return render(request, 'read_level.html', context)
 
@csrf_exempt
def create_level(request):
    if request.session['role'] == 'pemain':
        messages.add_message(request, messages.WARNING, f"Hanya admin yang dapat menambahkan level")
        return redirect("/")
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO LEVEL VALUES 
                    ('{request.POST['tingkatan_level']}',
                    '{request.POST['jumlah_xp']}')
                """)

                return redirect("level:read_level")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data level dengan nama {request.POST['tingkatan_level']} sudah terdaftar")

    with connection.cursor() as cursor:
        context = {}
        return render(request, "create_level.html", context)

def update_level(request, tingkat_level):
    if request.session["role"] == "pemain":
        return redirect("/")

    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM LEVEL WHERE LEVEL='{}'".format(tingkat_level))
            data = cursor.fetchall()

    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE LEVEL 
                    SET xp='{request.POST['jumlah_xp']}'
                    WHERE LEVEL = '{tingkat_level}'
                """)
                return redirect("level:read_level")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data level dengan nama {request.POST['tingkatan_level']} sudah terdaftar")

    if len(data)<=0:
        return HttpResponse("<h1>Page not found</h1>", status=404)
    return render(request, "update_level.html", {"data":data[0]})
