from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from datetime import datetime

def create_pekerjaan(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")

    if role == "pemain":
        return HttpResponse("<h1>Page not found</h1>", status=404)

    if request.method == "POST":
        nama_pekerjaan = request.POST["nama_pekerjaan"]
        base_honor = request.POST["base_honor"]

        if nama_pekerjaan == "" or base_honor == "":
            messages.error(request, "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu")
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO PEKERJAAN VALUES ('{}', '{}')".format(nama_pekerjaan, base_honor))
            except IntegrityError:
                messages.error(request,"Data pekerjaan dengan nama {} sudah terdaftar".format(nama_pekerjaan))

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

    if request.method == "POST":
        base_honor = request.POST["base_honor"]
        print(base_honor, nama)

        if base_honor == "":
            messages.error(request, "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu")
        else:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE PEKERJAAN SET base_honor={} WHERE nama='{}'".format(base_honor, nama))
                cursor.execute("SELECT * FROM pekerjaan WHERE nama='{}'".format(nama))
                data = cursor.fetchall()

    return render(request, "update_pekerjaan.html", {"data":data[0]})


def delete_pekerjaan(request, nama):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")

    try:
        with connection.cursor() as cursor:
             cursor.execute("DELETE FROM PEKERJAAN WHERE nama='{}'".format(nama))
    except IntegrityError:
        messages.error(request,"Data pekerjaan dengan nama {} sudah di-refer".format(nama))

    return redirect("/read/pekerjaan")


def create_bekerja(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")

    if role == "admin":
        return HttpResponse("<h1>Page not found</h1>", status=404)

    if request.method == "POST":
        nama_tokoh = request.POST["nama_tokoh"]
        username_pengguna = request.session["username"]
        nama_pekerjaan = request.POST["nama_pekerjaan"]
        base_salary = request.POST["base_salary"]

        with connection.cursor() as cursor:
            cursor.execute("""SELECT level, keberangkatan_ke 
                FROM TOKOH t, BEKERJA b
                WHERE t.nama='{}' 
                and t.username_pengguna='{}'
                and b.nama_tokoh=t.nama
                and b.username_pengguna=t.username_pengguna
                and b.nama_pekerjaan='{}'
                ORDER BY keberangkatan_ke DESC"""
                .format(nama_tokoh, username_pengguna, nama_pekerjaan))
            row = cursor.fetchall()
            level = row[0][0]
            keberangkatan_ke = row[0][1]
            print(level, keberangkatan_ke)
            cursor.execute("""
                INSERT INTO BEKERJA VALUES(
                '{}', '{}', '{}', '{}', {}, {})"""
                .format(username_pengguna, nama_tokoh, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    nama_pekerjaan, keberangkatan_ke+1, base_salary*level))

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

