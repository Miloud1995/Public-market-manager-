import React, { useState } from 'react';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import axios from 'axios';
import toast from 'react-hot-toast';

interface Decompte {
  id?: number;
  numero: string;
  periode_debut: string;
  periode_fin: string;
  montant_ht: number;
  montant_ttc: number;
  statut: string;
  marche_id: number;
}

export default function Decomptes() {
  const [showModal, setShowModal] = useState(false);
  const [editingDecompte, setEditingDecompte] = useState<Decompte | null>(null);
  const [formData, setFormData] = useState<Decompte>({
    numero: '',
    periode_debut: '',
    periode_fin: '',
    montant_ht: 0,
    montant_ttc: 0,
    statut: 'brouillon',
    marche_id: 1
  });

  const columns = [
    { key: 'numero', label: 'Numéro' },
    { 
      key: 'periode_debut', 
      label: 'Période Début',
      render: (value: string) => value ? new Date(value).toLocaleDateString('fr-FR') : '-'
    },
    { 
      key: 'periode_fin', 
      label: 'Période Fin',
      render: (value: string) => value ? new Date(value).toLocaleDateString('fr-FR') : '-'
    },
    { 
      key: 'montant_ht', 
      label: 'Montant HT',
      render: (value: number) => `${value.toLocaleString()} €`
    },
    { 
      key: 'montant_ttc', 
      label: 'Montant TTC',
      render: (value: number) => `${value.toLocaleString()} €`
    },
    { 
      key: 'statut', 
      label: 'Statut',
      render: (value: string) => (
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
          value === 'brouillon' ? 'bg-gray-100 text-gray-800' :
          value === 'valide' ? 'bg-green-100 text-green-800' :
          value === 'paye' ? 'bg-blue-100 text-blue-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {value}
        </span>
      )
    }
  ];

  const handleAdd = () => {
    setEditingDecompte(null);
    setFormData({
      numero: '',
      periode_debut: '',
      periode_fin: '',
      montant_ht: 0,
      montant_ttc: 0,
      statut: 'brouillon',
      marche_id: 1
    });
    setShowModal(true);
  };

  const handleEdit = (decompte: Decompte) => {
    setEditingDecompte(decompte);
    setFormData(decompte);
    setShowModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingDecompte) {
        await axios.put(`http://localhost:3001/api/decompte/${editingDecompte.id}`, formData);
        toast.success('Décompte mis à jour avec succès');
      } else {
        await axios.post('http://localhost:3001/api/decompte', formData);
        toast.success('Décompte créé avec succès');
      }
      setShowModal(false);
      window.location.reload();
    } catch (error) {
      toast.error('Erreur lors de la sauvegarde');
    }
  };

  // Calculate TTC automatically when HT changes (assuming 20% VAT)
  const handleMontantHTChange = (value: number) => {
    const montantTTC = value * 1.2;
    setFormData({ ...formData, montant_ht: value, montant_ttc: montantTTC });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Gestion des Décomptes</h1>
      </div>

      <DataTable
        endpoint="decompte"
        columns={columns}
        title="Liste des Décomptes"
        onAdd={handleAdd}
        onEdit={handleEdit}
        searchPlaceholder="Rechercher par numéro..."
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={editingDecompte ? 'Modifier le Décompte' : 'Nouveau Décompte'}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Numéro *
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
                Statut
              </label>
              <select
                value={formData.statut}
                onChange={(e) => setFormData({ ...formData, statut: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="brouillon">Brouillon</option>
                <option value="valide">Validé</option>
                <option value="paye">Payé</option>
                <option value="rejete">Rejeté</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Période début
              </label>
              <input
                type="date"
                value={formData.periode_debut}
                onChange={(e) => setFormData({ ...formData, periode_debut: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Période fin
              </label>
              <input
                type="date"
                value={formData.periode_fin}
                onChange={(e) => setFormData({ ...formData, periode_fin: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Montant HT (€)
              </label>
              <input
                type="number"
                step="0.01"
                value={formData.montant_ht}
                onChange={(e) => handleMontantHTChange(parseFloat(e.target.value) || 0)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Montant TTC (€)
              </label>
              <input
                type="number"
                step="0.01"
                value={formData.montant_ttc}
                onChange={(e) => setFormData({ ...formData, montant_ttc: parseFloat(e.target.value) || 0 })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">
                Calculé automatiquement avec TVA 20%
              </p>
            </div>
          </div>

          <div className="flex items-center justify-end gap-2 pt-4 border-t border-gray-200">
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
              {editingDecompte ? 'Mettre à jour' : 'Créer'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}