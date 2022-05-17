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

def read_tokoh_admin(request):
    if request.session['role'] == 'pemain':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM TOKOH")
        tabel = dictfetchall(cursor)
    context = {'semuatokoh': tabel}
    context["role"] = request.session['role']
    return render(request, 'read_tokoh_admin.html', context)

def read_tokoh_pemain(request):
    if request.session['role'] == 'admin':
        return redirect("/")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM TOKOH WHERE USERNAME_PENGGUNA = %s;", [request.session['username']])
        tabel = dictfetchall(cursor)
    context = {'semuatokohpemain': tabel}
    context["role"] = request.session['role']
    return render(request, 'read_tokoh_pemain.html', context)    

@csrf_exempt
def create_tokoh(request):
    if request.session['role'] == 'admin':
        messages.add_message(request, messages.WARNING, f"Hanya pemain yang dapat menambahkan tokoh")
        return redirect("/")
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO TOKOH VALUES 
                    ('{request.session['username']}',
                    '{request.POST['nama_tokoh']}',
                    '{request.POST['jenis_kelamin']}',
                    'Aktif',
                    0,
                    100,
                    0,
                    0,
                    '{request.POST['warna_kulit']}',
                    1,
                    'Kreatif',
                    '{request.POST['pekerjaan']}',
                    'RB001',
                    'MT001',
                    'RM001')
                """)

                return redirect("tokoh:read_tokoh_pemain")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data tokoh dengan nama {request.POST['nama_tokoh']} sudah terdaftar")

    with connection.cursor() as cursor:
        cursor.execute("SELECT KODE FROM WARNA_KULIT")
        context = {"list_warna_kulit" : cursor.fetchall()}
        cursor.execute("SELECT NAMA FROM PEKERJAAN")
        context["list_pekerjaan"] = cursor.fetchall()
        context["role"] = request.session['role']

        return render(request, "create_tokoh.html", context)

def detail_tokoh(request):
    try:
        role = request.session["role"]
    except:
        return redirect("/login-dan-register")
        
    if request.method == "POST":
        with connection.cursor() as cursor:
            if request.session["role"] == 'admin':
                cursor.execute(f"""
                    SELECT NAMA, ID_RAMBUT, ID_MATA, ID_RUMAH, WARNA_KULIT, PEKERJAAN
                    FROM TOKOH
                    WHERE NAMA = '{request.POST['tokoh']}' AND USERNAME_PENGGUNA='{request.POST['username_pemain']}'
                """)
            else:
                cursor.execute(f"""
                    SELECT NAMA, ID_RAMBUT, ID_MATA, ID_RUMAH, WARNA_KULIT, PEKERJAAN
                    FROM TOKOH
                    WHERE NAMA = '{request.POST['tokoh']}' AND USERNAME_PENGGUNA='{request.session['username']}'
                """)
            tabel = dictfetchall(cursor)
        context = {'detailtokoh': tabel}
        context["role"] = request.session['role']
        return render(request, "detail_tokoh.html", context)

def update_tokoh(request, nama_tokoh):
    if request.session["role"] == "admin":
        return redirect("/")

    with connection.cursor() as cursor:
            cursor.execute(f"""SELECT ID_KOLEKSI FROM KOLEKSI_TOKOH WHERE NAMA_TOKOH = '{nama_tokoh}'
            AND ID_KOLEKSI LIKE 'RB%'
            """)
            rambut = dictfetchall(cursor)
            context = {"list_rambut" : rambut}
            cursor.execute(f"""SELECT ID_KOLEKSI FROM KOLEKSI_TOKOH WHERE NAMA_TOKOH = '{nama_tokoh}'
            AND ID_KOLEKSI LIKE 'MT%'
            """)
            mata = dictfetchall(cursor)
            context["list_mata"] = mata
            cursor.execute(f"""SELECT ID_KOLEKSI FROM KOLEKSI_TOKOH WHERE NAMA_TOKOH = '{nama_tokoh}'
            AND ID_KOLEKSI LIKE 'RM%'
            """)
            rumah = dictfetchall(cursor)
            context["list_rumah"] = rumah

    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE TOKOH
                    SET ID_RAMBUT='{request.POST['rambut_baru']}',
                    ID_MATA='{request.POST['mata_baru']}',
                    ID_RUMAH='{request.POST['rumah_baru']}'
                    WHERE NAMA = '{nama_tokoh}'
                """)
                return redirect("tokoh:read_tokoh_pemain")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Data level dengan nama {request.POST['nama_tokoh']} sudah terdaftar")
    context["nama_tokoh_update"] = nama_tokoh
    context["role"] = request.session['role']

    return render(request, "update_tokoh.html", context)