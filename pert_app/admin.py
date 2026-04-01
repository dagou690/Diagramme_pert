from django.contrib import admin
from .models import Projet, Tache

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ['nom', 't0', 'created_at']

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ['id_tache', 'nom', 'duree', 'projet']
