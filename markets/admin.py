from django.contrib import admin
from .models import (
    MaitreOuvrage, Prestataire, Marche, 
   OrdreService, Decompte, PV, Document
)

@admin.register(MaitreOuvrage)
class MaitreOuvrageAdmin(admin.ModelAdmin):
    list_display = ['nom', 'responsable', 'telephone', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['nom', 'responsable', 'email']
    ordering = ['nom']

@admin.register(Prestataire)
class PrestataireAdmin(admin.ModelAdmin):
    list_display = ['nom', 'specialite', 'telephone', 'email', 'numero_registre']
    list_filter = ['specialite', 'created_at']
    search_fields = ['nom', 'specialite', 'email']
    ordering = ['nom']



@admin.register(Marche)
class MarcheAdmin(admin.ModelAdmin):
    list_display = ['numero', 'objet', 'type', 'montant', 'statut', 'prestataire', 'date_signature']
    list_filter = ['type', 'statut', 'created_at']
    search_fields = ['numero', 'objet', 'prestataire__nom']
    ordering = ['-created_at']
    


@admin.register(OrdreService)
class OrdreServiceAdmin(admin.ModelAdmin):
    list_display = ['numero', 'objet', 'get_marches_count', 'statut', 'date_emission']
    list_filter = ['statut', 'created_at']
    search_fields = ['numero', 'objet', 'marche__numero']
    ordering = ['-created_at']

    def get_marches_count(self , obj):
        return obj.marches.count()
        
@admin.register(Decompte)
class DecompteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'get_marches_count', 'montant_ttc', 'statut', 'periode_debut', 'periode_fin']
    list_filter = ['statut', 'created_at']
    search_fields = ['numero', 'marche__numero']
    ordering = ['-created_at']

    def get_marches_count(self , obj):
        return obj.marches.count()

@admin.register(PV)
class PVAdmin(admin.ModelAdmin):
    list_display = ['numero', 'type', 'get_marches_count', 'date_pv', 'objet']
    list_filter = ['type', 'created_at']
    search_fields = ['numero', 'objet', 'marche__numero']
    ordering = ['-created_at']

    def get_marches_count(self , obj):
        return obj.marches.count()


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type', 'marche', 'taille', 'uploaded_by', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['nom', 'marche__numero']
    ordering = ['-created_at']