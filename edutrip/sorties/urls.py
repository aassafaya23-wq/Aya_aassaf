from django.urls import path
from . import views

urlpatterns = [
    # Accueil public
    path('', views.accueil, name='accueil'),

    # Inscription
    path('inscription/', views.inscription, name='inscription'),

    # Dashboard (protégé)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Sorties
    path('sorties/', views.sortie_liste, name='sortie_liste'),
    path('sorties/nouvelle/', views.sortie_creer, name='sortie_creer'),
    path('sorties/<int:pk>/', views.sortie_detail, name='sortie_detail'),
    path('sorties/<int:pk>/modifier/', views.sortie_modifier, name='sortie_modifier'),
    path('sorties/<int:pk>/supprimer/', views.sortie_supprimer, name='sortie_supprimer'),

    # Classes
    path('classes/', views.classe_liste, name='classe_liste'),
    path('classes/nouvelle/', views.classe_creer, name='classe_creer'),
    path('classes/<int:pk>/modifier/', views.classe_modifier, name='classe_modifier'),
    path('classes/<int:pk>/supprimer/', views.classe_supprimer, name='classe_supprimer'),

    # Enseignants
    path('enseignants/', views.enseignant_liste, name='enseignant_liste'),
    path('enseignants/nouveau/', views.enseignant_creer, name='enseignant_creer'),
    path('enseignants/<int:pk>/modifier/', views.enseignant_modifier, name='enseignant_modifier'),
    path('enseignants/<int:pk>/supprimer/', views.enseignant_supprimer, name='enseignant_supprimer'),
]
