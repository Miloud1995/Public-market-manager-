import React, { useState } from 'react';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import axios from 'axios';
import toast from 'react-hot-toast';

interface Maintenance {
  id?: number;
  libelle: string;
  description: string;
  prix_unitaire: number;
  periodicite: string;
  marche_id: number;
}

export default function Maintenance() {
  const [showModal, setShowModal] = useState(false);
  const [editingMaintenance, setEditingMaintenance] = useState<Maintenance | null>(null);
  const [formData, setFormData] = useState<Maintenance>({
    libelle: '',
    description: '',
    prix_unitaire: 0,
    periodicite: '',
    marche_id: 1
  });

  const columns = [
    { key: 'libelle', label: 'Libellé' },
    { key: 'description', label: 'Description' },
    { 
      key: 'prix_unitaire', 
      label: 'Prix Unitaire',
      render: (value: number) => `${value.toLocaleString()} €`
    },
    { key: 'periodicite', label: 'Périodicité' }
  ];

  const handleAdd = () => {
    setEditingMaintenance(null);
    setFormData({
      libelle: '',
      description: '',
      prix_unitaire: 0,
      periodicite: '',
      marche_id: 1
    });
    setShowModal(true);
  };

  const handleEdit = (maintenance: Maintenance) => {
    setEditingMaintenance(maintenance);
    setFormData(maintenance);
    setShowModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingMaintenance) {
        await axios.put(`http://localhost:3001/api/maintenance/${editingMaintenance.id}`, formData);
        toast.success('Maintenance mise à jour avec succès');
      } else {
        await axios.post('http://localhost:3001/api/maintenance', formData);
        toast.success('Maintenance créée avec succès');
      }
      setShowModal(false);
      window.location.reload();
    } catch (error) {
      toast.error('Erreur lors de la sauvegarde');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Gestion de la Maintenance</h1>
      </div>

      <DataTable
        endpoint="maintenance"
        columns={columns}
        title="Liste des Maintenances"
        onAdd={handleAdd}
        onEdit={handleEdit}
        searchPlaceholder="Rechercher par libellé..."
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={editingMaintenance ? 'Modifier la Maintenance' : 'Nouvelle Maintenance'}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Libellé *
            </label>
            <input
              type="text"
              value={formData.libelle}
              onChange={(e) => setFormData({ ...formData, libelle: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Prix unitaire (€)
              </label>
              <input
                type="number"
                step="0.01"
                value={formData.prix_unitaire}
                onChange={(e) => setFormData({ ...formData, prix_unitaire: parseFloat(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Périodicité
              </label>
              <select
                value={formData.periodicite}
                onChange={(e) => setFormData({ ...formData, periodicite: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Sélectionner...</option>
                <option value="Hebdomadaire">Hebdomadaire</option>
                <option value="Mensuelle">Mensuelle</option>
                <option value="Trimestrielle">Trimestrielle</option>
                <option value="Semestrielle">Semestrielle</option>
                <option value="Annuelle">Annuelle</option>
                <option value="Ponctuelle">Ponctuelle</option>
              </select>
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
              {editingMaintenance ? 'Mettre à jour' : 'Créer'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}