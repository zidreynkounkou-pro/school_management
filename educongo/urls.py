# educongo/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),   # 01 Connexion
    path('', include('core.urls')),       # 02 Dashboard
    path('', include('scolarite.urls')), # 03 Élèves -> AJOUTE CETTE LIGNE
]