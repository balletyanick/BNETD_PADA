from django.db import models
from django.conf import settings
import os
from django.contrib.auth.models import User


class Voie(models.Model):
    id = models.AutoField(primary_key=True)
    nom_voies = models.CharField(max_length=255)
    quartier = models.CharField(max_length=255)
    X = models.CharField(max_length=255)
    Y = models.CharField(max_length=255)
    qr_code = models.TextField(unique=True)
    description = models.CharField(max_length=255)
    entites_territoriales_2 = models.TextField()
    photo_personnalite = models.CharField(max_length=255, null=True, blank=True)

    # --- Nouveaux champs pour le processus de validation ---
    description_proposee = models.TextField(null=True, blank=True)
    suggestion_cca = models.TextField(null=True, blank=True)
    suggestion_mo = models.TextField(null=True, blank=True)

    STATUT_CHOICES = [
        ('aucune_modification', 'Aucune modification'),
        ('en_attente_cca', 'En attente de validation CCA'),
        ('en_attente_mo', 'En attente de validation MO'),
        ('retour_toponymie', 'Retour à Toponymie'),
        ('validee_finalement', 'Validée définitivement'),
        ('rejete', 'Rejetée'),
    ]

    statut = models.CharField(
        max_length=30,
        choices=STATUT_CHOICES,
        null=True,
        blank=True,
        default='aucune_modification'
    )

    date_derniere_modification = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'panneautage'
        managed = False
        permissions = [
            ("view_dashboard_voies", "Voir Dashboard Voies"),
            ("can_add_suggestion_voie", "Peut ajouter une nouvelle description de voie"),

            ("valider_cca", "Valider Par CCA"),
            ("rejeter_cca", "Refuser par CCA"),
            ("ajouter_suggestion_cca", "Ajouter suggestion Par CCA"),

            ("valider_mo", "Valider Par MO"),
            ("rejeter_mo", "Refuser Par MO"),
            ("ajouter_suggestion_mo", "Ajouter suggestion Par MO"),

            ("voir_suggestion_voie", "Voir suggestion voie"),
            ("voir_suggestion_voie_attent_mo", "Voir suggestion voie attente MO"),
            ("voir_suggestion_voie_attente_cca", "Voir suggestion voie en attente CCA"),
        ]

    def __str__(self):
        return f"{self.nom_voies} - {self.quartier}"
    
    @property
    def has_personnalite_photo(self):
        """Vérifie si une photo est associée"""
        return bool(self.photo_personnalite)
    
    def get_absolute_photo_url(self):
        """
        Génère l'URL complète de la photo selon le format souhaité :
        /code_panneau/media/chemin_photo
        """
        if not self.photo_personnalite:
            return None    
        # Si c'est déjà une URL complète
        if self.photo_personnalite.startswith(('http://', 'https://')):
            return self.photo_personnalite   
        # Nettoyage du code QR pour l'URL
        qr_code = self.qr_code.replace('https://panneautage.bnetd.ci/', '').strip('/')
        
        # Construction de l'URL selon votre format demandé
        return f"/{qr_code}/media/{self.photo_personnalite.lstrip('/')}"
    
    @property
    def has_personnalite_photo(self):
        """Vérifie si une photo existe"""
        return bool(self.photo_personnalite)
    
    @property
    def clean_qr_code(self):
        """
        Retourne le code propre sans le domaine.
        Exemple :
        'https://panneautage.bnetd.ci/00212P11789' devient '00212P11789'
        """
        return self.qr_code.replace('https://panneautage.bnetd.ci/', '').strip('/')

 
   
class Suggestion(models.Model):
    voie = models.ForeignKey(
        Voie,
        on_delete=models.CASCADE,
        related_name='suggestions',
        db_column='voie_id'
    )
    nom_voie = models.CharField(max_length=255)
    qr_code_url = models.TextField()
    suggestion = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'suggestions'
        managed = False

    def save(self, *args, **kwargs):
        if not self.pk:  # Seulement lors du premier enregistrement
            if self.voie:
                self.nom_voie = self.voie.nom_voies
                self.qr_code_url = self.voie.qr_code
        super().save(*args, **kwargs)



class Probleme(models.Model):
    voie = models.ForeignKey(
        'Voie',
        on_delete=models.CASCADE,
        related_name='problemes',
        db_column='voie_id'
    )
    nom_voie = models.CharField(max_length=255)
    qr_code_url = models.TextField()
    nom_complet = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    probleme = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_signalement = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'problemes'
        managed = True  # ⚠️ si la table existe déjà, sinon mets True

    def save(self, *args, **kwargs):
        if not self.pk and self.voie:
            self.nom_voie = self.voie.nom_voies
            self.qr_code_url = self.voie.qr_code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Problème sur {self.nom_voie} ({self.probleme})"
    



class publicites(models.Model):
    titre = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    # 🖼️ Image principale
    image = models.ImageField(upload_to='publicites/images/', blank=True, null=True)
    
    # 🎥 Vidéo associée
    video = models.FileField(upload_to='publicites/videos/', blank=True, null=True)
    
    # Type de média principal (optionnel si tu veux classer)
    type_media = models.CharField(
        max_length=10,
        choices=(('image', 'Image'), ('video', 'Vidéo')),
        blank=True,
        null=True
    )

    # Date d’ajout automatique
    date_ajout = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'publicites'  # nom de la table dans PostgreSQL

    def __str__(self):
        return self.titre or "Média sans titre"

    # Vérifications rapides
    def has_image(self):
        return bool(self.image)

    def has_video(self):
        return bool(self.video)
    






