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
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializers import PasswordResetRequestSerializer, SetNewPasswordSerializer


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
    





class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = Utilisateur.objects.filter(email=email).first()

        if user is None:
            return Response({"error": "Utilisateur non trouvé"}, status=404)

        # Générer un token de réinitialisation de mot de passe
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Générer l'URL de réinitialisation du mot de passe
        reset_url = f'http://localhost:8000/api/reset-password/{uid}/{token}'

        # Rendre le template HTML pour l'e-mail
        message = render_to_string('main_app/email_password_reset.html', {
            'user': user,
            'reset_url': reset_url,
        })

        # Envoyer l'e-mail
        subject = 'Demande de réinitialisation de mot de passe'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]

        email_message = EmailMultiAlternatives(subject, '', email_from, recipient_list)
        email_message.attach_alternative(message, "text/html")
        email_message.send()

        return Response({"message": "E-mail de réinitialisation de mot de passe envoyé"}, status=200)

# Vue pour réinitialiser le mot de passe
class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Utilisateur.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Utilisateur.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({"message": "Le mot de passe a été réinitialisé avec succès."}, status=status.HTTP_200_OK)
        return Response({"error": "Lien invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)  