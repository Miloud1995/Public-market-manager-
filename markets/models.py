from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

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


    numero = models.CharField(max_length=50, unique=True, verbose_name="Numéro du marché")
    objet = models.TextField(verbose_name="Objet du marché")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    montant = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant (DH)")
    rest_a_payer = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant (DH)")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix unitaire (DH)")
    date_signature = models.DateField(null=True, blank=True, verbose_name="Date de signature")
    date_debut = models.DateField(null=True, blank=True, verbose_name="Date de début")
    date_fin = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours', verbose_name="Statut")
    maitre_ouvrage = models.ForeignKey(MaitreOuvrage, on_delete=models.CASCADE, verbose_name="Maître d'ouvrage")
    prestataire = models.ForeignKey(Prestataire, on_delete=models.CASCADE, verbose_name="Prestataire")
    marque = models.CharField(max_length=100, blank=True, verbose_name="Marque")
    periodicite = models.CharField(max_length=20, choices=PERIODICITE_CHOICES, blank=True, verbose_name="Périodicité")
    description = models.TextField(blank=True, verbose_name="description")
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
    """Service Order"""
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]

    numero = models.CharField(max_length=50, unique=True, verbose_name="Numéro")
    objet = models.TextField(verbose_name="Objet")
    date_emission = models.DateField(null=True, blank=True, verbose_name="Date d'émission")
    date_execution = models.DateField(null=True, blank=True, verbose_name="Date d'exécution")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    marche = models.ManyToManyField(
        Marche,
        related_name='OrdreServices',
        blank=True
    )

    class Meta:
        verbose_name = "Ordre de service"
        verbose_name_plural = "Ordres de service"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.numero} - {self.objet[:50]}"

class Decompte(models.Model):
    """Payment breakdown/Invoice"""
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('valide', 'Validé'),
        ('paye', 'Payé'),
        ('rejete', 'Rejeté'),
    ]

    numero = models.CharField(max_length=50, unique=True, verbose_name="Numéro")
    periode_debut = models.DateField(null=True, blank=True, verbose_name="Période début")
    periode_fin = models.DateField(null=True, blank=True, verbose_name="Période fin")
    montant_ht = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant HT (DH)")
    montant_ttc = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant TTC (DH)")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon', verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    marche = models.ForeignKey(
        Marche, 
        on_delete=models.CASCADE,  
        related_name='decomptes',
        null=True
    )
   

    class Meta:
        verbose_name = "Décompte"
        verbose_name_plural = "Décomptes"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.numero} - {self.montant_ttc}DH"

class PV(models.Model):
    """Procès-Verbal (Official Report)"""
    TYPE_CHOICES = [
        ('reception', 'Réception'),
        ('constat', 'Constat'),
        ('reunion', 'Réunion'),
        ('visite', 'Visite'),
        ('expertise', 'Expertise'),
        ('autre', 'Autre'),
    ]

    numero = models.CharField(max_length=50, unique=True, verbose_name="Numéro")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    date_pv = models.DateField(null=True, blank=True, verbose_name="Date du PV")
    objet = models.TextField(verbose_name="Objet")
    observations = models.TextField(blank=True, verbose_name="Observations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    marche = models.ManyToManyField(
        Marche,
        related_name='pvs',
        blank=True
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