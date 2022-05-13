"""the_cims URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import authentication.urls as authentication
import menggunakan_barang.urls as menggunakan_barang
import pekerjaan.urls as pekerjaan

urlpatterns = [
    path('admin/', admin.site.urls),
	path("", include(authentication)),
    path("", include(menggunakan_barang)),
    path("", include(pekerjaan)),
    path("tokoh/", include("tokoh.urls")),
    path("warna_kulit/", include("warna_kulit.urls")),
    path("level/", include("level.urls")),
    path("menggunakan_apparel/", include("menggunakan_apparel.urls")),
    path("misi_utama/", include("misi_utama.urls")),
    path("menjalankan_misi_utama/", include("menjalankan_misi_utama.urls")),
    path("makanan/", include("makanan.urls")),
    path("makan/", include("makan.urls"))
]
