from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

def create_menggunakan_barang(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")

    if role == 'admin':
        return HttpResponse("<h1>Page not found</h1>", status=404)

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
            cursor.execute("SELECT id_koleksi FROM koleksi_tokoh WHERE username_pengguna='{}' AND nama_tokoh='{}'".format(request.session['username'], request.POST['nama_tokoh']))
            barang = cursor.fetchall()
        return JsonResponse({'barang': barang})
    return HttpResponse("<h1>Method not allowed</h1>", status=405)