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
    marche = get_object_or_404(Prestataire, pk=pk)
    services = marche.services.all()
    maintenances = marche.maintenances.all()
    fournitures = marche.fournitures.all()
    ordres_service = marche.ordres_service.all()
    decomptes = marche.decomptes.all()
    pvs = marche.pvs.all()
    documents = marche.documents.all()
    
    return render(request, 'markets/maitre_detail.html', {
        'marche': marche,
        'services': services,
        'maintenances': maintenances,
        'fournitures': fournitures,
        'ordres_service': ordres_service,
        'decomptes': decomptes,
        'pvs': pvs,
        'documents': documents,
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
    #ordres_service = marche.ordres_service.all()
    #decomptes = marche.decomptes.all()
    #pvs = marche.pvs.all()
    #documents = marche.documents.all()
    
    return render(request, 'markets/marche_detail.html', {
        'marche': marche,
        'decomptes': decomptes
        
        #'ordres_service': ordres_service,
        #'decomptes': decomptes,
        #'pvs': pvs,
        #'documents': documents,
    })

@login_required
def prestataire_detail(request, pk):
    marche = get_object_or_404(Prestataire, pk=pk)
    services = marche.services.all()
    maintenances = marche.maintenances.all()
    fournitures = marche.fournitures.all()
    ordres_service = marche.ordres_service.all()
    decomptes = marche.decomptes.all()
    pvs = marche.pvs.all()
    documents = marche.documents.all()
    
    return render(request, 'markets/marche_detail.html', {
        'marche': marche,
        'services': services,
        'maintenances': maintenances,
        'fournitures': fournitures,
        'ordres_service': ordres_service,
        'decomptes': decomptes,
        'pvs': pvs,
        'documents': documents,
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
@login_required
def decompte_create(request):
   
     if request.method == 'POST':
        form = DecompteForm(request.POST)
        if form.is_valid():
            try:
                decompte = form.save(commit=False)
                
                # Only process if we have a marché and period dates
                if decompte.marche and decompte.periode_debut and decompte.periode_fin:
                    # Validate period dates
                    if decompte.periode_debut > decompte.periode_fin:
                        form.add_error('periode_fin', "La date de fin doit être postérieure à la date de début")
                        return render(request, 'markets/decompte_form.html', {'form': form})

                    # Get annual amount
                    montant_annuel = decompte.marche.montant_annual or Decimal(0)

                    # Verify marché start date exists
                    if not decompte.marche.date_debut:
                        form.add_error(None, "Le marché associé doit avoir une date de début définie")
                        return render(request, 'markets/decompte_form.html', {'form': form})

                    # Determine periods per year
                    periodicite = decompte.marche.periodicite.lower() if decompte.marche.periodicite else 'annuelle'
                    periodes_par_an = {
                        'trimestrielle': 4,
                        'semestrielle': 2,
                        'mensuelle': 12,
                        'annuelle': 1
                    }.get(periodicite, 1)

                    # Calculate amount per period
                    montant_par_periode = montant_annuel / Decimal(periodes_par_an)

                    # Find matching period
                    periode_actuelle = decompte.marche.date_debut
                    trouve = False
                    
                    while periode_actuelle < decompte.periode_fin:
                        periode_suivante = periode_actuelle + relativedelta(months=12//periodes_par_an)

                        if (decompte.periode_debut >= periode_actuelle and 
                            decompte.periode_fin <= periode_suivante):
                            decompte.montant_ht = montant_par_periode.quantize(Decimal('0.01'))
                            decompte.montant_ttc = (decompte.montant_ht * (1 + decompte.tva/100)).quantize(Decimal('0.01'))
                            trouve = True
                            break

                        periode_actuelle = periode_suivante

                    if not trouve:
                        form.add_error(None, "La période ne correspond à aucune période du marché")
                        return render(request, 'markets/decompte_form.html', {'form': form})

                # Handle paid status logic
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
    
    # Sauvegarde de l'ancien statut et montant pour comparaison
    old_statut = decompte.statut
    old_montant = decompte.montant_ttc
    
    if request.method == 'POST':
        form = DecompteForm(request.POST, instance=decompte)
        if form.is_valid():
            new_decompte = form.save(commit=False)
            
            if new_decompte.statut == 'paye':
                marche = new_decompte.marche
                new_montant = new_decompte.montant_ttc
                
                # Cas 1: Le décompte devient "payé" (ancien statut différent)
                if old_statut != 'paye':
                    if marche.rest_a_payer >= new_montant:
                        marche.rest_a_payer -= new_montant
                    else:
                        messages.error(request, "Le montant dépasse le reste à payer.")
                        return render(request, 'markets/decompte_form.html', 
                                    {'form': form, 'title': 'Modifier Decompte'})
                
                # Cas 2: Le montant a changé sur un décompte déjà payé
                elif old_montant != new_montant:
                    # On annule d'abord l'ancien montant
                    marche.rest_a_payer += old_montant
                    # Puis on applique le nouveau
                    if marche.rest_a_payer >= new_montant:
                        marche.rest_a_payer -= new_montant
                    else:
                        # On remet l'ancienne valeur si problème
                        marche.rest_a_payer -= old_montant
                        messages.error(request, "Le nouveau montant dépasse le reste à payer.")
                        return render(request, 'markets/decompte_form.html', 
                                    {'form': form, 'title': 'Modifier Decompte'})
                
                marche.save()
            
            # Cas 3: Le décompte n'est plus "payé" (on annule la précédente déduction)
            elif old_statut == 'paye' and new_decompte.statut != 'paye':
                marche = new_decompte.marche
                marche.rest_a_payer += old_montant
                marche.save()
            
            new_decompte.save()
            messages.success(request, 'Decompte mis à jour avec succès.')
            return redirect('decompte_list')
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
@login_required
def generate_decompte_pdf(request, pk):
    decompte = get_object_or_404(Decompte, pk=pk)
    
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="marche_{decompte.numero}.pdf"'
    
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
    title = Paragraph("DECOMPTE", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # decompte information
    data = [
        ['Désignation du decompte:', decompte.numero],
        ['periode debut:', decompte.periode_debut],
        ['Periode Fin:', decompte.periode_fin],
         ['Montant TTC:', f"{decompte.montant_ttc:,.2f} DH"],
         ['Montant HT:', f"{decompte.montant_ht:,.2f} DH"],
         ['TVA:', f"{decompte.tva}%"],
        ['Statut:', decompte.get_statut_display()],
         ['Marché:', decompte.marche.objet],
       
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.gray),
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
    #terms_title = Paragraph("CONDITIONS GÉNÉRALES", styles['Heading2'])
   # elements.append(terms_title)
    #elements.append(Spacer(1, 12))
    
    #terms = [
       # "1. Le présent marché est conclu conformément aux dispositions du decret n°2-22-431 relatif aux marches publics.",
       # "2. Les prestations devront être exécutées dans les délais convenus.",
        #"3. Le paiement s'effectuera selon les modalités définies dans le marché.",
       # "4. Toute modification du marché devra faire l'objet d'un avenant."
   # ]
    
    #for term in terms:
       # p = Paragraph(term, styles['Normal'])
        #elements.append(p)
       # elements.append(Spacer(1, 6))
    
   # elements.append(Spacer(1, 30))
    
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



#Decompte delete
@login_required
def decompte_delete(request, pk):
    decompte = get_object_or_404(Decompte, pk=pk)
    if request.method == 'POST':
       decompte .delete()
       messages.success(request, 'Decompte  supprimé avec succès.')
       return redirect('decompte_list')
    return render(request, 'markets/confirm_delete.html', {'object': decompte, 'type': 'Decompte'})
