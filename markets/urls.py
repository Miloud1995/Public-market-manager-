from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
  
    # Maître d'Ouvrage URLs
    path('maitre-ouvrage/', views.maitre_ouvrage_list, name='maitre_ouvrage_list'),
    path('maitre-ouvrage/create/', views.maitre_ouvrage_create, name='maitre_ouvrage_create'),
    path('maitre-ouvrage/<int:pk>/update/', views.maitre_ouvrage_update, name='maitre_ouvrage_update'),
    path('maitre-ouvrage/<int:pk>/delete/', views.maitre_ouvrage_delete, name='maitre_ouvrage_delete'),
    path('maitre-ouvrage/<int:pk>/', views.maitre_ouvrage_detail, name='maitre_detail'),
    
    # Prestataire URLs
    path('prestataires/', views.prestataire_list, name='prestataire_list'),
    path('prestataires/<int:pk>/', views.prestataire_detail, name='prestataire_detail'),
    path('prestataires/create/', views.prestataire_create, name='prestataire_create'),
    path('prestataires/<int:pk>/update/', views.prestataire_update, name='prestataire_update'),
    path('prestataires/<int:pk>/delete/', views.prestataire_delete, name='prestataire_delete'),
    
    # Marché URLs
    path('marches/', views.marche_list, name='marche_list'),
    path('marches/create/', views.marche_create, name='marche_create'),
    path('marches/<int:pk>/', views.marche_detail, name='marche_detail'),
    path('marches/<int:pk>/update/', views.marche_update, name='marche_update'),
    path('marches/<int:pk>/delete/', views.marche_delete, name='marche_delete'),
    path('marches/<int:pk>/pdf/', views.generate_marche_pdf, name='generate_marche_pdf'),
    

    #decompte URLs
    path('decomptes/', views.decompte_list, name='decompte_list'),
    path('decompte/create/', views.decompte_create, name='decompte_create'),
    path('decompte/<int:pk>/pdf/', views.generate_decompte_pdf, name='generate_decompte_pdf'),
    path('decompte/<int:pk>/delete/', views. decompte_delete, name='decompte_delete'),
    path('decompte/<int:pk>/update/', views.decompte_update, name='decompte_update'),
    path('decompte/<int:pk>/', views.decompte_detail, name='decompte_detail'),
    

    #Orderde sevrice  URLs
    path('orders/',views.order_list, name='order_list'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/<int:pk>/pdf/', views.generate_ordre_service_pdf, name='generate_ordre_service_pdf'),
    path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('order/<int:pk>/update/', views.order_update, name='order_update'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),



    #PVs  URLs
    path('pvs/',views.pv_list, name='pv_list'),
    path('pv/create/', views.pv_create, name='pv_create'),
    path('pv/<int:pk>/update/', views.pv_update, name='pv_update'),
    path('pv/<int:pk>/', views.pv_detail, name='pv_detail'),
    path('pv/<int:pk>/delete/', views.pv_delete, name='pv_delete'),
    path('pv/<int:pk>/pdf/', views.generate_pv_pdf, name='generate_pv_pdf'),

    #FILEs  URLs
    path('documents/',views.document_list, name='document_list'),
    path('document/create/', views.document_create, name='document_create'),
    path('document/<int:pk>/update/', views.document_update, name='document_update'),
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path('document/<int:pk>/delete/', views.document_delete, name='document_delete'),

    #acompte URLs
    path('acomptes/', views.acompte_list, name='acompte_list'),
    path('acompte/create/', views.acompte_create, name='acompte_create'),
    #path('decompte/<int:pk>/pdf/', views.generate_decompte_pdf, name='generate_decompte_pdf'),
    path('acompte/<int:pk>/delete/', views. acompte_delete, name='acompte_delete'),
    path('acompte/<int:pk>/update/', views.acompte_update, name='acompte_update'),
    path('acompte/<int:pk>/', views.acompte_detail, name='acompte_detail'),

    #Signataires URLs
    path('signataires/', views.signataire_list, name='signataire_list'),
    path('signataire/create/', views.signataire_create, name='signataire_create'),
    #path('signataire/<int:pk>/delete/', views. signataire_delete, name='signataire_delete'),
    path('signataire/<int:pk>/update/', views.signataire_update, name='signataire_update'),
    path('signataire/<int:pk>/', views.signataire_detail, name='signataire_detail'),


    path('lignes/',views.ligne_list, name='ligne_list'),
    path('ligne/create/', views.ligne_create, name='ligne_create'),
    path('ligne/<int:pk>/update/', views.ligne_update, name='ligne_update'),
    path('ligne/<int:pk>/', views.ligne_detail, name='ligne_detail'),
    path('ligne/<int:pk>/delete/', views.ligne_delete, name='ligne_delete'),
    

    
]