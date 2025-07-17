import React, { useState } from 'react';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import axios from 'axios';
import toast from 'react-hot-toast';

interface PV {
  id?: number;
  numero: string;
  type: string;
  date_pv: string;
  objet: string;
  observations: string;
  marche_id: number;
}

export default function PV() {
  const [showModal, setShowModal] = useState(false);
  const [editingPV, setEditingPV] = useState<PV | null>(null);
  const [formData, setFormData] = useState<PV>({
    numero: '',
    type: 'reception',
    date_pv: '',
    objet: '',
    observations: '',
    marche_id: 1
  });

  const columns = [
    { key: 'numero', label: 'Numéro' },
    { key: 'type', label: 'Type' },
    { 
      key: 'date_pv', 
      label: 'Date PV',
      render: (value: string) => value ? new Date(value).toLocaleDateString('fr-FR') : '-'
    },
    { key: 'objet', label: 'Objet' }
  ];

  const handleAdd = () => {
    setEditingPV(null);
    setFormData({
      numero: '',
      type: 'reception',
      date_pv: '',
      objet: '',
      observations: '',
      marche_id: 1
    });
    setShowModal(true);
  };

  const handleEdit = (pv: PV) => {
    setEditingPV(pv);
    setFormData(pv);
    setShowModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingPV) {
        await axios.put(`http://localhost:3001/api/pv/${editingPV.id}`, formData);
        toast.success('PV mis à jour avec succès');
      } else {
        await axios.post('http://localhost:3001/api/pv', formData);
        toast.success('PV créé avec succès');
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
        <h1 className="text-2xl font-bold text-gray-900">Gestion des Procès-Verbaux</h1>
      </div>

      <DataTable
        endpoint="pv"
        columns={columns}
        title="Liste des Procès-Verbaux"
        onAdd={handleAdd}
        onEdit={handleEdit}
        searchPlaceholder="Rechercher par numéro, objet..."
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={editingPV ? 'Modifier le PV' : 'Nouveau PV'}
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
                Type
              </label>
              <select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="reception">Réception</option>
                <option value="constat">Constat</option>
                <option value="reunion">Réunion</option>
                <option value="visite">Visite</option>
                <option value="expertise">Expertise</option>
                <option value="autre">Autre</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Date du PV
            </label>
            <input
              type="date"
              value={formData.date_pv}
              onChange={(e) => setFormData({ ...formData, date_pv: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
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

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Observations
            </label>
            <textarea
              value={formData.observations}
              onChange={(e) => setFormData({ ...formData, observations: e.target.value })}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Observations, remarques, décisions prises..."
            />
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
              {editingPV ? 'Mettre à jour' : 'Créer'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}