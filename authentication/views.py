from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection, IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse, HttpResponse

def homepage(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")

    args = {}
    if role == "admin":
        args["role"] = "admin"
        args["username"] = request.session["username"]
    else:
        args["role"] = "pemain"
        args["username"] = request.session["username"]
        args["email"] = request.session["email"]
        args["no_hp"] = request.session["no_hp"]
        args["koin"] = request.session["koin"]
    return render(request, "homepage.html", args)

def login_dan_register(request):
    return render(request, "login_dan_register.html")

def	login(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ADMIN WHERE username='{}' AND password='{}'".format(request.POST["username"], request.POST["password"]))
            row = cursor.fetchall()
            if len(row) > 0:
                request.session["username"] = row[0][0]
                request.session["role"] = "admin"
                return redirect("/")
            else:
                cursor.execute("SELECT * FROM PEMAIN WHERE username='{}' AND password='{}'".format(request.POST["username"], request.POST["password"]))
                row = cursor.fetchall()
                if len(row) > 0:
                    request.session["username"] = row[0][0]
                    request.session["email"] = row[0][1]
                    request.session["no_hp"] = row[0][3]
                    request.session["koin"] = row[0][4]
                    request.session["role"] = "pemain"
                    return redirect("/")
                else:
                    return render(request, "login.html", {"error":"Username atau password salah"})

    return render(request, "login.html", {"error":""})

def logout(request):
    request.session.flush()
    return redirect("/login-dan-register")


@csrf_exempt
def register_admin(request):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO AKUN
                    ('{request.POST['username']}')
                """)
                cursor.execute(f"""
                    INSERT INTO ADMIN VALUES 
                    ('{request.POST['username']}',
                    '{request.POST['password']}')""")
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM ADMIN WHERE username='{}' AND password='{}'".format(request.POST["username"], request.POST["password"]))
                row = cursor.fetchall()
                if len(row) > 0:
                    request.session["username"] = row[0][0]
                    request.session["role"] = "admin"
                return redirect("/")
        except:
            messages.add_message(request, messages.WARNING, "email sudah sudah terdaftar")

    return render(request, "register_admin.html")

def register_pemain(request):
    return render(request, "register_pemain.html")
