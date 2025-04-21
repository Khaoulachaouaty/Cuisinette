# Accueil/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Like, Notification

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        recipe = instance.recipe
        if instance.user != recipe.author:
            Notification.objects.create(
                user=recipe.author,  # Utilisateur qui reçoit la notification
                sender=instance.user,  # Utilisateur qui effectue l'action (commentaire)
                message=f"{instance.user.username} a commenté votre recette '{recipe.title}'"
            )

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        recipe = instance.recipe
        if instance.user != recipe.author:
            Notification.objects.create(
                user=recipe.author,  # Utilisateur qui reçoit la notification
                sender=instance.user,  # Utilisateur qui effectue l'action (like)
                message=f"{instance.user.username} a aimé votre recette '{recipe.title}'"
            )


