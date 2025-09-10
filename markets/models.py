from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from dateutil.relativedelta import relativedelta
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

class MaitreOuvrage(models.Model):
    """Maître d'ouvrage - Client/Owner"""
    nom = models.CharField(max_length=200, verbose_name="Nom de l'organisation")
    adresse = models.TextField(blank=True, verbose_name="Adresse")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    responsable = models.CharField(max_length=100, blank=True, verbose_name="Responsable")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Maître d'ouvrage"
        verbose_name_plural = "Maîtres d'ouvrage"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('maitre_ouvrage_detail', kwargs={'pk': self.pk})

class Prestataire(models.Model):
    """Service Provider/Contractor"""
    nom = models.CharField(max_length=200, verbose_name="Nom de l'entreprise")
    adresse = models.TextField(blank=True, verbose_name="Adresse")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    specialite = models.CharField(max_length=100, blank=True, verbose_name="Spécialité")
    numero_registre = models.CharField(max_length=50, blank=True, verbose_name="Numéro de registre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Prestataire"
        verbose_name_plural = "Prestataires"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('prestataire_detail', kwargs={'pk': self.pk})

class Marche(models.Model):
    """Public Market/Contract"""
    TYPE_CHOICES = [
        ('travaux', 'Travaux'),
        ('fournitures', 'Fournitures'),
        ('services', 'Services'),
        ('maintenance', 'Maintenance'),
    ]
    
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('suspendu', 'Suspendu'),
        ('annule', 'Annulé'),
    ]
    PERIODICITE_CHOICES = [
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuelle', 'Mensuelle'),
        ('trimestrielle', 'Trimestrielle'),
        ('semestrielle', 'Semestrielle'),
        ('annuelle', 'Annuelle'),
        ('ponctuelle', 'Ponctuelle'),
    ]


    numero = models.CharField(max_length=50, unique=True, verbose_name="Référence ")
    objet = models.TextField(verbose_name="Objet du marché")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    montant = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant (DH)")
    montant_annual= models.DecimalField(max_digits=15,null=True,blank=True, decimal_places=2, verbose_name="Montant Annuel (DH)")
    rest_a_payer = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant (DH)")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True, verbose_name="Prix unitaire (DH)")
    date_signature = models.DateField(null=True, blank=True, verbose_name="Date de signature")
    date_debut = models.DateField(null=True, blank=True, verbose_name="Date de début")
    date_fin = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours', verbose_name="Statut")
    maitre_ouvrage = models.ForeignKey(MaitreOuvrage, on_delete=models.CASCADE, verbose_name="Maître d'ouvrage")
    prestataire = models.ForeignKey(Prestataire, on_delete=models.CASCADE, verbose_name="Prestataire")
    marque = models.CharField(max_length=100,null=True,blank=True,verbose_name="Marque")
    quantite = models.PositiveIntegerField(null= True ,blank = True , verbose_name="Quantité")
    periodicite = models.CharField(max_length=20,null=True,blank=True, choices=PERIODICITE_CHOICES,verbose_name="Périodicité")
    description = models.TextField(blank=True,null= True,verbose_name="description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Marché"
        verbose_name_plural = "Marchés"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.numero} - {self.objet[:50]}"

    def get_absolute_url(self):
        return reverse('marche_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.pk:  
            self.rest_a_payer = self.montant
        super().save(*args, **kwargs)

class OrdreService(models.Model):
    """Ordre de service"""

    TYPE_CHOICES = [
        ('commencement', 'Commencement'),
        ('arret', 'Arrêt'),
        ('reprise', 'Reprise'),
        ('resiliation', 'Résiliation'),
        ('reception', 'Réception'),
        ('annule', 'Annulé'),
        ('autre', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]

    numero = models.CharField(max_length=50, unique=True, verbose_name="Désignation")
    objet = models.TextField(verbose_name="Objet")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES,default="Commencement" ,verbose_name="Type d'ordre de service")
    date_emission = models.DateField(null=True, blank=True, verbose_name="Date d'émission")
    date_execution = models.DateField(null=True, blank=True, verbose_name="Date d'exécution prévue")
    signataire = models.CharField(max_length=100, null=True, blank=True, verbose_name="Signataire")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut")
    fichier = models.FileField(upload_to='ordres_service/', null=True, blank=True, verbose_name="Fichier joint (PDF)")
    observations = models.TextField(null=True, blank=True, verbose_name="Observations complémentaires")

    marche = models.ForeignKey(
        Marche,
        on_delete=models.CASCADE,
        related_name='ordres_service',
        verbose_name="Marché concerné",
        null=True
    )

    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ordre de service"
        verbose_name_plural = "Ordres de service"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.numero} ({self.get_type_display()})"

class Decompte(models.Model):
    """Payment breakdown/Invoice"""
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('valide', 'Validé'),
        ('paye', 'Payé'),
        ('rejete', 'Rejeté'),
    ]

    numero = models.CharField(max_length=50, unique=True, verbose_name="Désignation")
    periode_debut = models.DateField(null=True, blank=True, verbose_name="Période début")
    periode_fin = models.DateField(null=True, blank=True, verbose_name="Période fin")
    montant_ht = models.DecimalField(max_digits=15,decimal_places=2, verbose_name="Montant HT (DH)")
    tva = models.DecimalField(max_digits=15,decimal_places=2,default=20,verbose_name="TVA (%)")
    unite_de_mesure = models.CharField(max_length=10, blank=True, null=True, verbose_name="Unité de mesure")
    quantite = models.PositiveIntegerField(null=True, blank=True, verbose_name="Quantité")
    montant_ttc = models.DecimalField(max_digits=15,decimal_places=2,editable=False)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon', verbose_name="Statut")
    fichier = models.FileField(upload_to='decompte/', null=True, blank=True, verbose_name="Fichier joint (PDF)")
    description = models.TextField(blank=True, null=True, verbose_name=" description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    marche = models.ForeignKey(
        Marche, 
        on_delete=models.CASCADE,  
        related_name='decomptes',
        null=True
    )


     # def save(self, *args, **kwargs):
        # if self.marche and self.periode_debut and self.periode_fin:
            # Vérifie que le montant annuel est bien défini
            #  montant_annuel = self.marche.montant_annual or Decimal(0)

            # Utilise la TVA définie ou par défaut à 20%
             # tva = self.tva if self.tva is not None else Decimal(20)

            # Vérifie que la date de début du marché est définie
             # date_debut_marche = self.marche.date_debut
             # if not date_debut_marche:
                 # raise ValueError("Le marché doit avoir une date de début définie")

            # Détermine le nombre de périodes par an en fonction de la périodicité
             # periodicite = self.marche.periodicite
             # if periodicite == 'trimestrielle':
                 # periodes_par_an = 4
            #  elif periodicite == 'semestrielle':
                 # periodes_par_an = 2
            #  else:
                 # periodes_par_an = 1  # annuelle ou autre

            # Calcul du montant par période
             # montant_par_periode = montant_annuel / Decimal(periodes_par_an)

            # Itération pour trouver la bonne période
            #  periode_actuelle = date_debut_marche
             # trouve = False

             # while periode_actuelle < self.periode_fin:
                 # periode_suivante = periode_actuelle + relativedelta(months=12 // periodes_par_an)

                #  if self.periode_debut >= periode_actuelle and self.periode_fin <= periode_suivante:
                    # #  self.montant_ht = montant_par_periode
                    #  self.montant_ttc = self.montant_ht * (1 + tva / 100)
                    #  trouve = True
                   #   break

                 # periode_actuelle = periode_suivante

            #if not trouve:
            
                #raise ValueError("La période du décompte ne correspond à aucune période du marché.")

        #super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Décompte"
        verbose_name_plural = "Décomptes"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.numero} "

class PV(models.Model):
    """Procès-Verbal (Official Report)"""
    TYPE_CHOICES = [
        ('reception provisoire', 'Réception provisoire'),
        ('reception defintive', 'Réception defintive'),
        ('reception defintive', 'Réception defintive parcielle'),
        #('reunion', 'Réunion'),
        #('visite', 'Visite'),
        #('expertise', 'Expertise'),
        ('autre', 'Autre'),
    ]

    numero = models.CharField(max_length=50, unique=True, verbose_name="Désignation")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    date_pv = models.DateField(null=True, blank=True, verbose_name="Date du PV")
    objet = models.TextField(verbose_name="Objet")
    observations = models.TextField(blank=True, verbose_name="Observations")
    fichier = models.FileField(upload_to='pv/', null=True, blank=True, verbose_name="Fichier joint (PDF)")
    signataire = models.CharField(max_length=100, null=True, blank=True, verbose_name="Signataire 1")
    signataire_deux = models.CharField(max_length=100, null=True, blank=True, verbose_name="Signataire 2")
    signataire_trois = models.CharField(max_length=100, null=True, blank=True, verbose_name="Signataire 3")
    periode_fin = models.DateField(null=True, blank=True, verbose_name="Période fin")
    periode_debut = models.DateField(null=True, blank=True, verbose_name="Période début")
    fonction_signataire = models.CharField(max_length=100, null=True, blank=True, verbose_name="Fonction du signataire")
    fonction_signataire_deux = models.CharField(max_length=100, null=True, blank=True, verbose_name="Fonction du signataire")
    fonction_signataire_trois = models.CharField(max_length=100, null=True, blank=True, verbose_name="Fonction du signataire")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    marche = models.ForeignKey(
        Marche, 
        on_delete=models.CASCADE,  
        related_name='pvs',
        null=True
    )

    class Meta:
        verbose_name = "Procès-Verbal"
        verbose_name_plural = "Procès-Verbaux"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.numero} - {self.type}"

class Document(models.Model):
    """Document storage"""
    TYPE_CHOICES = [
        ('contrat', 'Contrat'),
        ('facture', 'Facture'),
        ('devis', 'Devis'),
        ('plan', 'Plan'),
        ('rapport', 'Rapport'),
        ('photo', 'Photo'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=200, verbose_name="Nom du document")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True, verbose_name="Type")
    fichier = models.FileField(upload_to='documents/%Y/%m/', verbose_name="Fichier")
    taille = models.PositiveIntegerField(null=True, blank=True, verbose_name="Taille (bytes)")
    marche = models.ForeignKey(Marche, on_delete=models.CASCADE, related_name='documents', verbose_name="Marché")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Téléchargé par")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['-created_at']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if self.fichier:
            self.taille = self.fichier.size
        super().save(*args, **kwargs)