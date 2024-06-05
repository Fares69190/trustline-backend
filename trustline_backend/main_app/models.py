from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager,PermissionsMixin,AbstractBaseUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse e-mail doit être renseignée')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Utilisateur(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    prénom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    rôle = models.CharField(max_length=50)
    date_inscription = models.DateTimeField(auto_now_add=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    téléphone = models.CharField(max_length=20, null=True, blank=True)
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'rôle']

    def _str_(self):
        return self.email
    
    def generate_auth_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token.key


class Entreprise(Utilisateur):
    site_web = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    logo = models.CharField(max_length=255, null=True, blank=True)
    WhatsApp = models.CharField(max_length=20, null=True, blank=True)
    catégorie = models.CharField(max_length=255, null=True, blank=True)
    social_media = models.JSONField(null=True, blank=True)
    video_presentation = models.CharField(max_length=255, null=True, blank=True)
    images = models.JSONField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

class Travailleur(Utilisateur):
    compétences = models.JSONField(null=True, blank=True)
    expériences = models.JSONField(null=True, blank=True)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    abonnement = models.JSONField(null=True, blank=True)

class Contenu(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField(null=True, blank=True)

class Annonce(Contenu):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    image = models.CharField(max_length=255, null=True, blank=True)

class OffreEmploi(Contenu):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    lieu = models.CharField(max_length=255)
    type_contrat = models.CharField(max_length=50)
    salaire = models.FloatField()

class Annuaire(models.Model):
    id = models.AutoField(primary_key=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)