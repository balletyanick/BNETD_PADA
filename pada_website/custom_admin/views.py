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

    context = {
        'total_utilisateurs': total_utilisateurs,
        'total_voies': total_voies,
        'total_problemes': total_problemes,
        'total_suggestions': total_suggestions,
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
            Q(quartier__icontains=query) |
            Q(description__icontains=query) |
            Q(entites_territoriales_2__icontains=query)
        )

    paginator = Paginator(voies, 50)  # 👉 10 enregistrements par page

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
            return redirect('users_list')  # à créer plus bas
    else:
        form = CustomUserForm()
    return render(request, 'create_user.html', {'form': form})



#Supprimer Utilisateurs
@permission_required('auth.delete_user', login_url='login')
def delete_user(request, user_id):
    # Seule la méthode POST doit supprimer
    if request.method != 'POST':
        messages.error(request, "Méthode invalide pour la suppression.")
        return redirect('users_list')

    user_to_delete = get_object_or_404(User, id=user_id)

    # Empêcher un admin de se supprimer lui-même (optionnel mais recommandé)
    if request.user == user_to_delete:
        messages.error(request, "Vous ne pouvez pas vous supprimer vous-même.")
        return redirect('users_list')

    username = user_to_delete.username
    user_to_delete.delete()
    messages.success(request, f"L'utilisateur « {username} » a été supprimé.")
    return redirect('users_list')




@user_passes_test(lambda u: u.is_superuser, login_url='login')
def edit_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    # Protection : empêcher de retirer le dernier superuser
    def would_remove_last_superuser(post_data):
        # si on tente de désactiver is_superuser pour cet utilisateur
        new_is_super = post_data.get('is_superuser') == 'on'
        if user_obj.is_superuser and not new_is_super:
            # combien de superusers actifs autres que celui-ci ?
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
                # groups & user_permissions m2m déjà gérés par form.save_m2m() si commit=False used;
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