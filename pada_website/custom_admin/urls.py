from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    #Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),


    #User
    path("users/", views.users_list, name="users_list"),
    path('utilisateurs/supprimer/<int:user_id>/', views.delete_user, name='delete_user'),
    path('utilisateurs/editer/<int:user_id>/', views.edit_user, name='edit_user'),
    path('utilisateurs_ajouter/', views.create_user, name='create_user'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),


    #Voie
    path('voies/', views.voies_list, name='voies_list'),
    path('edit_voies/<int:voie_id>/', views.edit_voies, name='edit_voies'),
    path('dashboard_voies/<int:voie_id>/', views.dashboard_voies, name='dashboard_voies'),


    #CCA Panneautage
    path('valider_cca/<int:voie_id>/', views.valider_cca, name='valider_cca'),
    path('rejeter_cca/<int:voie_id>/', views.rejeter_cca, name='rejeter_cca'),
    path('ajouter_suggestion_cca/<int:voie_id>/', views.ajouter_suggestion_cca, name='ajouter_suggestion_cca'),


    #MO Panneautage
    path('valider_mo/<int:voie_id>/', views.valider_mo, name='valider_mo'),
    path('rejeter_mo/<int:voie_id>/', views.rejeter_mo, name='rejeter_mo'),
    path('ajouter_suggestion_mo/<int:voie_id>/', views.ajouter_suggestion_mo, name='ajouter_suggestion_mo'),


    #MO Sugggestion Description Panneautage
    path('suggestion_voie_list/', views.suggestion_voie_list, name='suggestion_voie_list'),
    path('suggestion_voie_list_en_attente_cca/', views.suggestion_voie_list_en_attente_cca, name='suggestion_voie_list_en_attente_cca'),
    path('suggestion_voie_list_en_attente_mo/', views.suggestion_voie_list_en_attente_mo, name='suggestion_voie_list_en_attente_mo'),
    path('ajouter_suggestion_voie/<int:voie_id>/', views.ajouter_suggestion_voie, name='ajouter_suggestion_voie'),


    path('suggestion/', views.suggestion_list, name='suggestion_list'),
    path('problemes/', views.problemes_list, name='problemes_list'),


    #MO Publicite
    path('publicite/<int:id>/', views.edit_publicite, name='edit_publicite'),
    path('afficher_publicite/', views.afficher_publicite, name='afficher_publicite'),


    #Toponyme
    path('toponymie/', views.toponyme_list, name='toponymie_list'),
    path('toponyme_list_sans_desc/', views.toponyme_list_sans_desc, name='topo_list_sans_desc'),
    path('topo_attente_topo/', views.topo_attente_topo, name='topo_attente_topo'),
    path('topo_attente_cs/', views.topo_attente_cs, name='topo_attente_cs'),
    path('topo_attente_coord/', views.topo_attente_coord, name='topo_attente_coord'),
    path('topo_attente_mo/', views.topo_attente_mo, name='topo_attente_mo'),
    path('dashboard_topo/<int:topo_id>/', views.dashboard_topo, name='dashboard_topo'),
    path('toponymie/ajouter_nouvelle_description/<int:topo_id>/',views.ajouter_nouvelle_description,name='ajouter_nouvelle_description'),
    path('toponymie/edit_toponyme/<int:topo_id>/',views.edit_toponyme,name='edit_toponyme'),

    # CS Toponyme
    path("valider_cs/<int:topo_id>/", views.valider_cs, name="valider_cs"),
    path("rejeter_cs/<int:topo_id>/", views.rejeter_cs, name="rejeter_cs"),
    path('ajouter_suggestion_cs_topo/<int:voie_id>/', views.ajouter_suggestion_cs_topo, name='ajouter_suggestion_cs_topo'),


    #Coord Toponyme
    path("valider_coord/<int:topo_id>/", views.valider_coord, name="valider_coord"),
    path("rejeter_coord/<int:topo_id>/", views.rejeter_coord, name="rejeter_coord"),
    path('ajouter_suggestion_cca_topo/<int:voie_id>/', views.ajouter_suggestion_cca_topo, name='ajouter_suggestion_cca_topo'),


    # MO Toponyme
    path('validation_mo_topo/<int:topo_id>/',views.validation_mo_topo,name='validation_mo_topo'),
    path('reject_mo_topo/<int:topo_id>/',views.reject_mo_topo,name='reject_mo_topo'),
    path('ajouter_suggestion_mo_topo/<int:voie_id>/', views.ajouter_suggestion_mo_topo, name='ajouter_suggestion_mo_topo'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)