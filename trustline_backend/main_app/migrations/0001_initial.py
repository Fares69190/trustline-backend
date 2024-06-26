# Generated by Django 4.2.11 on 2024-06-05 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contenu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date_publication', models.DateTimeField(auto_now_add=True)),
                ('date_expiration', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255)),
                ('prénom', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('rôle', models.CharField(max_length=50)),
                ('date_inscription', models.DateTimeField(auto_now_add=True)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('téléphone', models.CharField(blank=True, max_length=20, null=True)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last\xa0login')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Entreprise',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main_app.utilisateur')),
                ('site_web', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('logo', models.CharField(blank=True, max_length=255, null=True)),
                ('WhatsApp', models.CharField(blank=True, max_length=20, null=True)),
                ('catégorie', models.CharField(blank=True, max_length=255, null=True)),
                ('social_media', models.JSONField(blank=True, null=True)),
                ('video_presentation', models.CharField(blank=True, max_length=255, null=True)),
                ('images', models.JSONField(blank=True, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('main_app.utilisateur',),
        ),
        migrations.CreateModel(
            name='Travailleur',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main_app.utilisateur')),
                ('compétences', models.JSONField(blank=True, null=True)),
                ('expériences', models.JSONField(blank=True, null=True)),
                ('cv', models.FileField(blank=True, null=True, upload_to='cvs/')),
                ('abonnement', models.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('main_app.utilisateur',),
        ),
        migrations.CreateModel(
            name='OffreEmploi',
            fields=[
                ('contenu_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main_app.contenu')),
                ('lieu', models.CharField(max_length=255)),
                ('type_contrat', models.CharField(max_length=50)),
                ('salaire', models.FloatField()),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.entreprise')),
            ],
            bases=('main_app.contenu',),
        ),
        migrations.CreateModel(
            name='Annuaire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.entreprise')),
            ],
        ),
        migrations.CreateModel(
            name='Annonce',
            fields=[
                ('contenu_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main_app.contenu')),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.entreprise')),
            ],
            bases=('main_app.contenu',),
        ),
    ]
