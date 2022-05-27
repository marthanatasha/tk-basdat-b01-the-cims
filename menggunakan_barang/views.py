from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime

def create_menggunakan_barang(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")

    if role == 'admin':
        return HttpResponse("<h1>Page not found</h1>", status=404)

    if request.method == "POST":
        nama_tokoh = request.POST["nama_tokoh"]
        barang = request.POST["barang"]

        if nama_tokoh == "" or barang == "":
            messages.error(request, "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu")
        else:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT b.tingkat_energi, t.energi 
                    FROM BARANG b, TOKOH t 
                    WHERE b.id_koleksi='{}' 
                    AND t.nama='{}' 
                    AND t.username_pengguna='{}'""".format(barang, nama_tokoh, request.session["username"]))
                row = cursor.fetchall()
                if row[0][1] < row[0][0]:
                    messages.error(request, "Energi tokoh tidak mencukupi sehingga barang tidak dapat digunakan")
                else:
                   cursor.execute("INSERT INTO MENGGUNAKAN_BARANG VALUES ('{}', '{}', '{}', '{}')"
                    .format(request.session["username"], nama_tokoh, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), barang))
                   return redirect("/read/menggunakan-barang") 

    with connection.cursor() as cursor:
        cursor.execute("SELECT nama FROM tokoh WHERE username_pengguna='{}'".format(request.session['username']))
        tokoh = cursor.fetchall()
    return render(request, "create_menggunakan_barang.html", {"tokoh":tokoh})

def read_menggunakan_barang(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")


    with connection.cursor() as cursor:
        if(role == "admin"):
            cursor.execute("""
                SELECT ROW_NUMBER() OVER (), 
                mb.username_pengguna, 
                mb.nama_tokoh, 
                k.nama, 
                to_char(waktu, 'DD/MM/YYYY HH24:MI') 
                FROM menggunakan_barang mb, koleksi_jual_beli k
                WHERE mb.id_barang=k.id_koleksi""")
            row = cursor.fetchall()
            return render(request, "read_menggunakan_barang.html", {"role":"admin", "data":row})

        else:
            cursor.execute("""
                SELECT ROW_NUMBER() OVER (), 
                mb.nama_tokoh, 
                k.nama, 
                to_char(mb.waktu, 'DD/MM/YYYY HH24:MI') 
                FROM menggunakan_barang mb, koleksi_jual_beli k
                WHERE mb.id_barang=k.id_koleksi AND username_pengguna='{}'""".format(request.session['username']))
            row = cursor.fetchall()
            return render(request, "read_menggunakan_barang.html", {"role":"pemain", "data":row})

@csrf_exempt
def get_barang(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")

    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT kt.id_koleksi FROM KOLEKSI_TOKOH kt  
                INNER  JOIN BARANG b 
                ON b.id_koleksi=kt.id_koleksi 
                AND kt. username_pengguna='{}' 
                AND kt.nama_tokoh='{}'""".format(request.session['username'], request.POST['nama_tokoh']))
            barang = cursor.fetchall()
        return JsonResponse({'barang': barang})
    return HttpResponse("<h1>Method not allowed</h1>", status=405)