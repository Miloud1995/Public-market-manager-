from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div
from .models import (
    MaitreOuvrage, Prestataire, Marche, 
     OrdreService, Decompte, PV, Document,Acompte
)

class MaitreOuvrageForm(forms.ModelForm):
    class Meta:
        model = MaitreOuvrage
        fields = ['nom', 'adresse', 'telephone', 'email', 'responsable']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='form-group col-md-8 mb-0'),
                Column('responsable', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'adresse',
            Row(
                Column('telephone', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )

class PrestataireForm(forms.ModelForm):
    class Meta:
        model = Prestataire
        fields = ['nom', 'adresse', 'telephone', 'email', 'specialite', 'numero_registre']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='form-group col-md-8 mb-0'),
                Column('specialite', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'adresse',
            Row(
                Column('telephone', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                Column('numero_registre', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )

class MarcheForm(forms.ModelForm):
    class Meta:
        model = Marche
        fields = ['numero', 'objet', 'type', 'montant','montant_annual','quantite','prix_unitaire', 'date_signature', 
                 'date_debut', 'date_fin', 'statut', 'maitre_ouvrage', 'prestataire','marque', 'periodicite','description']
        exclude = ['rest_a_payer']
        widgets = {
            'objet': forms.Textarea(attrs={'rows': 3}),
            'date_signature': forms.DateInput(attrs={'type': 'date'}),
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'description' : forms.Textarea(attrs={'rows':3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('numero', css_class='form-group col-md-6 mb-0'),
                Column('type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'objet',
            Row(
                Column('montant', css_class='form-group col-md-6 mb-0'),
                Column('montant_annual', css_class='form-group col-md-6 mb-0'),
                Column('statut', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('maitre_ouvrage', css_class='form-group col-md-6 mb-0'),
                Column('prestataire', css_class='form-group col-md-6 mb-0'),
                Column('quantite', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date_signature', css_class='form-group col-md-4 mb-0'),
                Column('date_debut', css_class='form-group col-md-4 mb-0'),
                Column('date_fin', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('prix_unitaire', css_class='form-group col-md-4 mb-0'),
                Column('marque', css_class='form-group col-md-4 mb-0'),
                Column('periodicite', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'description',
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )


class OrdreServiceForm(forms.ModelForm):
    class Meta:
        model = OrdreService
        fields = ['numero', 'objet','type', 'date_emission', 'date_execution', 'statut','signataire', 'marche','observations','fichier']
        widgets = {
            'objet': forms.Textarea(attrs={'rows': 3}),
            'date_emission': forms.DateInput(attrs={'type': 'date'}),
            'date_execution': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        
         #self.fields['montant_ttc'].widget.attrs.update({'step': '0.1'})

        
        self.fields['marche'].queryset = Marche.objects.all().order_by('numero')
        self.fields['marche'].empty_label = "Sélectionnez un marché"  # Custom empty label
        self.fields['marche'].label = "Marché associé"  # Custom label
        self.helper.layout = Layout(
             Row(
                Column('numero', css_class='form-group col-md-6 mb-0'),
                Column('type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'objet',
            Row(
                Column('date_emission', css_class='form-group col-md-6 mb-0'),
                Column('date_execution', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
           
            Row(
                Column('signataire', css_class='form-group col-md-4 mb-0'),
                Column('statut', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

            Column('observations', css_class='form-group col-md-12 mb-0'),
            Column('marche', css_class='form-group col-md-12 mb-0'),
            
            Column('fichier', css_class='form-group col-md-4 mb-0'),
               
            
            
            
           
            
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )

class DecompteForm(forms.ModelForm):
    class Meta:
        model = Decompte
        fields = [
            'numero', 'periode_debut', 'periode_fin', 'periodicite',
            'marche', 'acompte', 'type', 'tva', 'unite_de_mesure',
            'quantite', 'statut', 'fichier'
        ]

        widgets = {
            'periode_debut': forms.DateInput(attrs={'type': 'date'}),
            'periode_fin': forms.DateInput(attrs={'type': 'date'}),
            'marche': forms.Select(attrs={'class': 'form-control'}),
            'acompte': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Make sure the field exists before filtering
        if 'acompte' in self.fields:
            self.fields['acompte'].queryset = Acompte.objects.filter(decompte__isnull=True)
            self.fields['acompte'].label = "Acompte associé"

        # ✅ Marché dropdown
        self.fields['marche'].queryset = Marche.objects.all().order_by('numero')
        self.fields['marche'].empty_label = "Sélectionnez un marché"
        self.fields['marche'].label = "Marché associé"

        # ✅ Layout configuration (crispy-forms)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('numero', css_class='form-group col-md-4 mb-0'),
                Column('statut', css_class='form-group col-md-4 mb-0'),
                Column('type', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('periode_debut', css_class='form-group col-md-4 mb-0'),
                Column('periode_fin', css_class='form-group col-md-4 mb-0'),
                Column('periodicite', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('marche', css_class='form-group col-md-6 mb-0'),
                Column('acompte', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('tva', css_class='form-group col-md-4 mb-0'),
                Column('unite_de_mesure', css_class='form-group col-md-4 mb-0'),
                Column('quantite', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('fichier', css_class='form-group col-md-12 mb-0'),
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )
        
class PVForm(forms.ModelForm):
    class Meta:
        model = PV
        fields = [
            'numero', 'type', 'date_pv','periode_debut','periode_fin', 'objet', 'observations',
            'marche', 'signataire', 'signataire_deux','fonction_signataire','fonction_signataire_deux','fonction_signataire_trois',
            'signataire_trois', 'fichier',
        ]
        widgets = {
            'date_pv': forms.DateInput(attrs={'type': 'date'}),
            'periode_debut': forms.DateInput(attrs={'type': 'date'}),
            'periode_fin': forms.DateInput(attrs={'type': 'date'}),
            'objet': forms.Textarea(attrs={'rows': 3}),
            'observations': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.fields['marche'].queryset = Marche.objects.all().order_by('numero')
        self.fields['marche'].empty_label = "Sélectionnez un marché"
        self.fields['marche'].label = "Marché associé"

        self.helper.layout = Layout(
            Row(
                Column('numero', css_class='form-group col-md-6 mb-0'),
                Column('type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            'objet',
             Row(
                Column('signataire', css_class='form-group col-md-4 mb-0'),
                Column('signataire_deux', css_class='form-group col-md-4 mb-0'),
                Column('signataire_trois', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('fonction_signataire', css_class='form-group col-md-4 mb-0'),
                Column('fonction_signataire_deux', css_class='form-group col-md-4 mb-0'),
                Column('fonction_signataire_trois', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date_pv', css_class='form-group col-md-4 mb-0'),
                Column('periode_debut', css_class='form-group col-md-4 mb-0'),
                Column('periode_fin', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
            Column('marche', css_class='form-group col-md-6 mb-0'),
            'observations',
            Row(
                Column('fichier', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')  
        )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['nom', 'type', 'fichier', 'marche','date_doc','uploaded_by']

    def __init__(self, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.fields['marche'].queryset = Marche.objects.all().order_by('numero')
        self.fields['marche'].empty_label = "Sélectionnez un marché"
        self.fields['marche'].label = "Marché associe"

        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='form-group col-md-12 mb-0'),
               
                css_class='form-row'
            ),
            
             Row(
                Column('type', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('date_doc', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            
             Row(
                Column('uploaded_by', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('marche', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('fichier', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),

             Submit('submit', 'Enregistrer', css_class='btn btn-primary')  
            
        )

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Acompte, Marche

class AcompteForm(forms.ModelForm):
    class Meta:
        model = Acompte
        fields = [
            'numero',
            'objet',
            'statut',
            'date_acompte',
            'periode_debut',
            'periode_fin',
            'marche',
            'pourcentage_realisation',
            'observation',
            'document_justificatif',
        ]

        widgets = {
            'periode_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'periode_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_acompte': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'marche': forms.Select(attrs={'class': 'form-control'}),
            'observation': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'objet': forms.TextInput(attrs={'class': 'form-control'}),
            'pourcentage_realisation': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['marche'].queryset = Marche.objects.all().order_by('numero')
        self.fields['marche'].empty_label = "Sélectionnez un marché"
        self.fields['marche'].label = "Marché associé"

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('numero', css_class='form-group col-md-4 mb-0'),
                Column('statut', css_class='form-group col-md-4 mb-0'),
                Column('marche', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'objet',
            Row(
                Column('date_acompte', css_class='form-group col-md-4 mb-0'),
                Column('periode_debut', css_class='form-group col-md-4 mb-0'),
                Column('periode_fin', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('pourcentage_realisation', css_class='form-group col-md-6 mb-0'),
                Column('document_justificatif', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row('observation', css_class='form-group col-md-12 mb-0'),
            Submit('submit', 'Enregistrer', css_class='btn btn-primary mt-3')
        )
