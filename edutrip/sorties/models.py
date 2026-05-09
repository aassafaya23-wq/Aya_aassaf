from django.db import models


class Classe(models.Model):
    NIVEAUX = [
        ('Primaire', 'Primaire'),
        ('Collège', 'Collège'),
        ('Lycée', 'Lycée'),
    ]
    nom_classe = models.CharField(max_length=50, verbose_name="Nom de la classe")
    niveau = models.CharField(max_length=20, choices=NIVEAUX, verbose_name="Niveau")

    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"
        ordering = ['niveau', 'nom_classe']

    def __str__(self):
        return f"{self.nom_classe} ({self.niveau})"


class Enseignant(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    matiere = models.CharField(max_length=100, verbose_name="Matière enseignée")

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matiere})"


class Sortie(models.Model):
    ville = models.CharField(max_length=100, verbose_name="Destination (Ville)")
    date_sortie = models.DateField(verbose_name="Date de la sortie")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, verbose_name="Classe participante")
    nb_eleves = models.PositiveIntegerField(verbose_name="Nombre d'élèves")
    responsable = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, verbose_name="Responsable")

    class Meta:
        verbose_name = "Sortie scolaire"
        verbose_name_plural = "Sorties scolaires"
        ordering = ['date_sortie']

    def __str__(self):
        return f"Sortie à {self.ville} le {self.date_sortie} – {self.classe}"
