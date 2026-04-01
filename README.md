# Diagramme PERT - Django

Application de gestion de projets et génération de diagrammes PERT, convertie de Laravel vers Django.

## Installation

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer les migrations et la base de données
python manage.py makemigrations pert_app
python manage.py migrate

# 4. (Optionnel) Créer un compte admin
python manage.py createsuperuser

# 5. Lancer le serveur
python manage.py runserver
```

Accéder à l'application : http://127.0.0.1:8000/projets/

## Structure du projet

```
diagramme_pert_django/
├── manage.py
├── requirements.txt
├── diagramme_pert/          # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── pert_app/                # Application principale
    ├── models.py            # Modèles Projet et Tache
    ├── views.py             # Vues + algorithme PERT
    ├── forms.py             # Formulaires
    ├── urls.py              # Routes
    ├── admin.py
    ├── templatetags/
    │   └── pert_tags.py     # Filtre get_item pour les templates
    └── templates/pert_app/
        ├── base.html
        ├── projets/
        │   ├── index.html
        │   ├── afficher.html
        │   ├── creer.html
        │   └── modifier.html
        └── pert/
            └── diagram.html
```

## Fonctionnalités

- Créer, modifier et supprimer des projets
- Ajouter des tâches avec durée et prédécesseurs
- Calcul automatique du diagramme PERT :
  - Dates au plus tôt / au plus tard
  - Marges libres et totales
  - Chemin critique
- Visualisation canvas interactive
- Téléchargement du diagramme en PNG
- Tableau détaillé des tâches

## Correspondance Laravel → Django

| Laravel | Django |
|---|---|
| Eloquent Models | Django ORM Models |
| Migrations PHP | Migrations Django |
| Blade Templates | Django Templates |
| Route::get/post | path() dans urls.py |
| @csrf / @method | {% csrf_token %} |
| session('succes') | messages.success() |
| $requete->validate() | ModelForm |
| compact('var') | {'var': var} |
| $projet->taches | projet.taches.all() |
