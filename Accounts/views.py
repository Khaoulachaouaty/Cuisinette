from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model,login,logout,authenticate

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib import messages

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('accueil')
    return render(request, 'Accounts/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('accueil')
    return render(request, 'Accounts/login.html')

def logout_user(request):
    logout(request) 
    return redirect('home')

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        print("➡️ Méthode POST reçue")
        
        if 'change_password' in request.POST:
            print("🔐 Tentative de changement de mot de passe")
            password_form = CustomPasswordChangeForm(user, request.POST)
            user_form = CustomUserChangeForm(instance=user)  # non utilisé ici

            if password_form.is_valid():
                print("✅ Formulaire mot de passe valide")
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, "Mot de passe changé avec succès.")
                return redirect('edit_profile')
            else:
                print("❌ Formulaire mot de passe invalide :")
                print(password_form.errors.as_text())
                messages.error(request, "Erreur lors du changement de mot de passe.")

        elif 'update_profile' in request.POST:
            print("📝 Tentative de mise à jour du profil")
            user_form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
            password_form = CustomPasswordChangeForm(user)

            if user_form.is_valid():
                print("✅ Formulaire utilisateur valide")
                user_form.save()
                messages.success(request, "Profil mis à jour.")
                return redirect('edit_profile')
            else:
                print("❌ Formulaire utilisateur invalide")
                print(user_form.errors.as_text())
                messages.error(request, "Erreur lors de la mise à jour du profil.")
    else:
        print("➡️ Méthode GET")
        user_form = CustomUserChangeForm(instance=user)
        password_form = CustomPasswordChangeForm(user)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })

@login_required
def profile(request):
    return render(request, 'edit_profile.html', {'user': request.user})
