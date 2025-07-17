import React, { useState } from 'react';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import { Download } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

interface Marche {
  id?: number;
  numero: string;
  objet: string;
  type: string;
  montant: number;
  date_signature: string;
  date_debut: string;
  date_fin: string;
  statut: string;
  maitre_ouvrage_id: number;
  prestataire_id: number;
}

export default function Marches() {
  const [showModal, setShowModal] = useState(false);
  const [editingMarche, setEditingMarche] = useState<Marche | null>(null);
  const [formData, setFormData] = useState<Marche>({
    numero: '',
    objet: '',
    type: 'Travaux',
    montant: 0,
    date_signature: '',
    date_debut: '',
    date_fin: '',
    statut: 'en_cours',
    maitre_ouvrage_id: 1,
    prestataire_id: 1
  });

  const columns = [
    { key: 'numero', label: 'Numéro' },
    { key: 'objet', label: 'Objet' },
    { key: 'type', label: 'Type' },
    { 
      key: 'montant', 
      label: 'Montant',
      render: (value: number) => `${value.toLocaleString()} €`
    },
    { 
      key: 'date_signature', 
      label: 'Date Signature',
      render: (value: string) => new Date(value).toLocaleDateString('fr-FR')
    },
    { 
      key: 'statut', 
      label: 'Statut',
      render: (value: string) => (
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
          value === 'en_cours' ? 'bg-green-100 text-green-800' :
          value === 'termine' ? 'bg-blue-100 text-blue-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {value.replace('_', ' ')}
        </span>
      )
    }
  ];

  const handleAdd = () => {
    setEditingMarche(null);
    setFormData({
      numero: '',
      objet: '',
      type: 'Travaux',
      montant: 0,
      date_signature: '',
      date_debut: '',
      date_fin: '',
      statut: 'en_cours',
      maitre_ouvrage_id: 1,
      prestataire_id: 1
    });
    setShowModal(true);
  };

  const handleEdit = (marche: Marche) => {
    setEditingMarche(marche);
    setFormData(marche);
    setShowModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingMarche) {
        await axios.put(`http://localhost:3001/api/marche/${editingMarche.id}`, formData);
        toast.success('Marché mis à jour avec succès');
      } else {
        await axios.post('http://localhost:3001/api/marche', formData);
        toast.success('Marché créé avec succès');
      }
      setShowModal(false);
      window.location.reload();
    } catch (error) {
      toast.error('Erreur lors de la sauvegarde');
    }
  };

  const generatePDF = (marche: Marche) => {
    const doc = new jsPDF();
    
    // Header
    doc.setFontSize(20);
    doc.text('CONTRAT DE MARCHÉ PUBLIC', 20, 30);
    
    // Contract details
    doc.setFontSize(12);
    doc.text(`Numéro: ${marche.numero}`, 20, 50);
    doc.text(`Objet: ${marche.objet}`, 20, 60);
    doc.text(`Type: ${marche.type}`, 20, 70);
    doc.text(`Montant: ${marche.montant.toLocaleString()} €`, 20, 80);
    doc.text(`Date de signature: ${new Date(marche.date_signature).toLocaleDateString('fr-FR')}`, 20, 90);
    doc.text(`Date de début: ${new Date(marche.date_debut).toLocaleDateString('fr-FR')}`, 20, 100);
    doc.text(`Date de fin: ${new Date(marche.date_fin).toLocaleDateString('fr-FR')}`, 20, 110);
    doc.text(`Statut: ${marche.statut}`, 20, 120);
    
    // Terms and conditions
    doc.text('CONDITIONS GÉNÉRALES:', 20, 140);
    doc.setFontSize(10);
    const terms = [
      '1. Le présent marché est conclu conformément aux dispositions du Code des marchés publics.',
      '2. Les prestations devront être exécutées dans les délais convenus.',
      '3. Le paiement s\'effectuera selon les modalités définies dans le marché.',
      '4. Toute modification du marché devra faire l\'objet d\'un avenant.'
    ];
    
    terms.forEach((term, index) => {
      doc.text(term, 20, 150 + (index * 10));
    });
    
    // Signatures
    doc.setFontSize(12);
    doc.text('Maître d\'ouvrage:', 20, 200);
    doc.text('Prestataire:', 120, 200);
    
    doc.text('Signature:', 20, 220);
    doc.text('Signature:', 120, 220);
    
    doc.save(`marche_${marche.numero}.pdf`);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Gestion des Marchés</h1>
      </div>

      <DataTable
        endpoint="marche"
        columns={columns}
        title="Liste des Marchés"
        onAdd={handleAdd}
        onEdit={handleEdit}
        searchPlaceholder="Rechercher par numéro, objet..."
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={editingMarche ? 'Modifier le Marché' : 'Nouveau Marché'}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Numéro
              </label>
              <input
                type="text"
                value={formData.numero}
                onChange={(e) => setFormData({ ...formData, numero: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type
              </label>
              <select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="Travaux">Travaux</option>
                <option value="Fournitures">Fournitures</option>
                <option value="Services">Services</option>
                <option value="Maintenance">Maintenance</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Objet
            </label>
            <textarea
              value={formData.objet}
              onChange={(e) => setFormData({ ...formData, objet: e.target.value })}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Montant (€)
              </label>
              <input
                type="number"
                step="0.01"
                value={formData.montant}
                onChange={(e) => setFormData({ ...formData, montant: parseFloat(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Statut
              </label>
              <select
                value={formData.statut}
                onChange={(e) => setFormData({ ...formData, statut: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="en_cours">En cours</option>
                <option value="termine">Terminé</option>
                <option value="suspendu">Suspendu</option>
                <option value="annule">Annulé</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date de signature
              </label>
              <input
                type="date"
                value={formData.date_signature}
                onChange={(e) => setFormData({ ...formData, date_signature: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date de début
              </label>
              <input
                type="date"
                value={formData.date_debut}
                onChange={(e) => setFormData({ ...formData, date_debut: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date de fin
              </label>
              <input
                type="date"
                value={formData.date_fin}
                onChange={(e) => setFormData({ ...formData, date_fin: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-gray-200">
            {editingMarche && (
              <button
                type="button"
                onClick={() => generatePDF(formData as Marche)}
                className="flex items-center gap-2 text-blue-600 hover:text-blue-800"
              >
                <Download className="w-4 h-4" />
                Générer PDF
              </button>
            )}
            <div className="flex items-center gap-2 ml-auto">
              <button
                type="button"
                onClick={() => setShowModal(false)}
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Annuler
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                {editingMarche ? 'Mettre à jour' : 'Créer'}
              </button>
            </div>
          </div>
        </form>
      </Modal>
    </div>
  );
}