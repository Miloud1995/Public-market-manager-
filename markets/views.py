from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from dateutil.relativedelta import relativedelta
import io
from datetime import datetime
from django.db import transaction
from decimal import Decimal, InvalidOperation
from dateutil.relativedelta import relativedelta 
from reportlab.lib.units import inch, cm
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
import io
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

from .models import Decompte  # adapte selon ton projet



from .models import (
    MaitreOuvrage, Prestataire, Marche, 
     OrdreService, Decompte, PV, Document
)
from .forms import (
    MaitreOuvrageForm, PrestataireForm, MarcheForm,  
    OrdreServiceForm, DecompteForm, 
    PVForm, DocumentForm
)

@login_required
def dashboard(request):
    """Dashboard with statistics"""
    context = {
        'total_marches': Marche.objects.count(),
        'marches_en_cours': Marche.objects.filter(statut='en_cours').count(),
        'total_prestataires': Prestataire.objects.count(),
        'total_maitre_ouvrage': MaitreOuvrage.objects.count(),
        'montant_total': Marche.objects.aggregate(Sum('montant'))['montant__sum'] or 0,
        'recent_marches': Marche.objects.select_related('prestataire', 'maitre_ouvrage').order_by('-created_at')[:5],
        'recent_decomptes': Decompte.objects.prefetch_related('marche').order_by('-created_at')[:5],
    }
    return render(request, 'markets/dashboard.html', context)

# Maître d'Ouvrage Views
@login_required
def maitre_ouvrage_list(request):
    nom_query = request.GET.get('nom', '')
    responsable_query = request.GET.get('responsable', '')
    maitre_ouvrages = MaitreOuvrage.objects.all()
    
    if nom_query:
        maitre_ouvrages = maitre_ouvrages.filter
        Q(nom__icontains=nom_query) 
           
        

    if responsable_query:
        maitre_ouvrages = maitre_ouvrages.filter
        Q(responsable__icontains=responsable_query)   
        
    
    paginator = Paginator(maitre_ouvrages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'markets/maitre_ouvrage_list.html', {
        'page_obj': page_obj,
        'nom_query': nom_query,
        'responsable_query': responsable_query
    })

@login_required
def maitre_ouvrage_create(request):
    if request.method == 'POST':
        form = MaitreOuvrageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maître d\'ouvrage créé avec succès.')
            return redirect('maitre_ouvrage_list')
    else:
        form = MaitreOuvrageForm()
    return render(request, 'markets/maitre_ouvrage_form.html', {'form': form, 'title': 'Nouveau Maître d\'Ouvrage'})

@login_required
def maitre_ouvrage_update(request, pk):
    maitre_ouvrage = get_object_or_404(MaitreOuvrage, pk=pk)
    if request.method == 'POST':
        form = MaitreOuvrageForm(request.POST, instance=maitre_ouvrage)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maître d\'ouvrage mis à jour avec succès.')
            return redirect('maitre_ouvrage_list')
    else:
        form = MaitreOuvrageForm(instance=maitre_ouvrage)
    return render(request, 'markets/maitre_ouvrage_form.html', {'form': form, 'title': 'Modifier Maître d\'Ouvrage'})

@login_required
def maitre_ouvrage_detail(request, pk):
    maitre = get_object_or_404(MaitreOuvrage, pk=pk)
   
    return render(request, 'markets/maitre_detail.html', {
        'maitre': maitre,
       
    })
@login_required
def maitre_ouvrage_delete(request, pk):
    maitre_ouvrage = get_object_or_404(MaitreOuvrage, pk=pk)
    if request.method == 'POST':
        maitre_ouvrage.delete()
        messages.success(request, 'Maître d\'ouvrage supprimé avec succès.')
        return redirect('maitre_ouvrage_list')
    return render(request, 'markets/confirm_delete.html', {'object': maitre_ouvrage, 'type': 'Maître d\'Ouvrage'})

# Prestataire Views
@login_required
def prestataire_list(request):
    search_query = request.GET.get('search', '')
    prestataires = Prestataire.objects.all()
    
   
    if search_query:
        prestataires = prestataires.filter(nom__icontains=search_query)
           
        
    
    paginator = Paginator(prestataires, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'markets/prestataire_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })

@login_required
def prestataire_create(request):
    if request.method == 'POST':
        form = PrestataireForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prestataire créé avec succès.')
            return redirect('prestataire_list')
    else:
        form = PrestataireForm()
    return render(request, 'markets/prestataire_form.html', {'form': form, 'title': 'Nouveau Prestataire'})

@login_required
def prestataire_update(request, pk):
    prestataire = get_object_or_404(Prestataire, pk=pk)
    if request.method == 'POST':
        form = PrestataireForm(request.POST, instance=prestataire)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prestataire mis à jour avec succès.')
            return redirect('prestataire_list')
    else:
        form = PrestataireForm(instance=prestataire)
    return render(request, 'markets/prestataire_form.html', {'form': form, 'title': 'Modifier Prestataire'})

@login_required
def prestataire_detail(request, pk):
    prestataire = get_object_or_404(Prestataire, pk=pk)
   
    
    return render(request, 'markets/prestataire_detail.html', {
        'prestataire': prestataire,
        
    })


@login_required
def prestataire_delete(request, pk):
    prestataire = get_object_or_404(Prestataire, pk=pk)
    if request.method == 'POST':
        prestataire.delete()
        messages.success(request, 'Prestataire supprimé avec succès.')
        return redirect('prestataire_list')
    return render(request, 'markets/confirm_delete.html', {'object': prestataire, 'type': 'Prestataire'})

# Marché Views
@login_required
def marche_list(request):
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')
    statut_filter = request.GET.get('statut', '')
    
    marches = Marche.objects.select_related('prestataire', 'maitre_ouvrage').all()
    
    
    if search_query:
        marches = marches.filter(
            Q(numero__icontains=search_query) | 
            Q(objet__icontains=search_query) |
            Q(prestataire__nom__icontains=search_query)
        )
    
    if type_filter:
        marches = marches.filter(type=type_filter)
    
    if statut_filter:
        marches = marches.filter(statut=statut_filter)
    
    paginator = Paginator(marches, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'markets/marche_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'type_filter': type_filter,
        'statut_filter': statut_filter,
        'type_choices': Marche.TYPE_CHOICES,
        'statut_choices': Marche.STATUT_CHOICES,
    })

@login_required
def marche_create(request):
    if request.method == 'POST':
        form = MarcheForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marché créé avec succès.')
            return redirect('marche_list')
    else:
        form = MarcheForm()
    return render(request, 'markets/marche_form.html', {'form': form, 'title': 'Nouveau Marché'})

@login_required
def marche_detail(request, pk):
    marche = get_object_or_404(Marche, pk=pk)
    decomptes = marche.decomptes.all()
    ordres_service = marche.ordres_service.all()
    #decomptes = marche.decomptes.all()
    #pvs = marche.pvs.all()
    #documents = marche.documents.all()
    
    return render(request, 'markets/marche_detail.html', {
        'marche': marche,
        'decomptes': decomptes,
        
        'ordres_service': ordres_service,
        #'decomptes': decomptes,
        #'pvs': pvs,
        #'documents': documents,
    })


@login_required
def marche_update(request, pk):
    marche = get_object_or_404(Marche, pk=pk)
    if request.method == 'POST':
        form = MarcheForm(request.POST, instance=marche)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marché mis à jour avec succès.')
            return redirect('marche_detail', pk=pk)
    else:
        form = MarcheForm(instance=marche)
    return render(request, 'markets/marche_form.html', {'form': form, 'title': 'Modifier Marché'})

@login_required
def marche_delete(request, pk):
    marche = get_object_or_404(Marche, pk=pk)
    if request.method == 'POST':
       marche.delete()
       messages.success(request, 'Marché supprimé avec succès.')
       return redirect('marche_list')
    return render(request, 'markets/confirm_delete.html', {'object': marche, 'type': 'Marché'})

# PDF Generation
@login_required
def generate_marche_pdf(request, pk):
    marche = get_object_or_404(Marche, pk=pk)
    
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="marche_{marche.numero}.pdf"'
    
    # Create the PDF object
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center alignment
    )
    
    # Add title
    title = Paragraph("CONTRAT DE MARCHÉ PUBLIC", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Market information
    data = [
        ['Numéro du marché:', marche.numero],
        ['Objet:', marche.objet],
        ['Type:', marche.get_type_display()],
        ['Montant:', f"{marche.montant:,.2f} DH"],
        ['Statut:', marche.get_statut_display()],
        ['Date de signature:', marche.date_signature.strftime('%d/%m/%Y') if marche.date_signature else 'Non définie'],
        ['Date de début:', marche.date_debut.strftime('%d/%m/%Y') if marche.date_debut else 'Non définie'],
        ['Date de fin:', marche.date_fin.strftime('%d/%m/%Y') if marche.date_fin else 'Non définie'],
        ['Maître d\'ouvrage:', marche.maitre_ouvrage.nom],
        ['Prestataire:', marche.prestataire.nom],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Terms and conditions
    terms_title = Paragraph("CONDITIONS GÉNÉRALES", styles['Heading2'])
    elements.append(terms_title)
    elements.append(Spacer(1, 12))
    
    terms = [
        "1. Le présent marché est conclu conformément aux dispositions du decret n°2-22-431 relatif aux marches publics.",
        "2. Les prestations devront être exécutées dans les délais convenus.",
        "3. Le paiement s'effectuera selon les modalités définies dans le marché.",
        "4. Toute modification du marché devra faire l'objet d'un avenant."
    ]
    
    for term in terms:
        p = Paragraph(term, styles['Normal'])
        elements.append(p)
        elements.append(Spacer(1, 6))
    
    elements.append(Spacer(1, 30))
    
    # Signatures
    signature_data = [
        ['Maître d\'ouvrage', 'Prestataire'],
        ['', ''],
        ['Signature:', 'Signature:'],
    ]
    
    signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
    ]))
    
    elements.append(signature_table)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response


@login_required
def decompte_create(request):
    if request.method == 'POST':
        form = DecompteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                decompte = form.save(commit=False)
                
                if decompte.marche and decompte.periode_debut and decompte.periode_fin:
                    # Validation des dates
                    if decompte.periode_debut > decompte.periode_fin:
                        form.add_error('periode_fin', "La date de fin doit être postérieure à la date de début")
                        return render(request, 'markets/decompte_form.html', {'form': form})

                    if not decompte.marche.date_debut:
                        form.add_error(None, "Le marché associé doit avoir une date de début définie")
                        return render(request, 'markets/decompte_form.html', {'form': form})

                    montant_annuel = decompte.marche.montant_annual or Decimal(0)
                    periodicite = decompte.marche.periodicite.lower() if decompte.marche.periodicite else 'annuelle'

                    # Nouveau calcul proportionnel
                    if periodicite in ['trimestrielle', 'semestrielle', 'mensuelle']:
                        # Calcul du nombre de jours dans la période du décompte
                        jours_periode = (decompte.periode_fin - decompte.periode_debut).days + 1
                        
                        # Calcul du nombre de jours dans l'année
                        jours_annee = 366 if decompte.periode_debut.year % 4 == 0 else 365
                        
                        # Calcul proportionnel
                        montant_proportionnel = (montant_annuel * Decimal(jours_periode)) / Decimal(jours_annee)
                        decompte.montant_ht = montant_proportionnel.quantize(Decimal('0.01'))
                    else:
                        # Pour la périodicité annuelle, on prend le montant complet
                        decompte.montant_ht = montant_annuel.quantize(Decimal('0.01'))

                    # Calcul du TTC
                    decompte.montant_ttc = (decompte.montant_ht * (1 + decompte.tva/100)).quantize(Decimal('0.01'))

                    # Vérification du reste à payer si le statut est payé
                    if decompte.statut == 'paye':
                        marche = decompte.marche
                        if marche.rest_a_payer < decompte.montant_ttc:
                            form.add_error('montant_ttc', "Le montant dépasse le reste à payer")
                            return render(request, 'markets/decompte_form.html', {'form': form})
                        marche.rest_a_payer -= decompte.montant_ttc
                        marche.save()

                    decompte.save()
                    messages.success(request, 'Décompte créé avec succès.')
                    return redirect('decompte_list')

            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {str(e)}")
                return render(request, 'markets/decompte_form.html', {'form': form})
    else:
        form = DecompteForm()
    
    return render(request, 'markets/decompte_form.html', {'form': form})

@login_required
def decompte_update(request, pk):
    decompte = get_object_or_404(Decompte, pk=pk)
    
    # Sauvegarde des anciennes valeurs
    old_statut = decompte.statut
    old_montant_ht = decompte.montant_ht
    old_montant_ttc = decompte.montant_ttc
    
    if request.method == 'POST':
        form = DecompteForm(request.POST, instance=decompte)
        if form.is_valid():
            try:
                new_decompte = form.save(commit=False)
                
                # Recalcul des montants si la période ou le marché change
                if (new_decompte.marche and new_decompte.periode_debut and new_decompte.periode_fin and 
                    (new_decompte.marche != decompte.marche or 
                     new_decompte.periode_debut != decompte.periode_debut or
                     new_decompte.periode_fin != decompte.periode_fin)):
                    
                    # Validation des dates
                    if new_decompte.periode_debut > new_decompte.periode_fin:
                        form.add_error('periode_fin', "La date de fin doit être postérieure à la date de début")
                        return render(request, 'markets/decompte_form.html', 
                                    {'form': form, 'title': 'Modifier Decompte'})

                    if not new_decompte.marche.date_debut:
                        form.add_error(None, "Le marché associé doit avoir une date de début définie")
                        return render(request, 'markets/decompte_form.html', 
                                    {'form': form, 'title': 'Modifier Decompte'})

                    montant_annuel = new_decompte.marche.montant_annual or Decimal(0)
                    periodicite = new_decompte.marche.periodicite.lower() if new_decompte.marche.periodicite else 'annuelle'

                    # Calcul proportionnel
                    if periodicite in ['trimestrielle', 'semestrielle', 'mensuelle']:
                        jours_periode = (new_decompte.periode_fin - new_decompte.periode_debut).days + 1
                        jours_annee = 366 if new_decompte.periode_debut.year % 4 == 0 else 365
                        new_decompte.montant_ht = (montant_annuel * Decimal(jours_periode) / Decimal(jours_annee)).quantize(Decimal('0.01'))
                    else:
                        new_decompte.montant_ht = montant_annuel.quantize(Decimal('0.01'))

                    # Calcul du nouveau TTC
                    new_decompte.montant_ttc = (new_decompte.montant_ht * (1 + new_decompte.tva/100)).quantize(Decimal('0.01'))

                # Gestion du statut payé
                if new_decompte.statut == 'paye':
                    marche = new_decompte.marche
                    new_montant = new_decompte.montant_ttc
                    
                    # Cas 1: Devenu payé
                    if old_statut != 'paye':
                        if marche.rest_a_payer >= new_montant:
                            marche.rest_a_payer -= new_montant
                        else:
                            messages.error(request, "Le montant dépasse le reste à payer.")
                            return render(request, 'markets/decompte_form.html', 
                                        {'form': form, 'title': 'Modifier Decompte'})
                    
                    # Cas 2: Montant modifié sur un décompte payé
                    elif old_montant_ttc != new_montant:
                        marche.rest_a_payer += old_montant_ttc
                        if marche.rest_a_payer >= new_montant:
                            marche.rest_a_payer -= new_montant
                        else:
                            marche.rest_a_payer -= old_montant_ttc  # Annulation
                            messages.error(request, "Le nouveau montant dépasse le reste à payer.")
                            return render(request, 'markets/decompte_form.html', 
                                        {'form': form, 'title': 'Modifier Decompte'})
                    
                    marche.save()
                
                # Cas 3: N'est plus payé
                elif old_statut == 'paye' and new_decompte.statut != 'paye':
                    marche = new_decompte.marche
                    marche.rest_a_payer += old_montant_ttc
                    marche.save()

                new_decompte.save()
                messages.success(request, 'Decompte mis à jour avec succès.')
                return redirect('decompte_list')

            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {str(e)}")
                return render(request, 'markets/decompte_form.html', 
                            {'form': form, 'title': 'Modifier Decompte'})
    else:
        form = DecompteForm(instance=decompte)
    
    return render(request, 'markets/decompte_form.html', 
                 {'form': form, 'title': 'Modifier Decompte'}) 


@login_required
def decompte_list(request):
    
    #decompte = Decompte.objects.prefetch_related('marche').all()
    decompte = Decompte.objects.select_related('marche').all()
    #marches = Marche.objects.prefetch_related('decomptes').all()  
    marches = Marche.objects.select_related('decomptes').all()
   
    paginator = Paginator(decompte, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'markets/decompte_list.html', {
        'page_obj': page_obj,          # Paginated Decomptes
        'all_marches': marches,        # All Marches with related Decomptes
        'statut_choices': Decompte.STATUT_CHOICES,
    })




#generate PDF for Decompte
import io
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from openpyxl.utils import get_column_letter


from .models import Decompte  # adapte selon ton projet

@login_required
def generate_decompte_pdf(request, pk):
    decompte = get_object_or_404(Decompte, pk=pk)

    # Créer le fichier Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Décompte Provisoire"

    # Styles
    bold = Font(bold=True)
    center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )

    # === Titre ===
    ws.merge_cells("A1:F1")
    ws["A1"] = f"DÉCOMPTE PROVISOIRE N°{decompte.numero}"
    ws["A1"].font = Font(bold=True, size=14)
    ws["A1"].alignment = center

    ws.merge_cells("A2:F2")
    ws["A2"] = f"Prestations réalisées Du {decompte.periode_debut} au {decompte.periode_fin}"
    ws["A2"].font = bold
    ws["A2"].alignment = center

    # === En-têtes du tableau ===
    headers = ["N° des prix", "Désignation", "Unité de mesure", "Qté",
               "Prix unitaire hors TVA", "Prix Total"]
    ws.append(headers)

    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=3, column=col)
        cell.font = bold
        cell.alignment = center
        cell.border = thin_border

    # === Ligne prestation ===
    prix_total = decompte.montant_ht  # supposons que tu stockes le HT
    ws.append([1,
               decompte.numero,   # si tu as un champ "designation"
               #decompte.unite,         # champ unité
               decompte.quantite,      # champ quantité
               #decompte.prix_unitaire, # champ prix unitaire
               prix_total])

    for col in range(1, 7):
        cell = ws.cell(row=4, column=col)
        cell.border = thin_border
        cell.alignment = center

    # === Totaux ===
    montant_tva = decompte.montant_ttc - decompte.montant_ht

    ws.merge_cells("A6:E6")
    ws["A6"] = "Total Annuel Hors TVA"
    ws["A6"].font = bold
    ws["F6"] = decompte.montant_ht

    ws.merge_cells("A7:E7")
    ws["A7"] = f"TVA {decompte.tva}%"
    ws["A7"].font = bold
    ws["F7"] = montant_tva

    ws.merge_cells("A8:E8")
    ws["A8"] = f"TOTAL des Prestations réalisées Du {decompte.periode_debut} au {decompte.periode_fin} TTC"
    ws["A8"].font = bold
    ws["F8"] = decompte.montant_ttc

    # === Récapitulatif ===
    ws.merge_cells("A10:F10")
    ws["A10"] = "RECAPITULATION GENERALE"
    ws["A10"].font = bold
    ws["A10"].alignment = center
 
    recap = [
        ["NATURES DES DEPENSES", "DEPENSES FAITES"],
        ["Prestations réalisées", decompte.montant_ttc],
        ["TOTAUX TTC", decompte.montant_ttc],
        ["A déduire le montant des acomptes délivrés sur l'exercice en cours", ""],
        ["Montant de l'acompte à délivrer en DH TTC", decompte.montant_ttc],
        [f"   Dont T.V.A (à {decompte.tva}%)", montant_tva]
    ]

    for row in recap:
        ws.append(row)

    for col_cells in ws.columns:
        max_length = 0
        column = get_column_letter(col_cells[0].column)  # au lieu de col[0].column_letter
    for cell in col_cells:
        try:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        except:
            pass
    ws.column_dimensions[column].width = max_length + 3


    # Préparer la réponse HTTP
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename="decompte_{decompte.numero}.xlsx"'

    output = io.BytesIO()
    wb.save(output)
    response.write(output.getvalue())

    return response



#Decompte delete
@login_required
def decompte_delete(request, pk):
    decompte = get_object_or_404(Decompte, pk=pk)
    if request.method == 'POST':
       decompte .delete()
       messages.success(request, 'Decompte  supprimé avec succès.')
       return redirect('decompte_list')
    return render(request, 'markets/confirm_delete.html', {'object': decompte, 'type': 'Decompte'})

@login_required
def decompte_detail(request, pk):
    decompte = get_object_or_404(Decompte, pk=pk)
    return render(request, 'markets/decompte_detail.html', {
        'decompte': decompte,
        'marche': decompte.marche
    })




########"""

# Order SErvice Views

@login_required
def order_list(request):
    
    #decompte = Decompte.objects.prefetch_related('marche').all()
    order = OrdreService.objects.select_related('marche').all()
    #marches = Marche.objects.prefetch_related('decomptes').all()  
    marches = Marche.objects.select_related('order_services').all()
   
    paginator = Paginator(order, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'markets/order_service_list.html', {
        'page_obj': page_obj,          # Paginated Decomptes
        'all_marches': marches,        # All Marches with related Decomptes
        'statut_choices': OrdreService.STATUT_CHOICES,
    })




@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrdreServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ordre de service créé avec succès.')
            return redirect('order_list')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = OrdreServiceForm()

    return render(request, 'markets/order_form.html', {
        'form': form,
        'title': 'Nouveau ordre de service'
    })



@login_required
def order_detail(request, pk):
    order = get_object_or_404(OrdreService, pk=pk)
    return render(request, 'markets/order_detail.html', {
        'order': order,
        'marche': OrdreService.marche
    })

@login_required
def order_update(request, pk):
    order = get_object_or_404(OrdreService, pk=pk)
    if request.method == 'POST':
        form = OrdreServiceForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order de sevice mis à jour avec succès.')
            return redirect('order_detail', pk=pk)
    else:
        form = OrdreServiceForm(instance=order)
    return render(request, 'markets/order_form.html', {'form': form, 'title': 'Modifier Order de Service'})


@login_required
def order_delete(request, pk):
    order = get_object_or_404(OrdreService, pk=pk)
    if request.method == 'POST':
       order.delete()
       messages.success(request, 'Marché supprimé avec succès.')
       return redirect('order_list')
    return render(request, 'markets/confirm_delete.html', {'object': order, 'type': 'Order de Service'})





@login_required
def generate_ordre_service_pdf(request, pk):
    ordre = get_object_or_404(OrdreService, pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ordre_service_{ordre.numero}.pdf"'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm
    )

    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('Bold', parent=normal, fontName='Helvetica-Bold')
    centered = ParagraphStyle('Centered', parent=normal, alignment=1, fontSize=12, spaceAfter=10)
    paragraph_style = ParagraphStyle('Justify', parent=normal, alignment=4, leading=15, fontSize=11)

    elements = []

    # En-tête avec logos
    try:
        logo_left = Image("static/img/logo1.png", width=3*cm, height=3*cm)
        logo_center = Image("static/img/logo2.png", width=3*cm, height=3*cm)
        logo_right = Image("static/img/logo3.png", width=3*cm, height=3*cm)
        header_table = Table([[logo_left, logo_center, logo_right]], colWidths=[5*cm, 5*cm, 5*cm])
        header_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
        elements.append(header_table)
    except:
        pass

    elements.append(Spacer(1, 12))

    # Référence
    elements.append(Paragraph(f"Réf : {ordre.numero}", normal))
    elements.append(Spacer(1, 12))

    # Titre
    elements.append(Paragraph(f"<b>Ordre de Service N° {ordre.numero}</b>", centered))

    # === Paragraphe principal selon le type d'ordre ===
    if ordre.type == 'commencement':
        texte = f"""
        La Trésorerie Générale du Royaume, représentée par {ordre.marche.maitre_ouvrage or '________________'},
        invite la société <b>{ordre.marche.prestataire.nom if ordre.marche and ordre.marche.prestataire else '________________'}</b>,
        à exécuter à compter du {ordre.date_execution.strftime('%d/%m/%Y') if ordre.date_execution else '____/____/____'},
        les prestations relatives au marché <b>{ordre.marche.numero if ordre.marche else '____________'}</b>,
        concernant {ordre.objet}.
        """
    elif ordre.type == 'arret':
        texte = f"""
        La Trésorerie Générale du Royaume, représentée par {ordre.marche.maitre_ouvrage or '________________'},
        ordonne l’arrêt des prestations prévues dans le marché <b>{ordre.marche.numero if ordre.marche else '____________'}</b>,
        exécutées par la société <b>{ordre.marche.prestataire.nom if ordre.marche and ordre.marche.prestataire else '________________'}</b>,
        à compter du {ordre.date_execution.strftime('%d/%m/%Y') if ordre.date_execution else '____/____/____'}.
        """
    elif ordre.type == 'reprise':
        texte = f"""
        La Trésorerie Générale du Royaume, représentée par {ordre.marche.maitre_ouvrage or '________________'},
        ordonne la reprise des prestations relatives au marché <b>{ordre.marche.numero if ordre.marche else '____________'}</b>,
        confiées à la société <b>{ordre.marche.prestataire.nom if ordre.marche and ordre.marche.prestataire else '________________'}</b>,
        à compter du {ordre.date_execution.strftime('%d/%m/%Y') if ordre.date_execution else '____/____/____'}.
        """
    else:
        texte = f"""
        La Trésorerie Générale du Royaume, représentée par {ordre.marche.maitre_ouvrage or '________________'},
        informe la société <b>{ordre.marche.prestataire.nom if ordre.marche and ordre.marche.prestataire else '________________'}</b>
        concernant {ordre.objet}.
        """

    # Ajouter le paragraphe choisi
    elements.append(Paragraph(texte, paragraph_style))
    elements.append(Spacer(1, 20))

    # Date et signature (partie 1)
    elements.append(Paragraph(f"{ordre.date_emission.strftime('%d/%m/%Y') if ordre.date_emission else '____/____/____'}", normal))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Signature et cachet", normal))
    elements.append(Spacer(1, 30))

    # Ligne de séparation
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<b>Notification</b>", centered))

    # Notification texte
    notif_text = f"""
    Je soussigné(e) ____________________, représentant la société <b>{ordre.marche.prestataire.nom if ordre.marche and ordre.marche.prestataire else '________________'}</b>,
    reconnais avoir reçu de la Trésorerie Générale du Royaume un exemplaire de l'ordre de service
    concernant le marché <b>{ordre.marche.numero if ordre.marche else '____________'}</b>.
    """
    elements.append(Paragraph(notif_text, paragraph_style))
    elements.append(Spacer(1, 20))

    # Date et signature (partie 2)
    elements.append(Paragraph(f"{ordre.date_emission.strftime('%d/%m/%Y') if ordre.date_emission else '____/____/____'}", normal))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Signature et cachet du prestataire", normal))

    # Génération PDF
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required
def pv_create(request):
    if request.method == 'POST':
        form = PVForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'PV créé avec succès.')
            return redirect('pv_list')
    else:
        form = PVForm()
    return render(request, 'markets/pv_form.html', {'form': form, 'title': 'Nouveau PV'})

@login_required
def pv_list(request):
    
    #decompte = Decompte.objects.prefetch_related('marche').all()
    pv = PV.objects.select_related('marche').all()
    #marches = Marche.objects.prefetch_related('decomptes').all()  
    marches = Marche.objects.select_related('pv').all()
   
    paginator = Paginator(pv, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'markets/pv_list.html', {
        'page_obj': page_obj,          # Paginated Decomptes
        'all_marches': marches,        # All Marches with related Decomptes
        'statut_choices': OrdreService.STATUT_CHOICES,
    })


@login_required
def pv_update(request, pk):
    pv = get_object_or_404(PV, pk=pk)
    if request.method == 'POST':
        form = PVForm(request.POST, instance=pv)
        if form.is_valid():
            form.save()
            messages.success(request, 'PV  mis à jour avec succès.')
            return redirect('pv_detail', pk=pk)
    else:
        form = PVForm(instance=pv)
    return render(request, 'markets/pv_form.html', {'form': form, 'title': 'Modifier PV'})


@login_required
def pv_detail(request, pk):
    pv = get_object_or_404(PV, pk=pk)
    return render(request, 'markets/pv_detail.html', {
        'pv': pv,
        'marche': PV.marche
    })

@login_required
def pv_delete(request, pk):
    pv = get_object_or_404(PV, pk=pk)
    if request.method == 'POST':
       pv.delete()
       messages.success(request, 'PV supprimé avec succès.')
       return redirect('pv_list')
    return render(request, 'markets/confirm_delete.html', {'object': pv, 'type': 'pv'})


@login_required
def generate_pv_pdf(request, pk):
    pv = get_object_or_404(PV, pk=pk)

    # Préparer la réponse HTTP
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="pv_{pv.numero}.pdf"'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    elements = []
    styles = getSampleStyleSheet()

    # === Styles personnalisés ===
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=14,
        spaceAfter=20,
        leading=18,
    )
    justify_style = ParagraphStyle(
        "Justify",
        parent=styles["Normal"],
        alignment=TA_JUSTIFY,
        fontSize=11,
        leading=16,
    )

    # === Logos en haut ===
    logo1 = Image("static/img/logo1.png", width=100, height=100)
    logo2 = Image("static/img/logo2.png", width=100, height=100)
    logo3 = Image("static/img/logo3.png", width=100, height=100)

    logos_table = Table([[logo1, logo2, logo3]], colWidths=[150, 150, 150])
    logos_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
            ]
        )
    )
    elements.append(logos_table)
    elements.append(Spacer(1, 20))

    # === Choix du contenu selon le type de PV ===
    if pv.type == "reception provisoire":
        title = f"PROCÈS VERBAL DE RÉCEPTION PROVISOIRE<br/>RELATIF AU MARCHÉ {pv.marche.type} N° {pv.numero}"
        corps = f"""
        Le {pv.date_pv.strftime('%d %B %Y')} ; la commission chargée de la réception provisoire du marché N° {pv.numero}, 
        relatif à {pv.objet}, composée de :<br/><br/>
        • {pv.signataire or ''} ({pv.fonction_signataire or ''})<br/>
        • {pv.signataire_deux or ''} ({pv.fonction_signataire_deux or ''})<br/><br/>
        a constaté que les prestations exécutées par la société {pv.marche.prestataire} sont terminées et conformes.<br/><br/>
        En conséquence, la réception provisoire est prononcée.<br/><br/>
        <b>Fait à Rabat, le {pv.date_pv.strftime('%d/%m/%Y')}</b>.
        """

    elif pv.type == "reception defintive":
        title = f"PROCÈS VERBAL DE RÉCEPTION DÉFINITIVE<br/>RELATIF AU MARCHÉ {pv.marche.type} N° {pv.numero}"
        corps = f"""
        Le {pv.date_pv.strftime('%d %B %Y')} ; la commission chargée de la réception définitive du marché N° {pv.numero}, 
        relatif à {pv.objet}, composée de :<br/><br/>
        • {pv.signataire or ''} ({pv.fonction_signataire or ''})<br/>
        • {pv.signataire_deux or ''} ({pv.fonction_signataire_deux or ''})<br/><br/>
        a reconnu que toutes les prestations exécutées par la société {pv.marche.prestataire} sont conformes aux conditions du marché.<br/><br/>
        En conséquence, la réception définitive est prononcée.<br/><br/>
        <b>Fait à Rabat, le {pv.date_pv.strftime('%d/%m/%Y')}</b>.
        """

    elif pv.type == "reception defintive parcielle":
        title = f"PROCÈS VERBAL DE RÉCEPTION DÉFINITIVE PARTIELLE<br/>RELATIF AU MARCHÉ {pv.marche.type} N° {pv.numero}"
        corps = f"""
        Le {pv.date_pv.strftime('%d %B %Y')} ; la commission chargée de la réception définitive partielle du marché N° {pv.numero}, 
        relatif à {pv.objet}, composée de :<br/><br/>
        • {pv.signataire or ''} ({pv.fonction_signataire or ''})<br/>
        • {pv.signataire_deux or ''} ({pv.fonction_signataire_deux or ''})<br/><br/>
        a reconnu que les prestations exécutées par la société {pv.marche.prestataire}, 
        pour la période {pv.periode_debut or ''} au {pv.periode_fin or ''}, 
        sont conformes aux conditions du marché.<br/><br/>
        En conséquence, la réception définitive partielle est prononcée.<br/><br/>
        <b>Fait à Rabat, le {pv.date_pv.strftime('%d/%m/%Y')}</b>.
        """

    else:
        title = f"PROCÈS VERBAL<br/>Marché N° {pv.numero}"
        corps = f"""
        Ce procès-verbal a été établi le {pv.date_pv.strftime('%d %B %Y')} 
        concernant le marché N° {pv.numero}, relatif à {pv.objet}.
        """

    # === Ajouter titre et corps ===
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(corps, justify_style))
    elements.append(Spacer(1, 30))

    # === Signatures ===
    elements.append(Paragraph("<b>Signé :</b>", styles["Normal"]))
    elements.append(Spacer(1, 12))

    signataires = []
    if pv.signataire:
        signataires.append([f"• {pv.signataire} ({pv.fonction_signataire or ''})", ""])
    if pv.signataire_deux:
        signataires.append([f"• {pv.signataire_deux} ({pv.fonction_signataire_deux or ''})", ""])
    if pv.signataire_trois:
        signataires.append([f"• {pv.signataire_trois} ({pv.fonction_signataire_trois or ''})", ""])

    if signataires:
        table = Table(signataires, colWidths=[250, 250])
        table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
                ]
            )
        )
        elements.append(table)

    # === Génération du PDF ===
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response