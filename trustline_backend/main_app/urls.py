from django.urls import path
from .views import PasswordResetRequestView, PersonnaliseCreationDeCompte, LoginPersonne,MyTokenObtainPairView, MyTokenRefreshView, SetNewPasswordView,UtilisateurListCreate, UtilisateurDetail, EntrepriseListCreate, EntrepriseDetail, TravailleurListCreate, TravailleurDetail,ContenuListCreate, ContenuDetail,AnnonceListCreate, AnnonceDetail,OffreEmploiListCreate, OffreEmploiDetail, AnnuaireListCreate, AnnuaireDetail

urlpatterns = [
    path('utilisateurs/', UtilisateurListCreate.as_view(), name='utilisateur-list-create'),
    path('utilisateurs/<int:pk>/', UtilisateurDetail.as_view(), name='utilisateur-detail'),
    path('entreprises/', EntrepriseListCreate.as_view(), name='entreprise-list-create'),
    path('entreprises/<int:pk>/', EntrepriseDetail.as_view(), name='entreprise-detail'),
    path('travailleurs/', TravailleurListCreate.as_view(), name='travailleur-list-create'),
    path('travailleurs/<int:pk>/', TravailleurDetail.as_view(), name='travailleur-detail'),
    path('contenus/', ContenuListCreate.as_view(), name='contenu-list-create'),
    path('contenus/<int:pk>/', ContenuDetail.as_view(), name='contenu-detail'),
    path('annonces/', AnnonceListCreate.as_view(), name='annonce-list-create'),
    path('annonces/<int:pk>/', AnnonceDetail.as_view(), name='annonce-detail'),
    path('offres-emploi/', OffreEmploiListCreate.as_view(), name='offre-emploi-list-create'),
    path('offres-emploi/<int:pk>/', OffreEmploiDetail.as_view(), name='offre-emploi-detail'),
    path('annuaires/', AnnuaireListCreate.as_view(), name='annuaire-list-create'),
    path('annuaires/<int:pk>/', AnnuaireDetail.as_view(), name='annuaire-detail'),
    path('login/', LoginPersonne.as_view(), name='login'),
    path('register/', PersonnaliseCreationDeCompte.as_view(), name='register'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('reset-password/<uidb64>/<token>/', SetNewPasswordView.as_view(), name='reset-password'),
]
