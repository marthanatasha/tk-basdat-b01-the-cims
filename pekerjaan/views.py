from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse, HttpResponse

def create_pekerjaan(request):
    role = None
    try:
        role = request.session["role"]
    except:
        return redirect("/login")

    if role == "pemain":
        return HttpResponse("<h1>Page not found</h1>", status=404)

    return render(request, "create_pekerjaan.html")

def read_pekerjaan(request):
    role = None
    try:
        role = request.session["role"]
    except:
        return redirect("/login")

    with connection.cursor() as cursor:
        cursor.execute("SELECT ROW_NUMBER() OVER (), * FROM pekerjaan")
        pekerjaan = cursor.fetchall()

    if role == "pemain":
        return render(request, "read_pekerjaan.html", {"role":"pemain", "pekerjaan":pekerjaan})
    else:
        return render(request, "read_pekerjaan.html", {"role":"admin", "pekerjaan":pekerjaan})

def update_pekerjaan(request, nama):
    role = None
    try:
        role = request.session["role"]
    except:
        return redirect("/login")

    if role == "pemain":
        return HttpResponse("<h1>Page not found</h1>", status=404)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM pekerjaan WHERE nama='{}'".format(nama))
        data = cursor.fetchall()
        
    if len(data)<=0:
        return HttpResponse("<h1>Page not found</h1>", status=404)
    return render(request, "update_pekerjaan.html", {"data":data[0]})



