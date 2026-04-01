from django.db import models
import json


class Projet(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    t0 = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.nom


class Tache(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='taches')
    id_tache = models.CharField(max_length=10)
    nom = models.CharField(max_length=255)
    duree = models.IntegerField()
    predecesseurs = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id_tache']

    def __str__(self):
        return f"{self.id_tache} - {self.nom}"
