import re
from django.forms import ValidationError
from rest_framework import generics
from .models import (
    Utilisateur,
    Entreprise,
    Travailleur,
    Contenu,
    Annonce,
    OffreEmploi,
    Annuaire,
)
from .serializers import (
    LoginSerializer,
    UtilisateurSerializer,
    EntrepriseSerializer,
    TravailleurSerializer,
    ContenuSerializer,
    AnnonceSerializer,
    OffreEmploiSerializer,
    AnnuaireSerializer,
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import transaction
import json
from django.contrib.auth.password_validation import validate_password


# Vues pour le modèle Utilisateur
class UtilisateurListCreate(generics.ListCreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer


# permission_classes = [IsAuthenticated] #protéger l'accès à la liste des utilisateurs,


class UtilisateurDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer


# permission_classes = [IsAuthenticated] #protéger l'accès à la liste des utilisateurs,


# Vues pour le modèle Entreprise
class EntrepriseListCreate(generics.ListCreateAPIView):
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer


class EntrepriseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer


# Vues pour le modèle Travailleur
class TravailleurListCreate(generics.ListCreateAPIView):
    queryset = Travailleur.objects.all()
    serializer_class = TravailleurSerializer


class TravailleurDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Travailleur.objects.all()
    serializer_class = TravailleurSerializer


# Vues pour le modèle Contenu
class ContenuListCreate(generics.ListCreateAPIView):
    queryset = Contenu.objects.all()
    serializer_class = ContenuSerializer


class ContenuDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contenu.objects.all()
    serializer_class = ContenuSerializer


# Vues pour le modèle Annonce
class AnnonceListCreate(generics.ListCreateAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer


class AnnonceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer


# Vues pour le modèle OffreEmploi
class OffreEmploiListCreate(generics.ListCreateAPIView):
    queryset = OffreEmploi.objects.all()
    serializer_class = OffreEmploiSerializer


class OffreEmploiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OffreEmploi.objects.all()
    serializer_class = OffreEmploiSerializer


# Vues pour le modèle Annuaire
class AnnuaireListCreate(generics.ListCreateAPIView):
    queryset = Annuaire.objects.all()
    serializer_class = AnnuaireSerializer


class AnnuaireDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Annuaire.objects.all()
    serializer_class = AnnuaireSerializer


# Vues pour l'authentification JWT
class MyTokenObtainPairView(TokenObtainPairView):
    pass


class MyTokenRefreshView(TokenRefreshView):
    pass


#login utilisateur
class LoginPersonne(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_ou_telephone = serializer.validated_data["email_ou_telephone"]
        passCode = serializer.validated_data["passCode"]

        print(f"Email ou Téléphone: {email_ou_telephone}")
        print(f"PassCode: {passCode}")

        is_email = re.match(r"[^@]+@[^@]+\.[^@]+", email_ou_telephone) is not None

        if is_email:
            personne = Utilisateur.objects.filter(email=email_ou_telephone).first()
        else:
            personne = Utilisateur.objects.filter(téléphone=email_ou_telephone).first()

        if personne is None:
            print("Utilisateur non trouvé")
            raise AuthenticationFailed("E-mail, téléphone ou mot de passe incorrect")

        if not personne.check_password(passCode):
            print("Mot de passe incorrect")
            raise AuthenticationFailed("E-mail, téléphone ou mot de passe incorrect")

        if not personne.is_active:
            raise AuthenticationFailed("Le compte est désactivé")

        # Création du token
        refresh = RefreshToken.for_user(personne)

        return Response(
            {
                "jwt": str(refresh.access_token),
                "refresh": str(refresh),
                "user_type": personne.rôle,
            }
        )

#creation utilisateur
@method_decorator(csrf_exempt, name='dispatch')
class PersonnaliseCreationDeCompte(View):

    @csrf_exempt
    def post(self, request):
        if request.method == 'POST':
            try:
                # Vérifiez le Content-Type de la requête pour déterminer comment lire les données
                if request.content_type == 'application/json':
                    data = json.loads(request.body.decode('utf-8'))
                else:
                    data = request.POST

                nom = data.get('nom')
                prénom = data.get('prénom')
                email = data.get('email')
                téléphone = data.get('téléphone')
                adresse = data.get('adresse')
                password = data.get('password')
                repassword = data.get('repassword')
                rôle = data.get('rôle')
                date_inscription = data.get('date_inscription')

                if not nom or not email or not téléphone or not password:
                    return HttpResponseBadRequest("Les champs requis doivent être renseignés")

                if password != repassword:
                    return HttpResponseBadRequest("Les mots de passe ne correspondent pas")

                try:
                    validate_password(password)
                except ValidationError as e:
                    return HttpResponseBadRequest("Erreur de mot de passe : " + ', '.join(e.messages))

                with transaction.atomic():
                    # Créer un utilisateur générique
                    user = Utilisateur(
                        nom=nom,
                        prénom=prénom,
                        email=email,
                        téléphone=téléphone,
                        adresse=adresse,
                        rôle=rôle,
                        date_inscription=date_inscription,
                    )
                    user.set_password(password)
                    user.save()

                    return JsonResponse({"message": "Utilisateur créé avec succès"})

            except json.JSONDecodeError:
                return JsonResponse({"error": "Données JSON mal formatées"}, status=400)

        return JsonResponse({"error": "Requête invalide"},status=400)