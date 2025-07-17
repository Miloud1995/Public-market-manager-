import React, { useState } from 'react';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import { Upload, Download, FileText } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

interface Document {
  id?: number;
  nom: string;
  type: string;
  chemin: string;
  taille: number;
  marche_id: number;
}

export default function Documents() {
  const [showModal, setShowModal] = useState(false);
  const [editingDocument, setEditingDocument] = useState<Document | null>(null);
  const [formData, setFormData] = useState<Document>({
    nom: '',
    type: '',
    chemin: '',
    taille: 0,
    marche_id: 1
  });
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const columns = [
    { 
      key: 'nom', 
      label: 'Nom',
      render: (value: string, row: Document) => (
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-gray-400" />
          <span>{value}</span>
        </div>
      )
    },
    { key: 'type', label: 'Type' },
    { 
      key: 'taille', 
      label: 'Taille',
      render: (value: number) => {
        if (value < 1024) return `${value} B`;
        if (value < 1024 * 1024) return `${(value / 1024).toFixed(1)} KB`;
        return `${(value / (1024 * 1024)).toFixed(1)} MB`;
      }
    },
    { 
      key: 'created_at', 
      label: 'Date d\'ajout',
      render: (value: string) => value ? new Date(value).toLocaleDateString('fr-FR') : '-'
    }
  ];

  const handleAdd = () => {
    setEditingDocument(null);
    setFormData({
      nom: '',
      type: '',
      chemin: '',
      taille: 0,
      marche_id: 1
    });
    setSelectedFile(null);
    setShowModal(true);
  };

  const handleEdit = (document: Document) => {
    setEditingDocument(document);
    setFormData(document);
    setSelectedFile(null);
    setShowModal(true);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setFormData({
        ...formData,
        nom: file.name,
        type: file.type || 'application/octet-stream',
        taille: file.size
      });
    }
  };

  const uploadFile = async () => {
    if (!selectedFile) return null;

    const uploadFormData = new FormData();
    uploadFormData.append('file', selectedFile);

    try {
      setUploading(true);
      const response = await axios.post('http://localhost:3001/api/upload', uploadFormData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data.path;
    } catch (error) {
      toast.error('Erreur lors du téléchargement du fichier');
      return null;
    } finally {
      setUploading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    let chemin = formData.chemin;
    
    if (selectedFile) {
      chemin = await uploadFile();
      if (!chemin) return;
    }

    const documentData = { ...formData, chemin };

    try {
      if (editingDocument) {
        await axios.put(`http://localhost:3001/api/document/${editingDocument.id}`, documentData);
        toast.success('Document mis à jour avec succès');
      } else {
        await axios.post('http://localhost:3001/api/document', documentData);
        toast.success('Document créé avec succès');
      }
      setShowModal(false);
      window.location.reload();
    } catch (error) {
      toast.error('Erreur lors de la sauvegarde');
    }
  };

  const handleDownload = (document: Document) => {
    if (document.chemin) {
      window.open(`http://localhost:3001${document.chemin}`, '_blank');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Gestion des Documents</h1>
      </div>

      <DataTable
        endpoint="document"
        columns={[
          ...columns,
          {
            key: 'actions',
            label: 'Actions',
            render: (value: any, row: Document) => (
              <button
                onClick={() => handleDownload(row)}
                className="text-blue-600 hover:text-blue-900 p-1 rounded hover:bg-blue-50 transition-colors"
                title="Télécharger"
              >
                <Download className="w-4 h-4" />
              </button>
            )
          }
        ]}
        title="Liste des Documents"
        onAdd={handleAdd}
        onEdit={handleEdit}
        searchPlaceholder="Rechercher par nom, type..."
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={editingDocument ? 'Modifier le Document' : 'Nouveau Document'}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Fichier {!editingDocument && '*'}
            </label>
            <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-gray-400 transition-colors">
              <div className="space-y-1 text-center">
                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                <div className="flex text-sm text-gray-600">
                  <label className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                    <span>Télécharger un fichier</span>
                    <input
                      type="file"
                      className="sr-only"
                      onChange={handleFileChange}
                      accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png"
                    />
                  </label>
                  <p className="pl-1">ou glisser-déposer</p>
                </div>
                <p className="text-xs text-gray-500">
                  PDF, DOC, XLS, JPG jusqu'à 10MB
                </p>
                {selectedFile && (
                  <p className="text-sm text-green-600 font-medium">
                    Fichier sélectionné: {selectedFile.name}
                  </p>
                )}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nom du document
              </label>
              <input
                type="text"
                value={formData.nom}
                onChange={(e) => setFormData({ ...formData, nom: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Nom affiché du document"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type de document
              </label>
              <select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Sélectionner...</option>
                <option value="Contrat">Contrat</option>
                <option value="Facture">Facture</option>
                <option value="Devis">Devis</option>
                <option value="Plan">Plan</option>
                <option value="Rapport">Rapport</option>
                <option value="Photo">Photo</option>
                <option value="Autre">Autre</option>
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
              disabled={uploading || (!editingDocument && !selectedFile)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {uploading && <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />}
              {editingDocument ? 'Mettre à jour' : 'Créer'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}