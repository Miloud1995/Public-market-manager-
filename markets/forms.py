from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div
from .models import (
    MaitreOuvrage, Prestataire, Marche, 
     OrdreService, Decompte, PV, Document
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
        fields = ['numero', 'objet', 'type', 'montant','prix_unitaire', 'date_signature', 
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
                Column('statut', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('maitre_ouvrage', css_class='form-group col-md-6 mb-0'),
                Column('prestataire', css_class='form-group col-md-6 mb-0'),
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
        fields = ['numero', 'objet', 'date_emission', 'date_execution', 'statut', 'marche']
        widgets = {
            'objet': forms.Textarea(attrs={'rows': 3}),
            'date_emission': forms.DateInput(attrs={'type': 'date'}),
            'date_execution': forms.DateInput(attrs={'type': 'date'}),
        }

class DecompteForm(forms.ModelForm):
    class Meta:
        model = Decompte
        fields = ['numero', 'periode_debut', 'periode_fin', 'montant_ht', 'montant_ttc', 'statut', 'marche']
        widgets = {
            'periode_debut': forms.DateInput(attrs={'type': 'date'}),
            'periode_fin': forms.DateInput(attrs={'type': 'date'}),
            'marche': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['montant_ht'].widget.attrs.update({'step': '0.01'})
        self.fields['montant_ttc'].widget.attrs.update({'step': '0.01'})

        
        self.fields['marche'].queryset = Marche.objects.all().order_by('numero')
        self.fields['marche'].empty_label = "Sélectionnez un marché"  # Custom empty label
        self.fields['marche'].label = "Marché associé"  # Custom label
        self.helper.layout = Layout(
             Row(
                Column('numero', css_class='form-group col-md-6 mb-0'),
                Column('statut', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'objet',
            Row(
                Column('periode_debut', css_class='form-group col-md-6 mb-0'),
                Column('periode_fin', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('montant_ht', css_class='form-group col-md-6 mb-0'),
                Column('montant_ttc', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('marche', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
            
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )
class PVForm(forms.ModelForm):
    class Meta:
        model = PV
        fields = ['numero', 'type', 'date_pv', 'objet', 'observations', 'marche']
        widgets = {
            'date_pv': forms.DateInput(attrs={'type': 'date'}),
            'objet': forms.Textarea(attrs={'rows': 3}),
            'observations': forms.Textarea(attrs={'rows': 4}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['nom', 'type', 'fichier', 'marche']