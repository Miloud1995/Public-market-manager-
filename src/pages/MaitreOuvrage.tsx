import React, { useState } from 'react';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import axios from 'axios';
import toast from 'react-hot-toast';

interface MaitreOuvrage {
  id?: number;
  nom: string;
  adresse: string;
  telephone: string;
  email: string;
  responsable: string;
}

export default function MaitreOuvrage() {
  const [showModal, setShowModal] = useState(false);
  const [editingMaitreOuvrage, setEditingMaitreOuvrage] = useState<MaitreOuvrage | null>(null);
  const [formData, setFormData] = useState<MaitreOuvrage>({
    nom: '',
    adresse: '',
    telephone: '',
    email: '',
    responsable: ''
  });

  const columns = [
    { key: 'nom', label: 'Nom' },
    { key: 'responsable', label: 'Responsable' },
    { key: 'telephone', label: 'Téléphone' },
    { key: 'email', label: 'Email' }
  ];

  const handleAdd = () => {
    setEditingMaitreOuvrage(null);
    setFormData({
      nom: '',
      adresse: '',
      telephone: '',
      email: '',
      responsable: ''
    });
    setShowModal(true);
  };

  const handleEdit = (maitreOuvrage: MaitreOuvrage) => {
    setEditingMaitreOuvrage(maitreOuvrage);
    setFormData(maitreOuvrage);
    setShowModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingMaitreOuvrage) {
        await axios.put(`http://localhost:3001/api/maitre_ouvrage/${editingMaitreOuvrage.id}`, formData);
        toast.success('Maître d\'ouvrage mis à jour avec succès');
      } else {
        await axios.post('http://localhost:3001/api/maitre_ouvrage', formData);
        toast.success('Maître d\'ouvrage créé avec succès');
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
        <h1 className="text-2xl font-bold text-gray-900">Gestion des Maîtres d'Ouvrage</h1>
      </div>

      <DataTable
        endpoint="maitre_ouvrage"
        columns={columns}
        title="Liste des Maîtres d'Ouvrage"
        onAdd={handleAdd}
        onEdit={handleEdit}
        searchPlaceholder="Rechercher par nom, responsable..."
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={editingMaitreOuvrage ? 'Modifier le Maître d\'Ouvrage' : 'Nouveau Maître d\'Ouvrage'}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nom de l'organisation *
              </label>
              <input
                type="text"
                value={formData.nom}
                onChange={(e) => setFormData({ ...formData, nom: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Responsable
              </label>
              <input
                type="text"
                value={formData.responsable}
                onChange={(e) => setFormData({ ...formData, responsable: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Adresse
            </label>
            <textarea
              value={formData.adresse}
              onChange={(e) => setFormData({ ...formData, adresse: e.target.value })}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Téléphone
              </label>
              <input
                type="tel"
                value={formData.telephone}
                onChange={(e) => setFormData({ ...formData, telephone: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
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
              {editingMaitreOuvrage ? 'Mettre à jour' : 'Créer'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}