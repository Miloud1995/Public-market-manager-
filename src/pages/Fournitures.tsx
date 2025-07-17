import React, { useState } from 'react';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import axios from 'axios';
import toast from 'react-hot-toast';

interface Fourniture {
  id?: number;
  libelle: string;
  description: string;
  prix_unitaire: number;
  unite: string;
  marque: string;
  marche_id: number;
}

export default function Fournitures() {
  const [showModal, setShowModal] = useState(false);
  const [editingFourniture, setEditingFourniture] = useState<Fourniture | null>(null);
  const [formData, setFormData] = useState<Fourniture>({
    libelle: '',
    description: '',
    prix_unitaire: 0,
    unite: '',
    marque: '',
    marche_id: 1
  });

  const columns = [
    { key: 'libelle', label: 'Libellé' },
    { key: 'marque', label: 'Marque' },
    { 
      key: 'prix_unitaire', 
      label: 'Prix Unitaire',
      render: (value: number) => `${value.toLocaleString()} €`
    },
    { key: 'unite', label: 'Unité' }
  ];

  const handleAdd = () => {
    setEditingFourniture(null);
    setFormData({
      libelle: '',
      description: '',
      prix_unitaire: 0,
      unite: '',
      marque: '',
      marche_id: 1
    });
    setShowModal(true);
  };

  const handleEdit = (fourniture: Fourniture) => {
    setEditingFourniture(fourniture);
    setFormData(fourniture);
    setShowModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingFourniture) {
        await axios.put(`http://localhost:3001/api/fourniture/${editingFourniture.id}`, formData);
        toast.success('Fourniture mise à jour avec succès');
      } else {
        await axios.post('http://localhost:3001/api/fourniture', formData);
        toast.success('Fourniture créée avec succès');
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
        <h1 className="text-2xl font-bold text-gray-900">Gestion des Fournitures</h1>
      </div>

      <DataTable
        endpoint="fourniture"
        columns={columns}
        title="Liste des Fournitures"
        onAdd={handleAdd}
        onEdit={handleEdit}
        searchPlaceholder="Rechercher par libellé, marque..."
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={editingFourniture ? 'Modifier la Fourniture' : 'Nouvelle Fourniture'}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                Marque
              </label>
              <input
                type="text"
                value={formData.marque}
                onChange={(e) => setFormData({ ...formData, marque: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
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
                Unité
              </label>
              <select
                value={formData.unite}
                onChange={(e) => setFormData({ ...formData, unite: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Sélectionner...</option>
                <option value="Pièce">Pièce</option>
                <option value="Kg">Kilogramme</option>
                <option value="M">Mètre</option>
                <option value="M²">Mètre carré</option>
                <option value="M³">Mètre cube</option>
                <option value="Litre">Litre</option>
                <option value="Tonne">Tonne</option>
                <option value="Palette">Palette</option>
                <option value="Lot">Lot</option>
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
              {editingFourniture ? 'Mettre à jour' : 'Créer'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}