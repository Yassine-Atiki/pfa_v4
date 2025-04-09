from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator,MaxLengthValidator,MinLengthValidator

class Users (AbstractBaseUser):
    
    CIN=models.CharField(max_length=8,unique=True,validators=[MinLengthValidator(8),MaxLengthValidator(8)])
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(10), MaxLengthValidator(10)])
    password=models.CharField(max_length=50)
    def __str__(self):
        return super().__str__() + ' ' + self.first_name + ' ' + self.last_name+ ' ' + self.username+ ' ' + self.email+ ' ' + self.phone_number+ ' ' + self.password

class ProprietaireVE(Users):
    pass

class Fournisseur(Users):
    pass

class Administrateur(Users):
    pass

# Create your models here.
