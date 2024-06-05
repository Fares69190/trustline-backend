from rest_framework import serializers
from .models import Utilisateur, Entreprise, Travailleur, Contenu, Annonce, OffreEmploi, Annuaire


class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'

class EntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entreprise
        fields = '__all__'

class TravailleurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travailleur
        fields = '__all__'

class ContenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contenu
        fields = '__all__'

class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'

class OffreEmploiSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffreEmploi
        fields = '__all__'

class AnnuaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annuaire
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email_ou_telephone = serializers.CharField(required=True)
    passCode = serializers.CharField(required=True)