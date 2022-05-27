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
        cursor.execute("""
            SELECT 
            ROW_NUMBER() OVER (), 
            *, 
            CASE WHEN LEVEL NOT IN(
                SELECT LEVEL FROM TOKOH
            ) THEN true else false
            END AS deletable 
            FROM LEVEL""")
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
        except:
            messages.add_message(request, messages.WARNING, "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu")

    with connection.cursor() as cursor:
        context = {}
        return render(request, "create_level.html", context)

def update_level(request, tingkat_level):
    if request.session["role"] == "pemain":
        return redirect("/")

    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM LEVEL WHERE LEVEL='{}'".format(tingkat_level))
            data = dictfetchall(cursor)
            context = {"data":data[0]}

    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE LEVEL 
                    SET xp='{request.POST['jumlah_xp']}'
                    WHERE LEVEL = '{tingkat_level}'
                """)
                return redirect("level:read_level")
        except:
            messages.add_message(request, messages.WARNING, "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu")

    return render(request, "update_level.html", context)

def delete_level(request):
    if request.session["role"] == "pemain":
        return redirect("/")

    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute(f"""
                DELETE FROM LEVEL 
                WHERE LEVEL = '{request.POST['tingkat_level']}'
            """)
            return redirect("level:read_level")
        

