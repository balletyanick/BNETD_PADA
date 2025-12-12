
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

handler404 = 'myapp.views.custom_404'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('p_bnetd25/', include('custom_admin.urls')),
    path('street/', include('street_views.urls')),
    path('', include('myapp.urls')),
]
   # Erreur 404


# Permet d'afficher les fichiers qui se trouve dans media dans le navigateur
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


