from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login as auth_login
from users.models import ProprietaireVE, Fournisseur, Administrateur


def inscription(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        
        if user_type == 'proprietaire':
            view = ProprietaireVE_View_creat.as_view()
            return view(request)
        elif user_type == 'fournisseur':
            view = Fournisseur_View_creat.as_view()
            return view(request)

    return render(request, 'inscription.html')

class ProprietaireVE_View_creat(CreateView):
    model = ProprietaireVE
    fields = ['CIN', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'password']
    template_name = 'inscription.html'
    success_url = '/users/login/'  # Redirect to the login page after successful registration

    def post(self, request, *args, **kwargs):
        # Récupération des données du formulaire
        CIN = request.POST.get('CIN')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        # Vérifier si un champ est vide 
        if not all([CIN, first_name, last_name, username, email, phone_number, password]):
            return render(request, self.template_name, {'error': "Veuillez remplir tous les champs."})
        
        # Vérifier si le CIN existe déjà
        if ProprietaireVE.objects.filter(CIN=CIN).exists():
            return render(request, self.template_name, {'error': "Le CIN existe déjà."})

        # Vérifier si l'email existe déjà
        if ProprietaireVE.objects.filter(email=email).exists() or Fournisseur.objects.filter(email=email).exists():
            return render(request, self.template_name, {'error': "L'email existe déjà."})

        # Vérifier si le numéro de téléphone existe déjà
        if ProprietaireVE.objects.filter(phone_number=phone_number).exists() or Fournisseur.objects.filter(phone_number=phone_number).exists():
            return render(request, self.template_name, {'error': "Le numéro de téléphone existe déjà."})

        # Vérifier si le nom d'utilisateur existe déjà
        if ProprietaireVE.objects.filter(username=username).exists() or Fournisseur.objects.filter(username=username).exists():
            return render(request, self.template_name, {'error': "Le nom d'utilisateur existe déjà."})
        
        # Créer l'utilisateur
        ProprietaireVE.objects.create(
            CIN=CIN,
            first_name=first_name, 
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            password=make_password(password)
        )
        return HttpResponseRedirect(self.success_url)

class Fournisseur_View_creat(CreateView):
    model = Fournisseur
    fields = ['CIN', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'password']
    template_name = 'inscription.html'
    success_url = '/users/login/'  # Redirect to the login page after successful registration

    def post(self, request, *args, **kwargs):
        # Récupération des données du formulaire
        CIN = request.POST.get('CIN')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password') 

        # Vérifier si un champ est vide
        if not all([CIN, first_name, last_name, username, email, phone_number, password]):
            return render(request, self.template_name, {'error': "Veuillez remplir tous les champs."})
                
        # Vérifier si le CIN existe déjà
        if Fournisseur.objects.filter(CIN=CIN).exists():
            return render(request, self.template_name, {'error': "Le CIN existe déjà."})

        # Vérifier si l'email existe déjà
        if Fournisseur.objects.filter(email=email).exists() or ProprietaireVE.objects.filter(email=email).exists():
            return render(request, self.template_name, {'error': "L'email existe déjà."})

        # Vérifier si le numéro de téléphone existe déjà
        if Fournisseur.objects.filter(phone_number=phone_number).exists() or ProprietaireVE.objects.filter(phone_number=phone_number).exists():
            return render(request, self.template_name, {'error': "Le numéro de téléphone existe déjà."})

        # Vérifier si le nom d'utilisateur existe déjà
        if Fournisseur.objects.filter(username=username).exists() or ProprietaireVE.objects.filter(username=username).exists():
            return render(request, self.template_name, {'error': "Le nom d'utilisateur existe déjà."})
        
        # Créer l'utilisateur
        Fournisseur.objects.create(
            CIN=CIN,
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            password=make_password(password)
        )
        return HttpResponseRedirect(self.success_url)
    
# Login part for the users
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'proprietaire':
            view = ProprietaireVE_View_login.as_view()
            return view(request)
        elif user_type == 'fournisseur':
            view = Fournisseur_View_login.as_view()
            return view(request)
        elif user_type == 'Administrateur':
            view = Administrateur_View_login.as_view()
            return view(request)
    return render(request, 'login.html')

class ProprietaireVE_View_login(LoginView):
    model = ProprietaireVE
    fields = ['email', 'password']
    template_name = 'login.html'
    
    def post(self, request, *args, **kwargs):
        # Récupération des données du formulaire
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Vérifier si un champ est vide
        if not all([email, password]):
            return render(request, self.template_name, {'error': "Veuillez remplir tous les champs."})
        if ProprietaireVE.objects.filter(email=email).exists():
            user = ProprietaireVE.objects.get(email=email)
            if user.check_password(password):
                auth_login(request, user)
                return HttpResponseRedirect(reverse('Home:Home', args=[user.username]))
            else:
                return render(request, self.template_name, {'error': "Mot de passe invalide."})
        return render(request, self.template_name, {'error': "Utilisateur introuvable."})

class Fournisseur_View_login(LoginView):
    model = Fournisseur
    fields = ['email', 'password']
    template_name = 'login.html'
  
    def post(self, request, *args, **kwargs):
        # Récupération des données du formulaire
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Vérifier si un champ est vide
        if not all([email, password]):
            return render(request, self.template_name, {'error': "Veuillez remplir tous les champs."})
        if Fournisseur.objects.filter(email=email).exists():
            user = Fournisseur.objects.get(email=email)
            if user.check_password(password):
                auth_login(request, user)
                return HttpResponseRedirect(reverse('Home:Home', args=[user.username]))
            else:
                return render(request, self.template_name, {'error': "Mot de passe invalide."})
        return render(request, self.template_name, {'error': "Utilisateur introuvable."})
    
# Login part for the admin
class Administrateur_View_login(LoginView):
    model = Administrateur
    fields = ['email', 'password']
    template_name = 'login.html'
    
    def post(self, request, *args, **kwargs):
        # Récupération des données du formulaire
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Vérifier si un champ est vide
        if not all([email, password]):
            return render(request, self.template_name, {'error': "Veuillez remplir tous les champs."})
        if Administrateur.objects.filter(email=email).exists():
            user = Administrateur.objects.get(email=email)
            if user.check_password(password):
                auth_login(request, user)
                return HttpResponseRedirect(reverse('Home:Home', args=[user.username]))
            else:
                return render(request, self.template_name, {'error': "Mot de passe invalide."})
        return render(request, self.template_name, {'error': "Utilisateur introuvable."})

def profile(request, username):
    # Récupérer l'utilisateur en fonction du type
    if ProprietaireVE.objects.filter(username=username).exists():
        user = ProprietaireVE.objects.get(username=username)
        user_type = "Propriétaire De Véhicule Électrique"
    elif Fournisseur.objects.filter(username=username).exists():
        user = Fournisseur.objects.get(username=username)
        user_type = "Fournisseur De Stations De Recharge"
    elif Administrateur.objects.filter(username=username).exists():
        user = Administrateur.objects.get(username=username)
        user_type = "Administrateur principal"
    else:
        return render(request, 'profile.html', {'error': "Utilisateur introuvable."})

    error = None
    success = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_info':
            # Mettre à jour les informations personnelles
            CIN = request.POST.get('CIN', user.CIN)  # Utiliser la valeur actuelle si non fournie
            first_name = request.POST.get('first_name', user.first_name)
            last_name = request.POST.get('last_name', user.last_name)
            new_username = request.POST.get('username', user.username)
            email = request.POST.get('email', user.email)
            phone_number = request.POST.get('phone_number', user.phone_number)

            # Vérifier les conflits avec d'autres utilisateurs
            if email != user.email and (ProprietaireVE.objects.filter(email=email).exists() or Fournisseur.objects.filter(email=email).exists()):
                error = "L'email existe déjà."
            elif phone_number != user.phone_number and (ProprietaireVE.objects.filter(phone_number=phone_number).exists() or Fournisseur.objects.filter(phone_number=phone_number).exists()):
                error = "Le numéro de téléphone existe déjà."
            elif new_username != user.username and (ProprietaireVE.objects.filter(username=new_username).exists() or Fournisseur.objects.filter(username=new_username).exists()):
                error = "Le nom d'utilisateur existe déjà."
            else:
                # Mettre à jour les informations personnelles
                user.CIN = CIN
                user.first_name = first_name
                user.last_name = last_name
                user.username = new_username
                user.email = email
                user.phone_number = phone_number
                user.save()
                success = "Informations mises à jour avec succès."

        elif action == 'update_password':
            # Mettre à jour le mot de passe
            last_password = request.POST.get('last_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not all([last_password, new_password, confirm_password]):
                error = "Veuillez remplir tous les champs."
            elif not user.check_password(last_password):
                error = "Le mot de passe actuel est incorrect."
            elif new_password != confirm_password:
                error = "Le nouveau mot de passe et la confirmation ne correspondent pas."
            else:
                user.password = make_password(new_password)
                user.save()
                success = "Mot de passe mis à jour avec succès."

    return render(request, 'profile.html', {'user': user, 'user_type': user_type, 'error': error, 'success': success})