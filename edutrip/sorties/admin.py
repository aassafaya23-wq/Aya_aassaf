from django.contrib import admin
from .models import Classe, Enseignant, Sortie


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom_classe', 'niveau')
    list_filter = ('niveau',)
    search_fields = ('nom_classe',)


@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'matiere')
    search_fields = ('nom', 'prenom', 'matiere')
    ordering = ('nom',)


@admin.register(Sortie)
class SortieAdmin(admin.ModelAdmin):
    list_display = ('ville', 'date_sortie', 'classe', 'nb_eleves', 'responsable')
    list_filter = ('classe', 'responsable', 'date_sortie')
    search_fields = ('ville',)
    date_hierarchy = 'date_sortie'
    ordering = ('date_sortie',)

# Customize admin site header
admin.site.site_header = "EduTrip – Administration"
admin.site.site_title = "EduTrip Admin"
admin.site.index_title = "Gestion des Sorties Scolaires"
