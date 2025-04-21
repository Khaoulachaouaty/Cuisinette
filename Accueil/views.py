import json
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from .models import Notification, Recipe, Favorite, Category, Like, Comment, Rating
from django.utils.timezone import now
from .forms import RecipeForm
from django.template.loader import render_to_string


from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.db.models import Q

from .models import Recipe

def home(request):
    return render(request, "home.html")

def accueil(request):
    recipes = Recipe.objects.annotate(avg_rating=Avg("ratings__rating")).order_by('-created_at')
    if request.user.is_authenticated:
        for recipe in recipes:
            recipe.is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    
    return render(request, "Recipe/accueil.html", {"recipes": recipes})

def favorites(request):
    favorite_recipes = Recipe.objects.filter(favorites__user=request.user).annotate(avg_rating=Avg("ratings__rating")).order_by('-created_at')
    return render(request, "Recipe/favorite.html", {"favorite_recipes": favorite_recipes})

def categorie(request):
    categories = Category.objects.filter(parent__isnull=True) 
    return render(request, "Recipe/category.html", {"categories": categories})

def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)  # Récupérer la catégorie par ID
    subcategories = category.subcategories.all()  # Récupérer les sous-catégories de la catégorie
    return render(request, "Recipe/subcategory_list.html", {"category": category, "subcategories": subcategories})

def recipe_list_by_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Category, id=subcategory_id)
    recipes = Recipe.objects.filter(category=subcategory).order_by('-created_at')
    
    # Ajouter l'information "is_favorite" pour chaque recette en fonction de l'utilisateur connecté
    for recipe in recipes:
        recipe.is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    
    return render(request, "Recipe/recipe_list_by_subcategory.html", {
        "subcategory": subcategory,
        "recipes": recipes
    })

def accueilSansCnx(request):
    recipes = Recipe.objects.annotate(avg_rating=Avg("ratings__rating")).order_by('-created_at')
    return render(request, "SansConnexion/accueil.html", {"recipes": recipes})

def toggle_favorite(request, recipe_id):
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user

        favorite, created = Favorite.objects.get_or_create(user=user, recipe=recipe)

        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True

        return JsonResponse({
            "is_favorite": is_favorite
        })

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

def toggle_like(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    like, created = Like.objects.get_or_create(user=request.user, recipe=recipe)

    if not created:
        like.delete()  # Supprime le like si déjà liké
        liked = False
    else:
        liked = True

    likes_count = recipe.likes.count()
    return JsonResponse({'liked': liked, 'likes_count': likes_count})

def add_comment(request, recipe_id):
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, id=recipe_id)
        comment_content = request.POST.get("comment")

        if comment_content.strip():  # Vérifier que le commentaire n'est pas vide
            comment = Comment.objects.create(user=request.user, recipe=recipe, content=comment_content)
            
            # Récupérer les commentaires mis à jour
            comments = recipe.comments.all()

            comments_data = [
                {
                    "id": comment.id,
                    "user": comment.user.username,
                    "content": comment.content,
                    "created_at": comment.created_at.strftime("%d/%m/%Y %H:%M"),
                }
                for comment in comments
            ]
            
            return JsonResponse({
                "success": True,
                "comments": comments_data,
                "currentUser": request.user.username  # Ajout de l'utilisateur connecté
            })

    return JsonResponse({"success": False}, status=400)

def edit_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        new_content = request.POST.get('comment')

        if new_content:
            comment.content = new_content
            comment.save()
            return JsonResponse({'success': True, 'comment': comment.content})

    return JsonResponse({'success': False})

def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        comment.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

# Mes recettes
def mes_recettes(request):
    user = request.user
    recettes = Recipe.objects.filter(author=user).order_by('-created_at')

    # Exclusion de catégories
    categories = Category.objects.exclude(name__in=['Entrée', 'Dessert', 'Plats'])

    if request.method == 'POST':
        action = request.POST.get('action')
        recette_id = request.POST.get('recette_id')
        recette = get_object_or_404(Recipe, id=recette_id, author=user)

        if action == 'modifier':
            form = RecipeForm(request.POST, request.FILES, instance=recette)
            if form.is_valid():
                form.save()
        elif action == 'supprimer':
            recette.delete()
            return redirect('mes_recettes')

    # Statistiques globales
    total_posts = recettes.count()
    total_likes = sum([r.likes.count() for r in recettes])
    total_favorites = sum([r.favorites.count() for r in recettes])

    # Annoter avec moyenne des notes
    recettes = recettes.annotate(avg_rating=Avg('ratings__rating'))

    # Marquer les favoris
    for recette in recettes:
        recette.is_favorite = Favorite.objects.filter(user=request.user, recipe=recette).exists()


    forms = [(recette, RecipeForm(instance=recette, initial={'category': recette.category})) for recette in recettes]

    return render(request, 'Recipe/mes_recettes.html', {
        'recettes': recettes,
        'forms': forms,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_favorites': total_favorites,
        'user': user,
        'categories': categories,
    })

def ajouter_recette(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recette = form.save(commit=False)
            recette.author = request.user  # Associer l'utilisateur à la recette
            recette.save()
            return redirect('mes_recettes')  # Redirige vers mes-recettes après l'ajout
    else:
        form = RecipeForm()

    # Récupérer toutes les catégories sauf 'Entrée', 'Dessert', 'Plats'
    categories = Category.objects.exclude(name__in=['Entrée', 'Dessert', 'Plats'])

    return render(request, 'Recipe/mes_recettes.html', {'form': form, 'categories': categories})

def search_recipes(request):
    query = request.GET.get('q')
    recipes = []
    if query:
        recipes = Recipe.objects.filter(title__icontains=query)
        if request.user.is_authenticated:
            for recipe in recipes:
                recipe.is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    return render(request, 'Recipe/search_results.html', {'recipes': recipes, 'query': query})

def statistiques(request):
    user = request.user  # Récupère l'utilisateur actuellement connecté

    # 🔸 1. Nombre de recettes par catégorie (top 5)
    recettes_par_categorie = (
        Recipe.objects.filter(author=user)  # Filtrer les recettes créées par l'utilisateur
        .values('category__name')  # Regrouper par nom de catégorie
        .annotate(count=Count('id'))  # Compter le nombre de recettes dans chaque catégorie
        .order_by('-count')  # Trier par nombre décroissant
    )

    # 🔸 2. Recettes créées par mois
    recettes_par_mois = (
        Recipe.objects.filter(author=user)  # Recettes de l'utilisateur
        .annotate(month=TruncMonth('created_at'))  # Extraire le mois de création
        .values('month')  # Grouper par mois
        .annotate(count=Count('id'))  # Compter le nombre de recettes par mois
        .order_by('month')  # Trier par mois croissant
    )

    # 🔸 3. Évolution des likes reçus par mois
    likes_par_mois = (
        Like.objects.filter(recipe__author=user)  # Likes sur les recettes de l'utilisateur
        .annotate(month=TruncMonth('created_at'))  # Extraire le mois
        .values('month')  # Grouper par mois
        .annotate(count=Count('id'))  # Compter les likes par mois
        .order_by('month')  # Trier par ordre chronologique
    )

    # 🔸 4. Recettes populaires (top 5 avec le plus de likes)
    recettes_populaires = (
        Recipe.objects.filter(author=user)  # Recettes de l'utilisateur
        .annotate(
            likes_count=Count('likes'),  # Nombre de likes
            fav_count=Count('favorites')  # Nombre de favoris (optionnel ici)
        )
        .filter(Q(likes_count__gt=0) | Q(fav_count__gt=0))  # ✅ Au moins un like OU un favori
        .order_by('-likes_count')[:5]  # Trier par likes décroissants et prendre les 5 premières
    )

    # 🔸 5. Top 5 des favoris de l'utilisateur selon la note moyenne
    favoris_notes = (
        Favorite.objects.filter(user=user)  # Favoris de l'utilisateur
        .annotate(avg_rating=Avg('recipe__ratings__rating'))  # Moyenne des notes pour chaque recette favorite
        .order_by('-avg_rating')[:5]  # Trier par note décroissante
    )

    # 🔸 6. Meilleures catégories selon la note moyenne des recettes
    top_categories_par_note = (
        Recipe.objects.filter(author=user)  # Recettes de l'utilisateur
        .values('category__name')  # Grouper par nom de catégorie
        .annotate(avg_rating=Avg('ratings__rating'))  # Moyenne des notes
        .order_by('-avg_rating')[:5]  # Prendre les 5 meilleures catégories
    )

    # 🔸 7. Recettes qui n'ont ni likes ni notes
    non_notees_ou_non_likées = (
        Recipe.objects.filter(author=user)  # Recettes de l'utilisateur
        .annotate(
            nb_likes=Count('likes'),  # Compter les likes
            nb_ratings=Count('ratings')  # Compter les notes
        )
        .filter(nb_likes=0, nb_ratings=0)  # Filtrer celles sans likes ET sans notes
    )

    # 🔸 8. Statistiques globales (pour affichage en haut de page)
    total_recettes = Recipe.objects.filter(author=user).count()  # Nombre total de recettes
    total_likes = Like.objects.filter(recipe__author=user).count()  # Total de likes reçus
    total_favoris = Favorite.objects.filter(recipe__author=user).count()  # Total de favoris reçus
    avg_rating = Recipe.objects.filter(author=user).aggregate(
        avg_rating=Avg('ratings__rating')  # Calcul de la note moyenne générale
    )['avg_rating'] or 0  # Si aucune note, on affiche 0

    # 🔸 9. Préparer toutes les données à envoyer au template HTML
    context = {
        "recettes_par_categorie": recettes_par_categorie,
        "recettes_par_mois": recettes_par_mois,
        "likes_par_mois": likes_par_mois,
        "recettes_populaires": recettes_populaires,
        "favoris_notes": favoris_notes,
        "top_categories_par_note": top_categories_par_note,
        "non_notees_ou_non_likées": non_notees_ou_non_likées,
        "total_recettes": total_recettes,
        "total_likes": total_likes,
        "total_favoris": total_favoris,
        "avg_rating": avg_rating,
    }

    # 🔸 10. Afficher la page 'statistiques.html' avec toutes les données
    return render(request, 'Recipe/statistiques.html', context)

def rate_recipe(request, recipe_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Utilisateur non connecté'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rating_value = int(data.get('rating'))

            if rating_value < 1 or rating_value > 5:
                return JsonResponse({'error': 'Note invalide'}, status=400)

            recipe = Recipe.objects.get(id=recipe_id)

            # Soit on met à jour une note existante, soit on en crée une
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                recipe=recipe,
                defaults={'rating': rating_value}
            )

            return JsonResponse({'success': True, 'created': created})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def get_user_rating(request, recipe_id):
    try:
        rating = Rating.objects.get(user=request.user, recipe_id=recipe_id)
        return JsonResponse({'rating': rating.rating})
    except Rating.DoesNotExist:
        return JsonResponse({'rating': None})
    
def get_avg_rating(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        avg = recipe.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
        return JsonResponse({'avg_rating': round(avg, 1)})
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recette introuvable'}, status=404)
    
def some_view(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:10]
    context = {
        "notifications": notifications,
        "unread_count": notifications.count(),
    }
    return render(request, "base.html", context)

def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({"status": "ok"})



