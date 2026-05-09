# EduTrip – Système de Gestion des Sorties Scolaires

Application web Django pour planifier et gérer les sorties pédagogiques.

## Installation

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# 3. Créer un compte administrateur
python manage.py createsuperuser

# 4. Lancer le serveur
python manage.py runserver
```

Ouvrir : http://127.0.0.1:8000

## Fonctionnalités

- Tableau de bord avec alertes pour les sorties imminentes (< 7 jours)
- CRUD complet : Sorties, Classes, Enseignants
- Recherche et filtrage multi-critères (ville, classe, responsable, période)
- Interface d'administration Django sur /admin/
- Authentification (login/logout)

## Structure

```
edutrip/
├── manage.py
├── requirements.txt
├── edutrip/         # Configuration Django
│   ├── settings.py
│   └── urls.py
└── sorties/         # Application principale
    ├── models.py    # Sortie, Classe, Enseignant
    ├── views.py
    ├── forms.py
    ├── admin.py
    └── templates/
```
