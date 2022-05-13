from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse, HttpResponse

def create_pekerjaan(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")

    if role == "pemain":
        return HttpResponse("<h1>Page not found</h1>", status=404)

    return render(request, "create_pekerjaan.html")

def read_pekerjaan(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login_dan_register")

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
            ROW_NUMBER() OVER (), 
            *, 
            CASE WHEN p.nama NOT IN(
                SELECT pekerjaan FROM tokoh WHERE pekerjaan IS NOT NULL 
                UNION 
                SELECT nama_pekerjaan FROM bekerja 
                UNION 
                select nama_pekerjaan FROM apparel
            ) THEN true else false
            END AS deletable 
            FROM pekerjaan p""")
        pekerjaan = cursor.fetchall()

    if role == "pemain":
        return render(request, "read_pekerjaan.html", {"role":"pemain", "pekerjaan":pekerjaan})
    else:
        return render(request, "read_pekerjaan.html", {"role":"admin", "pekerjaan":pekerjaan})

def update_pekerjaan(request, nama):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")

    if role == "pemain":
        return HttpResponse("<h1>Page not found</h1>", status=404)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM pekerjaan WHERE nama='{}'".format(nama))
        data = cursor.fetchall()

    if len(data)<=0:
        return HttpResponse("<h1>Page not found</h1>", status=404)
    return render(request, "update_pekerjaan.html", {"data":data[0]})

def create_bekerja(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login_dan_register")

    if role == "admin":
        return HttpResponse("<h1>Page not found</h1>", status=404)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ROW_NUMBER() OVER (),
            t.nama,
            t.pekerjaan,
            p.base_honor
            FROM tokoh t, pekerjaan p
            WHERE p.nama=t.pekerjaan AND
            t.username_pengguna='{}'""".format(request.session['username']))
        row = cursor.fetchall()

    return render(request, "create_bekerja.html", {"data":row})

def read_bekerja(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")


    with connection.cursor() as cursor:
        if(role == "admin"):
            cursor.execute("""
                SELECT ROW_NUMBER() OVER (), 
                username_pengguna, 
                nama_tokoh,  
                nama_pekerjaan, 
                to_char(timestamp, 'DD-MM-YYYY HH24:MI'),
                keberangkatan_ke, 
                honor 
                FROM bekerja""")
            row = cursor.fetchall()
            return render(request, "read_bekerja.html", {"role":"admin", "data":row})

        else:
            cursor.execute("""
                SELECT ROW_NUMBER() OVER (), 
                nama_tokoh, 
                nama_pekerjaan, 
                to_char(timestamp, 'DD-MM-YYYY HH24:MI'), 
                keberangkatan_ke, 
                honor 
                FROM bekerja 
                WHERE username_pengguna='{}'""".format(request.session['username']))
            row = cursor.fetchall()
            return render(request, "read_bekerja.html", {"role":"pemain", "data":row})

