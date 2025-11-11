from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    

    path("users/", views.users_list, name="users_list"),
    path('utilisateurs/supprimer/<int:user_id>/', views.delete_user, name='delete_user'),
    path('utilisateurs/editer/<int:user_id>/', views.edit_user, name='edit_user'),
    path('utilisateurs_ajouter/', views.create_user, name='create_user'),


    path('voies/', views.voies_list, name='voies_list'),
    path('edit_voies/<int:voie_id>/', views.edit_voies, name='edit_voies'),

    path('dashboard_voies/<int:voie_id>/', views.dashboard_voies, name='dashboard_voies'),
    
    path('valider_cca/<int:voie_id>/', views.valider_cca, name='valider_cca'),
    path('rejeter_cca/<int:voie_id>/', views.rejeter_cca, name='rejeter_cca'),
    path('ajouter_suggestion_cca/<int:voie_id>/', views.ajouter_suggestion_cca, name='ajouter_suggestion_cca'),

    path('valider_mo/<int:voie_id>/', views.valider_mo, name='valider_mo'),
    path('rejeter_mo/<int:voie_id>/', views.rejeter_mo, name='rejeter_mo'),
    path('ajouter_suggestion_mo/<int:voie_id>/', views.ajouter_suggestion_mo, name='ajouter_suggestion_mo'),


    path('suggestion_voie_list/', views.suggestion_voie_list, name='suggestion_voie_list'),
    path('suggestion_voie_list_en_attente_cca/', views.suggestion_voie_list_en_attente_cca, name='suggestion_voie_list_en_attente_cca'),
    path('suggestion_voie_list_en_attente_mo/', views.suggestion_voie_list_en_attente_mo, name='suggestion_voie_list_en_attente_mo'),
    path('ajouter_suggestion_voie/<int:voie_id>/', views.ajouter_suggestion_voie, name='ajouter_suggestion_voie'),


    path('suggestion/', views.suggestion_list, name='suggestion_list'),
    path('problemes/', views.problemes_list, name='problemes_list'),

    path('publicite/<int:id>/', views.edit_publicite, name='edit_publicite'),
    path('afficher_publicite/', views.afficher_publicite, name='afficher_publicite'),




]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)