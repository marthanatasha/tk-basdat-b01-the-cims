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
                    INSERT INTO level VALUES 
                    ('{request.POST['tingkatan_level']}',
                    '{request.POST['jumlah_xp']}')
                """)

                return redirect("level:read_level")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data level dengan nama {request.POST['tingkatan_level']} sudah terdaftar")

    with connection.cursor() as cursor:
        context = {}
        return render(request, "create_level.html", context)