"""
URL configuration for Recette project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Accounts.views import signup, signin, logout_user, edit_profile, profile
from Accueil.views import home, toggle_favorite
from Accueil.views import accueil,favorites, categorie, accueilSansCnx, mes_recettes, statistiques
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name='home'),
    path('accueil/',accueil, name='accueil'),
    path('toggle-favorite/<int:recipe_id>/', toggle_favorite, name='toggle_favorite'),
    path('favorite/',favorites, name='favorite'),
    path('catoregories/',categorie, name='categorie'),
    path('signup/', signup, name='signup'),
    path('login/', signin, name='login'),
    path('logout/', logout_user, name='logout'),
    path('explorer/',accueilSansCnx, name='accueilSansCnx'),
    path('recipes/', include('Accueil.urls')),
    path('', include('Accueil.urls')),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('profile/', profile, name='profile'),
    path('mes-recettes/', mes_recettes, name='mes_recettes'),
    path('statistiques/', statistiques, name='statistiques'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
