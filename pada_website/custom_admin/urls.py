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

    path('dashboard/', views.dashboard, name='dashboard'),
    path("users/", views.users_list, name="users_list"),
    path('voies/', views.voies_list, name='voies_list'),
    path('suggestion/', views.suggestion_list, name='suggestion_list'),
    path('problemes/', views.problemes_list, name='problemes_list'),

    path('publicite/<int:id>/', views.edit_publicite, name='edit_publicite'),
 
    path('afficher_publicite/', views.afficher_publicite, name='afficher_publicite'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)