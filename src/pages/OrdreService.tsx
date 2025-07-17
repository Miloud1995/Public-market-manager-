import React, { useState } from 'react';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import axios from 'axios';
import toast from 'react-hot-toast';

interface OrdreService {
  id?: number;
  numero: string;
  objet: string;
  date_emission: string;
  date_execution: string;
  statut: string;
  marche_id: number;
}

export default function OrdreService() {
  const [showModal, setShowModal] = useState(false);
  const [editingOrdre, setEditingOrdre] = useState<OrdreService | null>(null);
  const [formData, setFormData] = useState<OrdreService>({
    numero: '',
    objet: '',
    date_emission: '',
    date_execution: '',
    statut: 'en_attente',
    marche_id: 1
  });

  const columns = [
    { key: 'numero', label: 'Numéro' },
    { key: 'objet', label: 'Objet' },
    { 
      key: 'date_emission', 
      label: 'Date Émission',
      render: (value: string) => value ? new Date(value).toLocaleDateString('fr-FR') : '-'
    },
    { 
      key: 'date_execution', 
      label: 'Date Exécution',
      render: (value: string) => value ? new Date(value).toLocaleDateString('fr-FR') : '-'
    },
    { 
      key: 'statut', 
      label: 'Statut',
      render: (value: string) => (
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
          value === 'en_attente' ? 'bg-yellow-100 text-yellow-800' :
          value === 'en_cours' ? 'bg-blue-100 text-blue-800' :
          value === 'termine' ? 'bg-green-100 text-green-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {value.replace('_', ' ')}
        </span>
      )
    }
  ];

  const handleAdd = () => {
    setEditingOrdre(null);
    setFormData({
      numero: '',
      objet: '',
      date_emission: '',
      date_execution: '',
      statut: 'en_attente',
      marche_id: 1
    });
    setShowModal(true);
  };

  const handleEdit = (ordre: OrdreService) => {
    setEditingOrdre(ordre);
    setFormData(ordre);
    setShowModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingOrdre) {
        await axios.put(`http://localhost:3001/api/ordre_service/${editingOrdre.id}`, formData);
        toast.success('Ordre de service mis à jour avec succès');
      } else {
        await axios.post('http://localhost:3001/api/ordre_service', formData);
        toast.success('Ordre de service créé avec succès');
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
        <h1 className="text-2xl font-bold text-gray-900">Gestion des Ordres de Service</h1>
      </div>

      <DataTable
        endpoint="ordre_service"
        columns={columns}
        title="Liste des Ordres de Service"
        onAdd={handleAdd}
        onEdit={handleEdit}
        searchPlaceholder="Rechercher par numéro, objet..."
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={editingOrdre ? 'Modifier l\'Ordre de Service' : 'Nouvel Ordre de Service'}
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
                <option value="en_attente">En attente</option>
                <option value="en_cours">En cours</option>
                <option value="termine">Terminé</option>
                <option value="annule">Annulé</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Objet *
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
                Date d'émission
              </label>
              <input
                type="date"
                value={formData.date_emission}
                onChange={(e) => setFormData({ ...formData, date_emission: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date d'exécution
              </label>
              <input
                type="date"
                value={formData.date_execution}
                onChange={(e) => setFormData({ ...formData, date_execution: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
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
              {editingOrdre ? 'Mettre à jour' : 'Créer'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}