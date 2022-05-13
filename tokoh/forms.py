from django import forms
from django.db import connection


class CreateTokoh(forms.Form):
    list_warna_kulit = []
    list_pekerjaan = []
    list_jk = ["Laki-laki", "perempuan"]
    warna_kulit = forms.ChoiceField(choices=list_warna_kulit, required=True)
    pekerjaan = forms.ChoiceField(choices=list_pekerjaan, required=True)
    j_kelamin = forms.ChoiceField(choices=list_jk, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT KODE FROM WARNA_KULIT;")
            self.fields['warna_kulit'].choices = cursor.fetchall()
            cursor.execute(
                "SELECT NAMA FROM PEKERJAAN;")
            self.fields['pekerjaan'].choices = cursor.fetchall()