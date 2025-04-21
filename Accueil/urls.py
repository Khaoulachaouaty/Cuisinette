from django.urls import path
from .views import toggle_like, toggle_favorite, add_comment, edit_comment, delete_comment, subcategory_list, recipe_list_by_subcategory, ajouter_recette, search_recipes, rate_recipe, get_avg_rating, get_user_rating, mark_notifications_read

urlpatterns = [
    path("toggle-like/<int:recipe_id>/", toggle_like, name="toggle_like"),
    path("toggle-favorite/<int:recipe_id>/", toggle_favorite, name="toggle_favorite"),
    path("add-comment/<int:recipe_id>/", add_comment, name="add_comment"),
    path('edit-comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('categories/<int:category_id>/subcategories/', subcategory_list, name='subcategory_list'),  # Liste des sous-catégories
    path('subcategory/<int:subcategory_id>/recipes/', recipe_list_by_subcategory, name='recipe_list_by_subcategory'),
    path('ajouter/', ajouter_recette, name='ajouter_recette'),
    path('recherche/', search_recipes, name='search'),
    path('rate-recipe/<int:recipe_id>/', rate_recipe, name='rate_recipe'),
    path('get-user-rating/<int:recipe_id>/', get_user_rating, name='get_user_rating'),
    path('get-avg-rating/<int:recipe_id>/', get_avg_rating, name='get_avg_rating'),
    path('notifications/read/', mark_notifications_read, name='mark_notifications_read'),
    #path('recette/modifier/<int:id>/', modifier_recette, name='modifier_recette'),
    #path('recette/supprimer/<int:id>/', supprimer_recette, name='supprimer_recette')
]
