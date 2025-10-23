from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Voirie_Pada_V15(models.Model):
    gid = models.AutoField(primary_key=True)
    id_0 = models.FloatField(blank=True, null=True)
    id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    id_voie = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    type_voie = models.CharField(max_length=254, blank=True, null=True)
    nom_cnt = models.CharField(max_length=100, blank=True, null=True)
    voie_96 = models.CharField(max_length=100, blank=True, null=True)
    nom_osm = models.CharField(max_length=100, blank=True, null=True)
    creation = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    atelier = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    epl = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    commune = models.CharField(max_length=100, blank=True, null=True)
    zone = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    secteur = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    class_pada = models.CharField(max_length=50, blank=True, null=True)
    nom_pada = models.CharField(max_length=254, blank=True, null=True)
    new_name = models.CharField(max_length=100, blank=True, null=True)
    longueur = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cite = models.CharField(max_length=254, blank=True, null=True)
    part1 = models.CharField(max_length=100, blank=True, null=True)
    part2 = models.CharField(max_length=100, blank=True, null=True)
    part3 = models.CharField(max_length=100, blank=True, null=True)
    doublon = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    quartier = models.CharField(max_length=254, blank=True, null=True)
    source_n = models.CharField(max_length=254, blank=True, null=True)
    doubcom = models.CharField(max_length=254, blank=True, null=True)
    doub_name = models.CharField(max_length=254, blank=True, null=True)
    doub_sourc = models.CharField(max_length=254, blank=True, null=True)
    doub_cat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.


# Create your models here.
