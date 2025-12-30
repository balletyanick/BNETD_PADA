from django.db import models
from django.conf import settings
import os
from django.contrib.auth.models import User
# from django.contrib.gis.db import models as gis_models GDAL


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

    id_voies = models.IntegerField(null=True, blank=True)


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
    
    # Image principale
    image = models.ImageField(upload_to='publicites/images/', blank=True, null=True)
    
    # Vidéo associée
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
    


class Toponymie(models.Model):

    id_toponymie = models.AutoField(primary_key=True)

    nom_pada = models.TextField(null=True, blank=True)
    type_voie = models.TextField(null=True, blank=True)
    nouvelle_description = models.TextField(null=True, blank=True)
    statut = models.CharField(max_length=30, null=True, blank=True,)

    toponyme = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    typologie = models.TextField(null=True, blank=True)
    quartier_origine = models.TextField(null=True, blank=True)

    id_voies = models.IntegerField(null=True, blank=True)
    gid_commune = models.IntegerField(null=True, blank=True)

    date_insert = models.DateField(null=True, blank=True)
    date_modif_toponyme = models.DateField(null=True, blank=True)
    date_modif_description = models.DateField(null=True, blank=True)

    suggestion_cs = models.TextField(null=True, blank=True)
    suggestion_cca = models.TextField(null=True, blank=True)
    suggestion_mo = models.TextField(null=True, blank=True)

    validation_cs = models.BooleanField(default=False)
    validation_coord = models.BooleanField(default=False)
    validation_mo = models.BooleanField(default=False)

    categorie = models.TextField(null=True, blank=True)
    genre = models.TextField(null=True, blank=True)
    autoris_modification = models.TextField(null=True, blank=True)

    auteur_modif_toponyme = models.TextField(null=True, blank=True)
    auteur_modif_desc = models.TextField(null=True, blank=True)
    hist_desc = models.TextField(null=True, blank=True)
    hist_toponyme = models.TextField(null=True, blank=True)

    class Meta:
        db_table = '"501_siga_toponymie"'   # Schéma public par défaut
        managed = False
        permissions = [
            ("list_toponyme", "Voir List Toponyme"),
            ("list_toponyme_sans_desc", "Voir List Toponyme sans description"),
            ("ajouter_description_toponyme", "Ajouter une nouvelle description toponyme"),
            ("voir_dashboard_toponyme", "Voir Dashboard Toponyme"),
            
            ("valider_cs_topo", "Valider Par CS TOPO"),
            ("rejeter_cs_topo", "Refuser par CS TOPO"),

            ("valider_coord_topo", "Valider Par CCA TOPO"),
            ("rejeter_coord_topo", "Refuser par CCA TOPO"),

            ("valider_mo_topo", "Valider Par MO TOPO"),
            ("rejeter_mo_topo", "Refuser par MO TOPO"),

            ("voir_topo_attente_toponymie", "Voir Toponymie en attente de Tponymie"),
            ("voir_topo_attente_CS", "Voir Toponymie en attente de cs"),
            ("voir_topo_attente_CCA", "Voir Toponymie en attente de CCA"),
            ("voir_topo_attente_mo", "Voir Toponymie en attente de MO"),
            ("suggestion_topo_CS", "Ajouter Suggestion TOPO CS"),
            ("suggestion_topo_CCA", "Ajouter Suggestion TOPO CCA"),
            ("suggestion_topo_MO", "Ajouter Suggestion TOPO MO"),
            ("edit_toponyme", "Modifier un toponyme"),
        ]

    def __str__(self):
        return self.toponyme or "Toponyme"
  
    @property
    def get_statut_label(self):
        mapping = {
            "en_attente_cs": "En attente validation Chef de service",
            "en_attente_coord": "En attente validation Coordinatrice",
            "en_attente_mo": "En attente validation MO",
            "valider": "Validée définitivement",
            "aucune_modification": "Aucune modification",
            "retour_toponymie": "Retour à la Toponymie",
        }
        return mapping.get(self.statut, "Aucune modification")
    





class voirie_panneautage(models.Model):
    # Django gère automatiquement l'id en auto-increment
    geom = models.TextField(null=True, blank=True)  # SRID 32630 = UTM Zone 30N
    id_voie = models.BigIntegerField(null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    nom_cnt = models.CharField(max_length=100, null=True, blank=True)
    localisati = models.CharField(max_length=255, null=True, blank=True)
    zone = models.BigIntegerField(null=True, blank=True)
    secteur = models.BigIntegerField(null=True, blank=True)
    class_pada = models.CharField(max_length=50, null=True, blank=True)
    type_voie = models.CharField(max_length=254, null=True, blank=True)
    validé = models.BooleanField(default=False)

    class Meta:
        db_table = "voirie_panneautage"
        managed = False  # ← Si la table existe déjà dans PostGIS

    def __str__(self):
        return f"{self.nom_cnt or 'Sans nom'} - Zone {self.zone}"