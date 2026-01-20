from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div
from .models import (
    MaitreOuvrage, Prestataire, Marche, 
     OrdreService, Decompte, PV, Document,Acompte,Signataire,Ligne
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
        fields = ['representant','nom', 'adresse', 'telephone', 'email', 'specialite', 'numero_registre','cnss','patente','compte','capital']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='form-group col-md-4 mb-0'),
                Column('representant', css_class='form-group col-md-4 mb-0'),
                Column('specialite', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'adresse',
            Row(
                Column('telephone', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                Column('numero_registre', css_class='form-group col-md-4 mb-0'),
                Column('cnss', css_class='form-group col-md-4 mb-0'),
                Column('patente', css_class='form-group col-md-4 mb-0'),
                Column('compte', css_class='form-group col-md-4 mb-0'),
                Column('capital', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )



from django import forms
from .models import Ligne

class LigneForm(forms.ModelForm):
    class Meta:
        model = Ligne
        fields = [
            'numero_prix', 'designation', 'unite_mesure','quantite','prix_unitaire',
            'marche'
            
        ]
        widgets = {
            
        }

    def __init__(self, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        self.fields['marche'].queryset = Marche.objects.all().order_by('numero')
        self.fields['marche'].empty_label = "Sélectionnez un marché"
        self.fields['marche'].label = "Marché associé"

        self.helper.layout = Layout(
            Row(
                Column('numero_prix', css_class='form-group col-md-6 mb-0'),
                Column('designation', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
           
            
            Row(
                Column('unite_mesure', css_class='form-group col-md-4 mb-0'),
                Column('quantite', css_class='form-group col-md-4 mb-0'),
                
                
                css_class='form-row'
            ),

             Row(
                Column('prix_unitaire', css_class='form-group col-md-4 mb-0'),
                Column('marche', css_class='form-group col-md-4 mb-0'),
                
                
                css_class='form-row'
            ),
         
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')  
        )

class MarcheForm(forms.ModelForm):
    class Meta:
        model = Marche
        fields = ['numero', 'objet', 'type', 'montant','montant_annual','quantite','prix_unitaire', 'date_signature', 
                 'date_debut', 'date_fin', 'statut', 'maitre_ouvrage', 'prestataire','marque', 'periodicite','description','rest_a_payer']
        #exclude = ['rest_a_payer']
        widgets = {
            'objet': forms.Textarea(attrs={'rows': 3}),
            'date_signature': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
            'date_debut': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
            'date_fin': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
            'description' : forms.Textarea(attrs={'rows':3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['rest_a_payer'].widget = forms.HiddenInput()
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
                
                css_class='form-row'
            ),
            Row(
                Column('statut', css_class='form-group col-md-4 mb-0'),
                Column('maitre_ouvrage', css_class='form-group col-md-4 mb-0'),
                Column('prestataire', css_class='form-group col-md-4 mb-0'),
                #Column('quantite', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date_signature', css_class='form-group col-md-4 mb-0'),
                Column('date_debut', css_class='form-group col-md-4 mb-0'),
                Column('date_fin', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                
                #Column('marque', css_class='form-group col-md-4 mb-0'),
                
                Column('periodicite', css_class='form-group col-md-6 mb-0'),
                Column('rest_a_payer', css_class='form-group col-md-6 mb-0'),
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
            'date_emission': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
            'date_execution': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
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
        exclude = ['created_at','updated_at']
        fields = [
            'numero', 'periode_debut', 'periode_fin', 'periodicite',
            'marche', 'acompte', 'type', 'tva', 'montant_ttc',
            'quantite', 'statut', 'fichier'
        ]

        widgets = {
            'periode_debut': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
            'periode_fin': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
            'marche': forms.Select(attrs={'class': 'form-control'}),
            'acompte': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Make sure the field exists before filtering
        if 'acompte' in self.fields:
            self.fields['acompte'].queryset = Acompte.objects.filter(decompte__isnull=True)
            self.fields['acompte'].label = "Acompte associé"
        
        is_update = self.instance.pk is not None
        if not is_update:
    # Création
           self.fields['montant_ttc'].disabled = True
           self.fields['montant_ttc'].required = False
        else:
    # Modification
           self.fields['montant_ttc'].disabled = False
        # ✅ Marché dropdown
        self.fields['marche'].queryset = Marche.objects.all().order_by('numero')
        self.fields['marche'].empty_label = "Sélectionnez un marché"
        self.fields['marche'].label = "Marché associé"

        # ✅ Layout configuration (crispy-forms)
        layout = [
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
                Column('marche', css_class='form-group col-md-4 mb-0'),
                Column('acompte', css_class='form-group col-md-4 mb-0'),
                Column('tva', css_class='form-group col-md-4 mb-0'),
            ),
            
          
        
        ]
        if is_update:layout.append(Row(
                Column('montant_ttc', css_class='form-group col-md-12 mb-0'),
            ))

        layout.extend([ Row(
        Column('fichier', css_class='form-group col-md-12 mb-0'),
         ),
          Submit('submit', 'Enregistrer', css_class='btn btn-primary')])
        self.helper = FormHelper()
        self.helper.layout = Layout(*layout)
           
        




class PVForm(forms.ModelForm):
    class Meta:
        model = PV
        fields = [
            'numero', 'type', 'date_pv','periode_debut','periode_fin', 'objet', 'observations',
            'marche', 'signataires',
             'fichier',
        ]
        widgets = {
            'date_pv': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
            'periode_debut': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
            'periode_fin': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
            'objet': forms.Textarea(attrs={'rows': 3}),
            'signataires': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'observations': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['signataires'].queryset = Signataire.objects.all().order_by('nom')
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
                Column('date_pv', css_class='form-group col-md-4 mb-0'),
                Column('periode_debut', css_class='form-group col-md-4 mb-0'),
                Column('periode_fin', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
            Row(Column('marche', css_class='form-group col-md-6 mb-0'),
            Column('signataires', css_class='form-group col-md-6 mb-0'),
            css_class='form-row'),
            
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
from .models import Acompte, Marche,Signataire

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




class SignataireForm(forms.ModelForm):
    class Meta:
        model = Signataire
        fields = [
            'nom',
            'fonction',
            'email',
            'telephone', 
        ]

        widgets = {
            
            'marche': forms.Select(attrs={'class': 'form-control'}),
        
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        

        self.helper = FormHelper()
        self.helper.layout = Layout(
            
            Row(
                Column('nom', css_class='form-group col-md-6 mb-0'),
                Column('fonction', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('telephone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            
            Submit('submit', 'Enregistrer', css_class='btn btn-primary mt-3')
        )
