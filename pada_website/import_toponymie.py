import pandas as pd
import os
import django
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from myapp.models import Toponymie  


def nettoyer_toponyme(nom):
    if not isinstance(nom, str):
        return nom
    nom = re.sub(r"\bAVENUE\b", "", nom, flags=re.IGNORECASE)
    nom = re.sub(r"\bBOULEVARD\b", "", nom, flags=re.IGNORECASE)
    return nom.strip()


def normaliser_genre(val):
    if not isinstance(val, str):
        return None
    
    val = val.strip().lower()
    if val == "m":
        return "M"
    
    if val == "f":
        return "F"
    
    if val == "concept":
        return "Concept"
    
    if val == "CONCEPT":
        return "Concept"
    
    return None


def importer_toponymie():
    path_excel = r"C:\Users\Yanick\Documents\Description_topo.xlsx"

    print("Lecture du fichier Excel :", path_excel)

    df = pd.read_excel(path_excel, sheet_name="AVENUE")

    print("Importation en base...")

    for index, row in df.iterrows():
        toponyme_nettoye = nettoyer_toponyme(row.get("NOM PADA"))

        Toponymie.objects.update_or_create(
            id_voies=row.get("IDENTIFIANT"),
            defaults={
                "nom_pada": row.get("NOM PADA"),
                "id_voies": row.get("IDENTIFIANT"),
                "genre": normaliser_genre(row.get("GENRE")),
                "type_voie": row.get("TYPE DE VOIE"),
                "description": row.get("DESCRIPTION"),
                "typologie": row.get("TYPOLOGIE"),
                "toponyme": toponyme_nettoye,
            }
        )

    print("Import terminé !")


if __name__ == "__main__":
    importer_toponymie()
