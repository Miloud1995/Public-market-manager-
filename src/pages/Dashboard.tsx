import React, { useState, useEffect } from 'react';
import { 
  FileText, Users, Building, FolderOpen, 
  TrendingUp, AlertCircle, CheckCircle, Clock 
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';

interface Stats {
  totalMarches: number;
  totalPrestataires: number;
  totalMaitreOuvrage: number;
  totalDocuments: number;
  marchesEnCours: number;
  montantTotal: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats>({
    totalMarches: 0,
    totalPrestataires: 0,
    totalMaitreOuvrage: 0,
    totalDocuments: 0,
    marchesEnCours: 0,
    montantTotal: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('http://localhost:3001/api/dashboard/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const chartData = [
    { name: 'Jan', value: 45000 },
    { name: 'Fév', value: 52000 },
    { name: 'Mar', value: 48000 },
    { name: 'Avr', value: 61000 },
    { name: 'Mai', value: 55000 },
    { name: 'Jun', value: 67000 },
  ];

  const statCards = [
    {
      name: 'Total Marchés',
      value: stats.totalMarches,
      icon: FileText,
      color: 'bg-blue-500',
      change: '+12%',
      changeType: 'increase'
    },
    {
      name: 'Prestataires',
      value: stats.totalPrestataires,
      icon: Users,
      color: 'bg-green-500',
      change: '+8%',
      changeType: 'increase'
    },
    {
      name: 'Maîtres d\'Ouvrage',
      value: stats.totalMaitreOuvrage,
      icon: Building,
      color: 'bg-purple-500',
      change: '+5%',
      changeType: 'increase'
    },
    {
      name: 'Documents',
      value: stats.totalDocuments,
      icon: FolderOpen,
      color: 'bg-orange-500',
      change: '+15%',
      changeType: 'increase'
    }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Tableau de bord</h1>
        <div className="text-sm text-gray-500">
          Dernière mise à jour: {new Date().toLocaleDateString('fr-FR')}
        </div>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card) => (
          <div key={card.name} className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{card.name}</p>
                <p className="text-2xl font-bold text-gray-900">{card.value.toLocaleString()}</p>
              </div>
              <div className={`p-3 rounded-full ${card.color}`}>
                <card.icon className="w-6 h-6 text-white" />
              </div>
            </div>
            <div className="mt-4 flex items-center">
              <TrendingUp className="w-4 h-4 text-green-500" />
              <span className="text-sm text-green-600 ml-1">{card.change}</span>
              <span className="text-sm text-gray-500 ml-1">vs mois dernier</span>
            </div>
          </div>
        ))}
      </div>

      {/* Charts and additional info */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue chart */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Évolution des Montants</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip formatter={(value) => [`${value}€`, 'Montant']} />
              <Bar dataKey="value" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Recent activity */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Activités Récentes</h3>
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <CheckCircle className="w-5 h-5 text-green-500" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-900">Marché M2024001 validé</p>
                <p className="text-xs text-gray-500">Il y a 2 heures</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <AlertCircle className="w-5 h-5 text-orange-500" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-900">Document en attente de validation</p>
                <p className="text-xs text-gray-500">Il y a 4 heures</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <Clock className="w-5 h-5 text-blue-500" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-900">Nouveau prestataire ajouté</p>
                <p className="text-xs text-gray-500">Il y a 6 heures</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Summary section */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Résumé</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">{stats.marchesEnCours}</div>
            <div className="text-sm text-gray-600">Marchés en cours</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">
              {(stats.montantTotal || 0).toLocaleString()}€
            </div>
            <div className="text-sm text-gray-600">Montant total des marchés</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">
              {stats.montantTotal > 0 ? Math.round((stats.montantTotal / stats.totalMarches) || 0).toLocaleString() : 0}€
            </div>
            <div className="text-sm text-gray-600">Montant moyen par marché</div>
          </div>
        </div>
      </div>
    </div>
  );
}