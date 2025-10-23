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




# Liste des Suggestion
@user_passes_test(staff_check)
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
def afficher_publicite(request):
    
    pub = publicites.objects.first()  # il n’y a qu’une seule publicité
    return render(request, 'afficher_publicite.html', {'pub': pub})



#Deconnexion
def logout_view(request):
    logout(request)
    return redirect('login')  # ou le nom de ta page de connexion