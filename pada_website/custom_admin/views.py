from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from myapp.models import Voie
from myapp.models import Suggestion
from myapp.models import Probleme
from myapp.models import publicites
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import redirect
from myapp.models import publicites
from myapp.forms import PublicitesForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from myapp.forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from myapp.forms import AdminUserEditForm, AdminSetPasswordForm
from django.db.models import Q
from django.http import JsonResponse
from myapp.models import Toponymie

# Seuls les utilisateurs is_staff=True peuvent accéder
def staff_check(user):
    return user.is_staff

# Dashboard
@user_passes_test(staff_check)
def dashboard(request):
    users = User.objects.all()

    # Compteurs
    total_utilisateurs = User.objects.count()
    total_voies = Voie.objects.count()
    total_problemes = Probleme.objects.count()
    total_suggestions = Suggestion.objects.count()

    # Compteurs par statut panneautage
    voies_en_attente_cca = Voie.objects.filter(statut='en_attente_cca').count()
    voies_en_attente_mo = Voie.objects.filter(statut='en_attente_mo').count()
    voies_validees_finalement = Voie.objects.filter(statut='validee_finalement').count()

    # Compteurs par statut Toponymie
    topo_retour_toponymie = Toponymie.objects.filter(statut='retour_toponymie').count()
    topo__attente_cs = Toponymie.objects.filter(statut='en_attente_cs').count()
    topo_attente_coord = Toponymie.objects.filter(statut='en_attente_coord').count()
    topo_attente_mo = Toponymie.objects.filter(statut='en_attente_mo').count()
    topo_valider = Toponymie.objects.filter(statut='valider').count()

    context = {
        'total_utilisateurs': total_utilisateurs,
        'total_voies': total_voies,
        'total_problemes': total_problemes,
        'total_suggestions': total_suggestions,
        'voies_en_attente_cca': voies_en_attente_cca,
        'voies_en_attente_mo': voies_en_attente_mo,
        'voies_validees_finalement': voies_validees_finalement,

        'topo_retour_toponymie': topo_retour_toponymie,
        'topo__attente_cs': topo__attente_cs,
        'topo_attente_mo': topo_attente_mo,
        'topo_valider': topo_valider,
        'topo_attente_coord': topo_attente_coord,
    }
    return render(request, 'dashboard.html', context)


# Liste des Utilisateurs
@user_passes_test(staff_check)
@permission_required('myapp.view_user', login_url='login')
def users_list(request):

    query = request.GET.get("q")  # récupération du mot-clé
    users = User.objects.all().order_by("id")

    if query:
        users = users.filter(
            Q(email__icontains=query) 
        )

    paginator = Paginator(users, 50)  

    page_number = request.GET.get("page")  # récupère ?page=...
    page_obj = paginator.get_page(page_number)

    return render(request, "users_list.html", {
        "page_obj": page_obj,
        "query": query,
    })


# Liste des Voies
@user_passes_test(staff_check)
@permission_required('myapp.view_voie', login_url='login')
def voies_list(request):
   
    query = request.GET.get("q")  # récupération du mot-clé
    voies = Voie.objects.all().order_by("id")

    if query:
        voies = voies.filter(
            Q(nom_voies__icontains=query) |
            Q(id_voies__icontains=query) |
            Q(quartier__icontains=query) |
            Q(description__icontains=query) |
            Q(entites_territoriales_2__icontains=query)
        )

    paginator = Paginator(voies, 50)  # 50 enregistrements par page

    page_number = request.GET.get("page")  # récupère ?page=...
    page_obj = paginator.get_page(page_number)

    return render(request, "voies_list.html", {
        "page_obj": page_obj,
        "query": query,
    })



# Liste des Suggestion
@user_passes_test(staff_check)
@permission_required('myapp.view_suggestion', login_url='login')
def suggestion_list(request):
   
    query = request.GET.get("q")  # récupération du mot-clé
    suggestions = Suggestion.objects.all().order_by("id")

    if query:
        suggestions = suggestions.filter(
            Q(suggestion__icontains=query) |
            Q(nom_voie__icontains=query)
        )

    paginator = Paginator(suggestions, 50)  #50 enregistrements par page

    page_number = request.GET.get("page")  # récupère ?page=...
    page_obj = paginator.get_page(page_number)

    return render(request, "suggestion_list.html", {
        "page_obj": page_obj,
        "query": query,
    })




# Liste des Problèmes
@user_passes_test(staff_check)
@permission_required('myapp.view_probleme', login_url='login')
def problemes_list(request):
   
    query = request.GET.get("q")  # récupération du mot-clé
    problemes = Probleme.objects.all().order_by("id")

    if query:
        problemes = problemes.filter(
            Q(probleme__icontains=query) |
            Q(nom_voie__icontains=query)
        )

    paginator = Paginator(problemes, 50)  #50 enregistrements par page

    page_number = request.GET.get("page")  # récupère ?page=...
    page_obj = paginator.get_page(page_number)

    return render(request, "problemes_list.html", {
        "page_obj": page_obj,
        "query": query,
    })


# Page Editer une publicité
@user_passes_test(staff_check)
@permission_required('myapp.change_publicites', login_url='login')
def edit_publicite(request, id):
   
    pub = get_object_or_404(publicites, id=id)

    if request.method == 'POST':
        pub.titre = request.POST.get('titre')
        pub.description = request.POST.get('description')

        if 'image' in request.FILES:
            pub.image = request.FILES['image']
        if 'video' in request.FILES:
            pub.video = request.FILES['video']

        pub.save()
        messages.success(request, "Publicité mise à jour avec succès !")
        return redirect('afficher_publicite')  # ou autre URL

    return render(request, 'edit_publicite.html', {'pub': pub})


# Liste des publicites
@user_passes_test(staff_check)
@permission_required('myapp.view_publicites', login_url='login')
def afficher_publicite(request):
    
    pub = publicites.objects.first()  # il n’y a qu’une seule publicité
    return render(request, 'afficher_publicite.html', {'pub': pub})



#Deconnexion
def logout_view(request):
    logout(request)
    return redirect('login')  # ou le nom de ta page de connexion




# Vérifie que seul un administrateur puisse créer un utilisateur @user_passes_test(lambda u: u.is_staff or u.is_superuser)
@user_passes_test(lambda u: u.is_superuser)
@permission_required('myapp.add_user', login_url='login')
def create_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()  # pour enregistrer les groupes et permissions
            messages.success(request, f"L'utilisateur {user.username} a été créé avec succès.")
            return redirect('users_list')  
    else:
        form = CustomUserForm()
    return render(request, 'create_user.html', {'form': form})



#Supprimer Utilisateurs
@permission_required('auth.delete_user', login_url='login')
def delete_user(request, user_id):
    if request.method != 'POST':
        messages.error(request, "Méthode invalide pour la suppression.")
        return redirect('users_list')

    user_to_delete = get_object_or_404(User, id=user_id)

    if request.user == user_to_delete:
        messages.error(request, "Vous ne pouvez pas vous supprimer vous-même.")
        return redirect('users_list')

    username = user_to_delete.username
    user_to_delete.delete()
    messages.success(request, f"L'utilisateur « {username} » a été supprimé.")
    return redirect('users_list')




#Modifier Utilisateurs
@user_passes_test(lambda u: u.is_superuser, login_url='login')
def edit_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    def would_remove_last_superuser(post_data):
        # si on tente de désactiver is_superuser pour cet utilisateur
        new_is_super = post_data.get('is_superuser') == 'on'
        if user_obj.is_superuser and not new_is_super:

            other_super_count = User.objects.filter(is_superuser=True).exclude(id=user_obj.id).count()
            return other_super_count == 0
        return False

    if request.method == 'POST':
        if 'save_user' in request.POST:
            if would_remove_last_superuser(request.POST):
                messages.error(request, "Impossible de retirer le statut superutilisateur — il doit rester au moins un superutilisateur.")
                return redirect('edit_user', user_id=user_obj.id)

            form = AdminUserEditForm(request.POST, instance=user_obj)
            if form.is_valid():
                form.save()
                messages.success(request, f"Utilisateur « {user_obj.username} » mis à jour.")

                return redirect('users_list')
            else:
                messages.error(request, "Erreur dans le formulaire. Vérifiez les champs.")
                pw_form = AdminSetPasswordForm(user_obj)  # pour réafficher
        elif 'change_password' in request.POST:
            pw_form = AdminSetPasswordForm(user_obj, request.POST)
            form = AdminUserEditForm(instance=user_obj)  # pour afficher
            if pw_form.is_valid():
                pw_form.save()
                messages.success(request, f"Mot de passe de « {user_obj.username} » mis à jour.")
                return redirect('users_list')
            else:
                messages.error(request, "Erreur dans le formulaire de mot de passe.")
        else:
            # requête POST non reconnue
            return redirect('users_list')
    else:
        form = AdminUserEditForm(instance=user_obj)
        pw_form = AdminSetPasswordForm(user_obj)

    context = {
        'form': form,
        'pw_form': pw_form,
        'user_obj': user_obj,
    }
    return render(request, 'edit_user.html', context)



#Editer description de voie
@permission_required('myapp.change_voie', login_url='login')
def edit_voies(request, voie_id):
    voie = get_object_or_404(Voie, id=voie_id)

    if request.method == 'POST':
        nouvelle_description = request.POST.get('description')
        voie.description = nouvelle_description
        voie.save()
        messages.success(request, "Description mise à jour avec succès ")
        return redirect('voies_list')

    context = {
        'voie': voie,
    }
    return render(request, 'edit_voies.html', context)


# Voir le dashboard d'une voie
@permission_required('myapp.view_dashboard_voies', login_url='login')
def dashboard_voies(request, voie_id):
    voie = get_object_or_404(Voie, id=voie_id)

    return render(request, 'dashboard_voies.html', {'voie': voie})


# Valider une nouvelle description par le CCA
def valider_cca(request, voie_id):
    voie = get_object_or_404(Voie, id=voie_id)
    
    if request.method == 'POST':
        voie.statut = 'en_attente_mo'
        voie.date_derniere_modification = timezone.now()
        voie.save()
        messages.success(request, f"La voie '{voie.nom_voies}' a été validée par la CCA. En attente de validation MO.")

        # Si c’est une requête AJAX → renvoyer un signal de redirection
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'redirect_url': '/p_bnetd25/suggestion_voie_list/'})
        
        # Sinon, rediriger normalement
        return redirect('suggestion_voie_list')
    return JsonResponse({'error': 'Méthode non autorisée'}, status=400)



# Rejeter une nouvelle description par le CCA
def rejeter_cca(request, voie_id):

    voie = get_object_or_404(Voie, id=voie_id)

    if request.method == 'POST':
        voie.statut = 'retour_toponymie'
        voie.date_derniere_modification = timezone.now()
        voie.save()
        messages.warning(request, f"La voie '{voie.nom_voies}' a été renvoyée à la Toponymie.")

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'redirect_url': '/p_bnetd25/suggestion_voie_list/'})
        return redirect('suggestion_voie_list')
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=400)


# Ajouter une nouvelle description pour commencer le processus
@permission_required('myapp.can_add_suggestion_voie', login_url='login')
def ajouter_suggestion_voie(request, voie_id):
    voie = get_object_or_404(Voie, id=voie_id)

    if request.method == 'POST':
        nouvelle_description = request.POST.get('description_proposee')
        if nouvelle_description:
            voie.description_proposee = nouvelle_description
            voie.statut = 'en_attente_cca'  # verrouille la voie pour Toponymie
            voie.date_derniere_modification = timezone.now()
            voie.save()
            messages.success(request, "Proposition envoyée, en attente de validation CCA.")
            return redirect('suggestion_voie_list')  # retourne vers la page de liste
        else:
            messages.warning(request, "Veuillez saisir une description.")

    return render(request, 'ajouter_suggestion_voie.html', {'voie': voie})



# Liste des suggestions voies 
@permission_required('myapp.voir_suggestion_voie', login_url='login')
def suggestion_voie_list(request):
   
    query = request.GET.get("q")  # récupération du mot-clé
    voies = Voie.objects.all().order_by("id")

    if query:
        voies = voies.filter(
            Q(nom_voies__icontains=query) |
            Q(id_voies__icontains=query) |
            Q(quartier__icontains=query) |
            Q(description__icontains=query) |
            Q(entites_territoriales_2__icontains=query)
        )

    paginator = Paginator(voies, 50)  # 50 enregistrements par page

    page_number = request.GET.get("page")  # récupère ?page=...
    page_obj = paginator.get_page(page_number)

    return render(request, "suggestion_voie_list.html", {
        "page_obj": page_obj,
        "query": query,
    })



# Liste des suggestions voies en attente de validation du CCA
@permission_required('myapp.voir_suggestion_voie', login_url='login')
def suggestion_voie_list_en_attente_cca(request):
   
    query = request.GET.get("q")  # récupération du mot-clé
    voies = Voie.objects.filter(statut='en_attente_cca').order_by('id')

    if query:
        voies = voies.filter(
            Q(nom_voies__icontains=query) |
            Q(quartier__icontains=query) |
            Q(description__icontains=query) |
            Q(entites_territoriales_2__icontains=query)
        )

    paginator = Paginator(voies, 50)  # 50 enregistrements par page

    page_number = request.GET.get("page")  # récupère ?page=...
    page_obj = paginator.get_page(page_number)

    return render(request, "suggestion_voie_list.html", {
        "page_obj": page_obj,
        "query": query,
    })



# Liste des suggestions voies en attente de validation du MO
@permission_required('myapp.voir_suggestion_voie', login_url='login')
def suggestion_voie_list_en_attente_mo(request):
   
    query = request.GET.get("q")  # récupération du mot-clé
    voies = Voie.objects.filter(statut='en_attente_mo').order_by('id')

    if query:
        voies = voies.filter(
            Q(nom_voies__icontains=query) |
            Q(quartier__icontains=query) |
            Q(description__icontains=query) |
            Q(entites_territoriales_2__icontains=query)
        )

    paginator = Paginator(voies, 50)  # 50 enregistrements par page

    page_number = request.GET.get("page")  
    page_obj = paginator.get_page(page_number)

    return render(request, "suggestion_voie_list.html", {
        "page_obj": page_obj,
        "query": query,
    })


# Ajouter une suggestion par le CCA
def ajouter_suggestion_cca(request, voie_id):
    voie = get_object_or_404(Voie, id=voie_id)
    
    if request.method == 'POST':
        suggestion = request.POST.get('suggestion_cca')
        if suggestion:
            voie.suggestion_cca = suggestion
            voie.date_derniere_modification = timezone.now()
            voie.save()
            messages.success(request, f"Suggestion ajoutée avec succès pour la voie « {voie.nom_voies} ».")
        else:
            messages.warning(request, "Veuillez entrer une suggestion avant d’envoyer.")
    
    return redirect('suggestion_voie_list')


# Ajouter une suggestion par le MO
def ajouter_suggestion_mo(request, voie_id):
    voie = get_object_or_404(Voie, id=voie_id)
    
    if request.method == 'POST':
        suggestion = request.POST.get('suggestion_mo')
        if suggestion:
            voie.suggestion_mo = suggestion
            voie.date_derniere_modification = timezone.now()
            voie.save()
            messages.success(request, f"Suggestion du MO ajoutée avec succès pour la voie « {voie.nom_voies} ».")
        else:
            messages.warning(request, "Veuillez entrer une suggestion avant d’envoyer.")
    
    return redirect('suggestion_voie_list')


# Validation par le MO
def valider_mo(request, voie_id):
    voie = get_object_or_404(Voie, id=voie_id)

    # Si une nouvelle description a été proposée, elle devient la description officielle
    if voie.description_proposee:
        voie.description = voie.description_proposee

    voie.statut = 'validee_finalement'
    voie.date_derniere_modification = timezone.now()
    voie.save()

    messages.success(
        request,
        f"La voie « {voie.nom_voies} » a été validée définitivement. La nouvelle description a été enregistrée."
    )

    return JsonResponse({'redirect_url': '/p_bnetd25/suggestion_voie_list/'})



# Rejet par le MO
def rejeter_mo(request, voie_id):
    voie = get_object_or_404(Voie, id=voie_id)
    voie.statut = 'retour_toponymie'
    voie.date_derniere_modification = timezone.now()
    voie.save()
    messages.warning(request, f"La voie « {voie.nom_voies} » a été renvoyée à la Toponymie.")
    return JsonResponse({'redirect_url': '/p_bnetd25/suggestion_voie_list/'})




# Liste des toponymes
def toponyme_list(request):
   
    query = request.GET.get("q")  # récupération du mot-clé
    topo = Toponymie.objects.all().order_by('id_toponymie')

    if query:
        topo = topo.filter(
          Q(nom_pada__icontains=query) |
            Q(description__icontains=query) |
            Q(type_voie__icontains=query) |
            Q(quartier_origine__icontains=query) |
            Q(id_voies__icontains=query) |
            Q(gid_commune__icontains=query)
        )

    paginator = Paginator(topo, 50)  # 50 enregistrements par page

    page_number = request.GET.get("page")  # récupère ?page=...
    page_obj = paginator.get_page(page_number)

    return render(request, "toponymie_list.html", {
        "page_obj": page_obj,
        "query": query,
    })

# Liste des toponymes en attente pour toponymie
def topo_attente_topo(request):
   
    query = request.GET.get("q")  # récupération du mot-clé
    topo = Toponymie.objects.filter(statut='retour_toponymie').order_by('id_toponymie')

    if query:
        topo = topo.filter(
          Q(nom_pada__icontains=query) |
            Q(description__icontains=query) |
            Q(type_voie__icontains=query) |
            Q(quartier_origine__icontains=query) |
            Q(id_voies__icontains=query) |
            Q(gid_commune__icontains=query)
        )

    paginator = Paginator(topo, 50)  # 50 enregistrements par page

    page_number = request.GET.get("page")  # récupère ?page=...
    page_obj = paginator.get_page(page_number)

    return render(request, "toponymie_list.html", {
        "page_obj": page_obj,
        "query": query,
    })


# Liste des toponymes en attente pour CS
def topo_attente_cs(request):
   
    query = request.GET.get("q")  # récupération du mot-clé
    topo = Toponymie.objects.filter(statut='en_attente_cs').order_by('id_toponymie')

    if query:
        topo = topo.filter(
          Q(nom_pada__icontains=query) |
            Q(description__icontains=query) |
            Q(type_voie__icontains=query) |
            Q(quartier_origine__icontains=query) |
            Q(id_voies__icontains=query) |
            Q(gid_commune__icontains=query)
        )

    paginator = Paginator(topo, 50)  # 50 enregistrements par page

    page_number = request.GET.get("page")  # récupère ?page=...
    page_obj = paginator.get_page(page_number)

    return render(request, "toponymie_list.html", {
        "page_obj": page_obj,
        "query": query,
    })



# Liste des toponymes en attente pour COORD
def topo_attente_coord(request):
   
    query = request.GET.get("q")  # récupération du mot-clé
    topo = Toponymie.objects.filter(statut='en_attente_coord').order_by('id_toponymie')

    if query:
        topo = topo.filter(
          Q(nom_pada__icontains=query) |
            Q(description__icontains=query) |
            Q(type_voie__icontains=query) |
            Q(quartier_origine__icontains=query) |
            Q(id_voies__icontains=query) |
            Q(gid_commune__icontains=query)
        )

    paginator = Paginator(topo, 50)  # 50 enregistrements par page

    page_number = request.GET.get("page")  # récupère ?page=...
    page_obj = paginator.get_page(page_number)

    return render(request, "toponymie_list.html", {
        "page_obj": page_obj,
        "query": query,
    })




# Liste des toponymes en attente pour MO
def topo_attente_mo(request):
   
    query = request.GET.get("q")  # récupération du mot-clé
    topo = Toponymie.objects.filter(statut='en_attente_mo').order_by('id_toponymie')

    if query:
        topo = topo.filter(
          Q(nom_pada__icontains=query) |
            Q(description__icontains=query) |
            Q(type_voie__icontains=query) |
            Q(quartier_origine__icontains=query) |
            Q(id_voies__icontains=query) |
            Q(gid_commune__icontains=query)
        )

    paginator = Paginator(topo, 50)  # 50 enregistrements par page

    page_number = request.GET.get("page")  # récupère ?page=...
    page_obj = paginator.get_page(page_number)

    return render(request, "toponymie_list.html", {
        "page_obj": page_obj,
        "query": query,
    })



# Voir le dashboard de la toponymie d'une voie
def dashboard_topo(request, topo_id):
    topo = get_object_or_404(Toponymie, id_toponymie=topo_id)
    return render(request, 'dashboard_topo.html', {'topo': topo})


# Ajouter une nouvelle description toponymie
def ajouter_nouvelle_description(request, topo_id):
    topo = get_object_or_404(Toponymie, id_toponymie=topo_id)

    if request.method == "POST":
        nouvelle_desc = request.POST.get("nouvelle_description")
        topo.nouvelle_description = nouvelle_desc
        topo.statut = 'en_attente_cs'
        topo.save()

        messages.success(request, "Nouvelle description enregistrée.")
        return redirect('toponymie_list')

    return render(request, "ajouter_nouvelle_description.html", {"topo": topo})


# Valider CS toponymie
def valider_cs(request, topo_id):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    topo = get_object_or_404(Toponymie, id_toponymie=topo_id)

    topo.validation_cs = True
    topo.statut = 'en_attente_coord'
    topo.save()

    messages.success(
        request,
        f"La proposition pour « {topo.nom_pada} » a été validée avec succès."
    )

    return JsonResponse({"redirect_url": "/p_bnetd25/toponymie/"})


# Rejeter CS toponymie
def rejeter_cs(request, topo_id):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    topo = get_object_or_404(Toponymie, id_toponymie=topo_id)

    topo.validation_cs = False
    topo.statut = 'retour_toponymie'
    topo.save()

    messages.error(
        request,
        f"La proposition pour « {topo.nom_pada} » a été rejetée."
    )

    return JsonResponse({
        "redirect_url": "/p_bnetd25/toponymie/"
    })



# Valider CCA toponymie
def valider_coord(request, topo_id):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    topo = get_object_or_404(Toponymie, id_toponymie=topo_id)

    topo.validation_coord = True
    topo.statut = 'en_attente_mo'
    topo.save()

    messages.success(
        request,
        f"La proposition pour « {topo.nom_pada} » a été validée par la Cellule de la Centrale d’Adressage (COORD)."
    )

    return JsonResponse({"redirect_url": "/p_bnetd25/toponymie/"})



# Rejeter CCA toponymie
def rejeter_coord(request, topo_id):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    topo = get_object_or_404(Toponymie, id_toponymie=topo_id)

    topo.validation_coord = False
    topo.validation_cs = False
    topo.statut = 'retour_toponymie'
    topo.save()

    messages.error(
        request,
        f"La proposition pour « {topo.nom_pada} » a été rejetée par la Cellule de la Centrale d’Adressage (COORD)."
    )

    return JsonResponse({"redirect_url": "/p_bnetd25/toponymie/"})



# Valider MO toponymie
def validation_mo_topo(request, topo_id):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    topo = get_object_or_404(Toponymie, id_toponymie=topo_id)

    topo.validation_mo = True
    topo.description = topo.nouvelle_description
    topo.statut = 'valider'
    topo.save()

    messages.success(
        request,
        f"La proposition pour « {topo.nom_pada} » a été validée par le Maitre d'Ouvrage"
    )

    return JsonResponse({"redirect_url": "/p_bnetd25/toponymie/"})



# Rejeter MO toponymie
def reject_mo_topo(request, topo_id):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    topo = get_object_or_404(Toponymie, id_toponymie=topo_id)

    topo.validation_mo = False
    topo.validation_cs = False
    topo.validation_coord = False
    topo.statut = 'retour_toponymie'
    topo.save()

    messages.error(
        request,
        f"La proposition pour « {topo.nom_pada} » a été rejetée par par le Maitre d'Ouvrage"
    )

    return JsonResponse({"redirect_url": "/p_bnetd25/toponymie/"})



# Ajouter une suggestion par le MO
def ajouter_suggestion_mo_topo(request, voie_id):
    topo = get_object_or_404(Toponymie, id_toponymie=voie_id)
    
    if request.method == 'POST':
        suggestion = request.POST.get('suggestion_mo')
        if suggestion:
            topo.suggestion_mo = suggestion
            topo.validation_mo = False
            topo.validation_cs = False
            topo.validation_coord = False

            topo.statut = 'retour_toponymie'
            topo.save()
            messages.success(request, f"Suggestion du MO ajoutée avec succès pour la voie « {topo.nom_pada} ».")
        else:
            messages.warning(request, "Veuillez entrer une suggestion avant d’envoyer.")
    
    return redirect('toponymie_list')


# Ajouter une suggestion par le MO
def ajouter_suggestion_cs_topo(request, voie_id):
    topo = get_object_or_404(Toponymie, id_toponymie=voie_id)
    
    if request.method == 'POST':
        suggestion = request.POST.get('suggestion_cs')
        if suggestion:
            topo.suggestion_cs = suggestion
            topo.validation_cs = False
            topo.statut = 'retour_toponymie'
            topo.save()
            messages.success(request, f"Suggestion du MO ajoutée avec succès pour la voie « {topo.nom_pada} ».")
        else:
            messages.warning(request, "Veuillez entrer une suggestion avant d’envoyer.")
    
    return redirect('toponymie_list')



# Ajouter une suggestion par le MO
def ajouter_suggestion_cca_topo(request, voie_id):
    topo = get_object_or_404(Toponymie, id_toponymie=voie_id)
    
    if request.method == 'POST':
        suggestion = request.POST.get('suggestion_cca')
        if suggestion:
            topo.validation_coord = False
            topo.validation_cs = False
            topo.statut = 'retour_toponymie'
            topo.save()
            messages.success(request, f"Suggestion du MO ajoutée avec succès pour la voie « {topo.nom_pada} ».")
        else:
            messages.warning(request, "Veuillez entrer une suggestion avant d’envoyer.")
    
    return redirect('toponymie_list')







