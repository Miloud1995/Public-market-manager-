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
    
]