from django.http import JsonResponse,Http404
from django.views.decorators.http import require_POST
from .models import Probleme, Voie
from .forms import SuggestionForm
from django.http import FileResponse
import os
from django.conf import settings
import requests
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProblemeForm
from django.http import JsonResponse
from myapp.models import Toponymie
import json
from django.db import connection

# Page 404
def custom_404(request, exception):
    return render(request, '404.html', status=404)


def voie_geojson(request, voie_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ST_AsGeoJSON(ST_Transform(v.geom, 4326))
            FROM voirie_panneautage v
            WHERE v.id_voie = %s
        """, [voie_id])

        row = cursor.fetchone()

    if not row or not row[0]:
        return JsonResponse({"error": "Voie non trouvée"}, status=404)

    return JsonResponse({
        "type": "Feature",
        "geometry": json.loads(row[0]),
        "properties": {
            "name": "voie"
        }
    })


def home_view(request, qr_code):

    cleaned_qr = qr_code.replace('https://panneautage.bnetd.ci/', '').strip()
    full_qr_code = f"https://panneautage.bnetd.ci/{cleaned_qr}"

    # Récupération de la voie
    voie = get_object_or_404(Voie, qr_code=full_qr_code)

    # Récupérer la ligne toponymie correspondante (si elle existe)
    topo = Toponymie.objects.filter(id_voies=voie.id_voies).first()

    # Fonction utilitaire: renvoie valeur topo OU valeur voie
    def prefer(topo_value, voie_value):
        if topo_value is None:
            return voie_value
        if isinstance(topo_value, str) and topo_value.strip() == "":
            return voie_value
        return topo_value

    context = {
        # description : priorité toponymie
        'description_rue': prefer(
            topo.description if topo else None,
            voie.description
        ),

        # nom : priorité nom_pada de toponymie
        'nom_rue': prefer(
            topo.nom_pada if topo else None,
            voie.nom_voies
        ),

        # quartier : priorité quartier_origine
        'quartier_rue': prefer(
            topo.quartier_origine if topo else None,
            voie.quartier
        ),

        # commune : priorité gid_commune
        'commune_rue': prefer(
            topo.gid_commune if topo else None,
            voie.entites_territoriales_2
        ),

        # Ce qui reste ne change pas
        'x': voie.X,
        'y': voie.Y,
        'qr_code': cleaned_qr,
        'photo_personnalite': voie.get_absolute_photo_url(),
        'has_personnalite_photo': voie.has_personnalite_photo,
        'voie': voie,
        'voie_id': voie.id_voies,
    }

    return render(request, 'home.html', context)



def redirect_view(request):
    # Logique de la vue de redirection
    return redirect('map')

 
@require_POST
def submit_suggestion(request, qr_code):
    # Vérification du CAPTCHA en premier
    # recaptcha_response = request.POST.get('g-recaptcha-response')
    # if not recaptcha_response:
    #     return JsonResponse({
    #         'status': 'error',
    #         'message': 'Veuillez compléter le CAPTCHA'
    #     }, status=400)

    # # Validation avec l'API Google reCAPTCHA
    # data = {
    #     'secret': settings.RECAPTCHA_PRIVATE_KEY,
    #     'response': recaptcha_response
    # }
    # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    # result = r.json()
    
    # if not result.get('success'):
    #     return JsonResponse({
    #         'status': 'error',
    #         'message': 'Validation CAPTCHA échouée. Veuillez réessayer.'
    #     }, status=400)

    # Suite du traitement original si CAPTCHA valide
    qr_code = qr_code.replace('https://panneautage.bnetd.ci/', '')
    full_qr_code = f"https://panneautage.bnetd.ci/{qr_code}"
    
    try:
        voie = get_object_or_404(Voie, qr_code=full_qr_code)
    except Voie.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Voie not found'}, status=404)
    
    form = SuggestionForm(request.POST)
    
    if form.is_valid():
        suggestion = form.save(commit=False)
        suggestion.voie = voie
        suggestion.save()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


def serve_personnalite_photo(request, qr_code, photo_path):
    # Validez que le QR code correspond à un panneau existant
    voie = get_object_or_404(Voie, qr_code=f"https://panneautage.bnetd.ci/{qr_code}")
    
    # Chemin complet du fichier
    file_path = os.path.join(settings.MEDIA_ROOT, photo_path)
    
    # Vérifiez que le fichier existe et est dans le bon dossier
    if not os.path.exists(file_path) or not file_path.startswith(settings.MEDIA_ROOT):
        raise Http404("Photo non trouvée")
    
    return FileResponse(open(file_path, 'rb'))


# Signaler un problème
# def signaler_probleme(request):
#     return render(request, 'signaler_probleme.html')




# def signaler_probleme(request, qr_code):
    
#     qr_code_clean = qr_code.strip('/')  # on nettoie le code
#     voie = get_object_or_404(Voie, qr_code__icontains=qr_code_clean)

    

#     if request.method == 'POST':
#         form = ProblemeForm(request.POST)
#         if form.is_valid():
#             probleme = form.save(commit=False)
#             probleme.voie = voie
#             probleme.save()
#             return render(request, 'signalement_succes.html', {'voie': voie})
#     else:
#         form = ProblemeForm()

#     return render(request, 'signaler_probleme.html', {
#         'form': form,
#         'voie': voie
#     })






def signaler_probleme(request, qr_code):
    qr_code_clean = qr_code.strip('/')  # on nettoie le code
    # qr_code_clean = qr_code.replace('https://panneautage.bnetd.ci/', '').strip('/')
    voie = get_object_or_404(Voie, qr_code__icontains=qr_code_clean)

    if request.method == 'POST':
        nom_complet = request.POST.get('name')
        telephone = request.POST.get('phone')
        probleme = request.POST.get('probleme')  # Ton <select> a name="cars"
        description = request.POST.get('description', '')

        # Validation simple
        if not nom_complet or not telephone or not probleme:
            return JsonResponse({'status': 'error', 'message': 'Tous les champs obligatoires doivent être remplis.'})

        # Sauvegarde du problème
        Probleme.objects.create(
            voie=voie,
            nom_voie=voie.nom_voies,
            qr_code_url=voie.qr_code,
            nom_complet=nom_complet,
            telephone=telephone,
            probleme=probleme,
            description=description
        )

        return JsonResponse({'status': 'success', 'message': 'Problème signalé avec succès !'})

    return render(request, 'signaler_probleme.html', {'voie': voie})



    