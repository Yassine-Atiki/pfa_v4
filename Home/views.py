from urllib import request
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import render
from django.views import View
from users.models import ProprietaireVE,Fournisseur # Import ProprietaireVE from models

# Create your views here.
def Home(request,username):
    if ProprietaireVE.objects.filter(username=username).exists() :
        user = ProprietaireVE.objects.get(username=username) 
    if Fournisseur.objects.filter(username=username).exists() :
        user = Fournisseur.objects.get(username=username)

    if user and (Fournisseur.objects.filter(username=username).exists() or ProprietaireVE.objects.filter(username=username).exists()):
        return Home_user_page.as_view()(request, user)
    #else:
        #return Home_admin_page.as_view()(request)

class Home_public_page(View):
    template_name = 'Home.html'
    def get(self, request):
        return render(request,self.template_name)
    
class Home_user_page(View):
    template_name = 'Home.html'
    def get(self, request, user):
        return render(request,self.template_name,context={'user': user})

class Home_admin_page(View):
    template_name = 'Home_Admin.html'
    def get(self, request, user):
        return render(request,self.template_name,context={'user': user})
    
def logout_view(request):
    logout(request)
    return render(request, 'Home.html')