from django.shortcuts import render, redirect
from django.db import connection

def homepage(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login")

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
    return redirect("/login")

def register_admin(request):
    return render(request, "register_admin.html")

def register_pemain(request):
    return render(request, "register_pemain.html")
