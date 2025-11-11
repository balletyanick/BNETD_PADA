
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('p_bnetd25/', include('custom_admin.urls')),
    path('', include('myapp.urls')),
]

# Permet d'afficher les fichiers qui se trouve dans media dans le navigateur
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



