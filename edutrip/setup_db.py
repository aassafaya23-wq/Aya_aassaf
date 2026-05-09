#!/usr/bin/env python
"""
Script de mise en place automatique de la base de données EduTrip.
Lance ce script UNE SEULE FOIS après l'installation.

Usage :
    python setup_db.py
"""

import os
import sys
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edutrip.settings')

def run(cmd):
    print(f"\n▶ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"  ✗ Erreur lors de : {cmd}")
        sys.exit(1)
    print(f"  ✓ OK")

if __name__ == "__main__":
    print("=" * 50)
    print("   EduTrip – Initialisation de la base de données")
    print("=" * 50)

    run("python manage.py makemigrations sorties")
    run("python manage.py migrate")
    run("python manage.py loaddata sorties/fixtures/initial_data.json")

    print("\n" + "=" * 50)
    print("  ✅ Base de données initialisée avec succès !")
    print("     10 classes, 8 enseignants, 12 sorties chargées.")
    print("\n  Créez maintenant votre compte admin :")
    print("     python manage.py createsuperuser")
    print("\n  Puis lancez le serveur :")
    print("     python manage.py runserver")
    print("=" * 50)
