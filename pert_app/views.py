import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Projet, Tache
from .forms import ProjetForm, TacheForm


# ─── Projets ───────────────────────────────────────────────────────────────────

def projets_index(request):
    projets = Projet.objects.prefetch_related('taches').all()
    return render(request, 'pert_app/projets/index.html', {'projets': projets})


def projets_creer(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save()
            messages.success(request, 'Projet créé avec succès !')
            return redirect('projets:afficher', pk=projet.pk)
    else:
        form = ProjetForm()
    return render(request, 'pert_app/projets/creer.html', {'form': form})


def projets_afficher(request, pk):
    projet = get_object_or_404(Projet.objects.prefetch_related('taches'), pk=pk)
    tache_form = TacheForm(projet=projet)
    return render(request, 'pert_app/projets/afficher.html', {
        'projet': projet,
        'tache_form': tache_form,
    })


def projets_modifier(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    if request.method == 'POST':
        form = ProjetForm(request.POST, instance=projet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projet mis à jour !')
            return redirect('projets:afficher', pk=projet.pk)
    else:
        form = ProjetForm(instance=projet)
    return render(request, 'pert_app/projets/modifier.html', {'form': form, 'projet': projet})


@require_POST
def projets_supprimer(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    projet.delete()
    messages.success(request, 'Projet supprimé !')
    return redirect('projets:index')


# ─── Tâches ────────────────────────────────────────────────────────────────────

@require_POST
def taches_enregistrer(request, projet_pk):
    projet = get_object_or_404(Projet, pk=projet_pk)
    form = TacheForm(request.POST, projet=projet)
    if form.is_valid():
        tache = form.save(commit=False)
        tache.projet = projet
        tache.predecesseurs = request.POST.getlist('predecesseurs') or []
        tache.save()
        messages.success(request, 'Tâche ajoutée !')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
    return redirect('projets:afficher', pk=projet.pk)


@require_POST
def taches_supprimer(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    projet_pk = tache.projet_id
    tache.delete()
    messages.success(request, 'Tâche supprimée !')
    return redirect('projets:afficher', pk=projet_pk)


# ─── Diagramme PERT ────────────────────────────────────────────────────────────

def pert_afficher(request, projet_pk):
    projet = get_object_or_404(Projet.objects.prefetch_related('taches'), pk=projet_pk)

    if not projet.taches.exists():
        messages.error(request, 'Aucune tâche dans ce projet !')
        return redirect('projets:afficher', pk=projet.pk)

    T0 = projet.t0 or 1
    donnees_pert = calculer_pert(projet.taches.all(), T0)

    return render(request, 'pert_app/pert/diagram.html', {
        'projet': projet,
        'donnees_pert': donnees_pert,
        'donnees_pert_json': json.dumps(donnees_pert),
    })


# ─── Algorithme PERT ───────────────────────────────────────────────────────────

def calculer_pert(taches, T0=1):
    carte_taches = {}

    for tache in taches:
        carte_taches[tache.id_tache] = {
            'id': tache.id_tache,
            'nom': tache.nom,
            'duree': tache.duree,
            'predecesseurs': tache.predecesseurs or [],
            'debut_plus_tot': 0,
            'fin_plus_tot': 0,
            'debut_plus_tard': 0,
            'fin_plus_tard': 0,
            'marge_total': 0,
            'marge_libre': 0,
        }

    triee = tri_topologique(carte_taches)

    # Passe avant : calcul des dates au plus tôt
    for id_tache in triee:
        tache = carte_taches[id_tache]
        if not tache['predecesseurs']:
            tache['debut_plus_tot'] = T0
            tache['fin_plus_tot'] = T0 + tache['duree'] - 1
        else:
            max_fin = 0
            for id_pred in tache['predecesseurs']:
                if id_pred in carte_taches:
                    max_fin = max(max_fin, carte_taches[id_pred]['fin_plus_tot'])
            tache['debut_plus_tot'] = max_fin + 1
            tache['fin_plus_tot'] = tache['debut_plus_tot'] + tache['duree'] - 1

    Tf = max(t['fin_plus_tot'] for t in carte_taches.values())

    # Passe arrière : calcul des dates au plus tard
    for id_tache in reversed(triee):
        tache = carte_taches[id_tache]
        successeurs = [
            sid for sid, st in carte_taches.items()
            if id_tache in st['predecesseurs']
        ]

        if not successeurs:
            tache['fin_plus_tard'] = Tf
            tache['debut_plus_tard'] = Tf - tache['duree'] + 1
        else:
            min_debut = min(carte_taches[sid]['debut_plus_tard'] for sid in successeurs)
            tache['fin_plus_tard'] = min_debut - 1
            tache['debut_plus_tard'] = tache['fin_plus_tard'] - tache['duree'] + 1

        tache['marge_total'] = tache['debut_plus_tard'] - tache['debut_plus_tot']

        if not successeurs:
            tache['marge_libre'] = tache['marge_total']
        else:
            min_debut_succ = min(carte_taches[sid]['debut_plus_tot'] for sid in successeurs)
            tache['marge_libre'] = (min_debut_succ - 1) - tache['fin_plus_tot']

    chemin_critique = [id for id in triee if carte_taches[id]['marge_total'] == 0]

    return {
        'taches': carte_taches,
        'T0': T0,
        'Tf': Tf,
        'duree_projet': Tf - T0 + 1,
        'chemin_critique': chemin_critique,
        'triee': triee,
    }


def tri_topologique(carte_taches):
    visites = set()
    resultat = []

    def visiter(id_tache):
        if id_tache in visites:
            return
        visites.add(id_tache)
        for id_pred in carte_taches.get(id_tache, {}).get('predecesseurs', []):
            if id_pred in carte_taches:
                visiter(id_pred)
        resultat.append(id_tache)

    for id_tache in carte_taches:
        visiter(id_tache)

    return resultat
