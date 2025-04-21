from django.contrib import admin

from Accueil.models import Category, Recipe, Comment, Rating, Favorite, Like, Notification

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Favorite)
admin.site.register(Like)
admin.site.register(Notification)