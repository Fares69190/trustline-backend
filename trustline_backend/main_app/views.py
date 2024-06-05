import re
from django.views import View
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


class LoginPersonne(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_ou_telephone = serializer.validated_data["email_ou_telephone"]
        password = serializer.validated_data["password"]

        is_email = re.match(r"[^@]+@[^@]+\.[^@]+", email_ou_telephone) is not None

        if is_email:
            personne = Utilisateur.objects.filter(email=email_ou_telephone).first()
        else:
            personne = Utilisateur.objects.filter(telephone=email_ou_telephone).first()

        if personne is None or not personne.check_password(password):
            raise AuthenticationFailed("E-mail, téléphone ou mot de passe incorrect")

        if not personne.is_active:
            raise AuthenticationFailed("Le compte est désactivé")

        # Création du token
        refresh = RefreshToken.for_user(personne)

        # Inclure le type d'utilisateur dans le payload du token si nécessaire
        # Exemple: refresh['user_type'] = personne.user_type

        return Response(
            {
                "jwt": str(refresh.access_token),
                "refresh": str(refresh),
                "user_type": personne.type_utilisateur,  # Assurez-vous que votre modèle a un champ user_type
            }
        )
