from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Sortie, Classe, Enseignant
from .forms import SortieForm, ClasseForm, EnseignantForm, RechercheForm


# ─── Inscription ──────────────────────────────────────────────────────────────

def inscription(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email      = request.POST.get('email', '')
            user.first_name = request.POST.get('first_name', '')
            user.last_name  = request.POST.get('last_name', '')
            user.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} ! Votre compte a été créé avec succès.")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'sorties/inscription.html', {'form': form})


# ─── Accueil publique ────────────────────────────────────────────────────────

def accueil(request):
    """Page d'accueil publique (landing page)."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'sorties/accueil.html')


# ─── Dashboard ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    """Page d'accueil : statistiques et sorties imminentes."""
    aujourd_hui = timezone.now().date()
    dans_7_jours = aujourd_hui + timedelta(days=7)

    sorties_imminentes = Sortie.objects.filter(
        date_sortie__gte=aujourd_hui,
        date_sortie__lte=dans_7_jours
    ).order_by('date_sortie')

    prochaines_sorties = Sortie.objects.filter(
        date_sortie__gte=aujourd_hui
    ).order_by('date_sortie')[:5]

    context = {
        'total_sorties': Sortie.objects.count(),
        'total_classes': Classe.objects.count(),
        'total_enseignants': Enseignant.objects.count(),
        'sorties_imminentes': sorties_imminentes,
        'prochaines_sorties': prochaines_sorties,
        'aujourd_hui': aujourd_hui,
    }
    return render(request, 'sorties/dashboard.html', context)


# ─── Sorties ─────────────────────────────────────────────────────────────────

@login_required
def sortie_liste(request):
    """Liste de toutes les sorties avec recherche/filtrage."""
    form = RechercheForm(request.GET or None)
    sorties = Sortie.objects.select_related('classe', 'responsable').order_by('date_sortie')

    if form.is_valid():
        ville = form.cleaned_data.get('ville')
        classe = form.cleaned_data.get('classe')
        responsable = form.cleaned_data.get('responsable')
        date_debut = form.cleaned_data.get('date_debut')
        date_fin = form.cleaned_data.get('date_fin')

        if ville:
            sorties = sorties.filter(ville__icontains=ville)
        if classe:
            sorties = sorties.filter(classe=classe)
        if responsable:
            sorties = sorties.filter(responsable=responsable)
        if date_debut:
            sorties = sorties.filter(date_sortie__gte=date_debut)
        if date_fin:
            sorties = sorties.filter(date_sortie__lte=date_fin)

    aujourd_hui = timezone.now().date()
    dans_7_jours = aujourd_hui + timedelta(days=7)

    return render(request, 'sorties/sortie_liste.html', {
        'sorties': sorties,
        'form': form,
        'aujourd_hui': aujourd_hui,
        'dans_7_jours': dans_7_jours,
    })


@login_required
def sortie_detail(request, pk):
    sortie = get_object_or_404(Sortie, pk=pk)
    aujourd_hui = timezone.now().date()
    dans_7_jours = aujourd_hui + timedelta(days=7)
    imminente = aujourd_hui <= sortie.date_sortie <= dans_7_jours
    return render(request, 'sorties/sortie_detail.html', {
        'sortie': sortie,
        'imminente': imminente,
    })


@login_required
def sortie_creer(request):
    if request.method == 'POST':
        form = SortieForm(request.POST)
        if form.is_valid():
            sortie = form.save()
            messages.success(request, f"La sortie à {sortie.ville} a été créée avec succès.")
            return redirect('sortie_detail', pk=sortie.pk)
    else:
        form = SortieForm()
    return render(request, 'sorties/sortie_form.html', {'form': form, 'titre': 'Nouvelle sortie'})


@login_required
def sortie_modifier(request, pk):
    sortie = get_object_or_404(Sortie, pk=pk)
    if request.method == 'POST':
        form = SortieForm(request.POST, instance=sortie)
        if form.is_valid():
            sortie = form.save()
            messages.success(request, f"La sortie à {sortie.ville} a été modifiée.")
            return redirect('sortie_detail', pk=sortie.pk)
    else:
        form = SortieForm(instance=sortie)
    return render(request, 'sorties/sortie_form.html', {
        'form': form,
        'titre': f'Modifier la sortie – {sortie.ville}',
        'sortie': sortie,
    })


@login_required
def sortie_supprimer(request, pk):
    sortie = get_object_or_404(Sortie, pk=pk)
    if request.method == 'POST':
        ville = sortie.ville
        sortie.delete()
        messages.warning(request, f"La sortie à {ville} a été supprimée.")
        return redirect('sortie_liste')
    return render(request, 'sorties/confirmer_suppression.html', {'objet': sortie, 'type': 'la sortie'})


# ─── Classes ─────────────────────────────────────────────────────────────────

@login_required
def classe_liste(request):
    classes = Classe.objects.all()
    return render(request, 'sorties/classe_liste.html', {'classes': classes})


@login_required
def classe_creer(request):
    if request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            classe = form.save()
            messages.success(request, f"La classe {classe.nom_classe} a été ajoutée.")
            return redirect('classe_liste')
    else:
        form = ClasseForm()
    return render(request, 'sorties/classe_form.html', {'form': form, 'titre': 'Nouvelle classe'})


@login_required
def classe_modifier(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    if request.method == 'POST':
        form = ClasseForm(request.POST, instance=classe)
        if form.is_valid():
            form.save()
            messages.success(request, "Classe mise à jour.")
            return redirect('classe_liste')
    else:
        form = ClasseForm(instance=classe)
    return render(request, 'sorties/classe_form.html', {
        'form': form,
        'titre': f'Modifier {classe.nom_classe}',
    })


@login_required
def classe_supprimer(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    if request.method == 'POST':
        classe.delete()
        messages.warning(request, "Classe supprimée.")
        return redirect('classe_liste')
    return render(request, 'sorties/confirmer_suppression.html', {'objet': classe, 'type': 'la classe'})


# ─── Enseignants ─────────────────────────────────────────────────────────────

@login_required
def enseignant_liste(request):
    enseignants = Enseignant.objects.all()
    return render(request, 'sorties/enseignant_liste.html', {'enseignants': enseignants})


@login_required
def enseignant_creer(request):
    if request.method == 'POST':
        form = EnseignantForm(request.POST)
        if form.is_valid():
            ens = form.save()
            messages.success(request, f"{ens.prenom} {ens.nom} a été ajouté(e).")
            return redirect('enseignant_liste')
    else:
        form = EnseignantForm()
    return render(request, 'sorties/enseignant_form.html', {'form': form, 'titre': 'Nouvel enseignant'})


@login_required
def enseignant_modifier(request, pk):
    ens = get_object_or_404(Enseignant, pk=pk)
    if request.method == 'POST':
        form = EnseignantForm(request.POST, instance=ens)
        if form.is_valid():
            form.save()
            messages.success(request, "Enseignant mis à jour.")
            return redirect('enseignant_liste')
    else:
        form = EnseignantForm(instance=ens)
    return render(request, 'sorties/enseignant_form.html', {
        'form': form,
        'titre': f'Modifier {ens.prenom} {ens.nom}',
    })


@login_required
def enseignant_supprimer(request, pk):
    ens = get_object_or_404(Enseignant, pk=pk)
    if request.method == 'POST':
        ens.delete()
        messages.warning(request, "Enseignant supprimé.")
        return redirect('enseignant_liste')
    return render(request, 'sorties/confirmer_suppression.html', {'objet': ens, 'type': "l'enseignant"})
