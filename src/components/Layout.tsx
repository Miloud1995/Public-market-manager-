import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  Building2, LayoutDashboard, FileText, Users, Settings, 
  LogOut, Menu, X, Package, Wrench, ShoppingCart, 
  ClipboardList, Calculator, FileCheck, FolderOpen,
  User
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface LayoutProps {
  children: React.ReactNode;
}

const navigation = [
  { name: 'Tableau de bord', href: '/', icon: LayoutDashboard },
  { name: 'Marchés', href: '/marches', icon: FileText },
  { name: 'Prestataires', href: '/prestataires', icon: Users },
  { name: 'Maître d\'Ouvrage', href: '/maitre-ouvrage', icon: User },
  { name: 'Services', href: '/services', icon: Package },
  { name: 'Maintenance', href: '/maintenance', icon: Wrench },
  { name: 'Fournitures', href: '/fournitures', icon: ShoppingCart },
  { name: 'Ordre de Service', href: '/ordre-service', icon: ClipboardList },
  { name: 'Décomptes', href: '/decomptes', icon: Calculator },
  { name: 'PV', href: '/pv', icon: FileCheck },
  { name: 'Documents', href: '/documents', icon: FolderOpen },
];

export default function Layout({ children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        </div>
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-xl transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200">
          <div className="flex items-center">
            <Building2 className="w-8 h-8 text-blue-600" />
            <span className="ml-2 text-lg font-semibold text-gray-900">GMP</span>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden"
          >
            <X className="w-6 h-6 text-gray-400" />
          </button>
        </div>

        <nav className="flex-1 px-4 py-6 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                    : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                }`}
                onClick={() => setSidebarOpen(false)}
              >
                <item.icon className={`w-5 h-5 mr-3 ${isActive ? 'text-blue-700' : 'text-gray-400'}`} />
                {item.name}
              </Link>
            );
          })}
        </nav>

        <div className="px-4 py-4 border-t border-gray-200">
          <div className="flex items-center px-3 py-2">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                {user?.username.charAt(0).toUpperCase()}
              </div>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-900">{user?.username}</p>
              <p className="text-xs text-gray-500">{user?.role}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="w-full flex items-center px-3 py-2 text-sm font-medium text-gray-700 rounded-lg hover:bg-gray-50 hover:text-gray-900 transition-colors mt-2"
          >
            <LogOut className="w-5 h-5 mr-3 text-gray-400" />
            Déconnexion
          </button>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <div className="sticky top-0 z-10 bg-white shadow-sm border-b border-gray-200">
          <div className="flex items-center justify-between h-16 px-6">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden"
            >
              <Menu className="w-6 h-6 text-gray-400" />
            </button>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                Bienvenue, {user?.username}
              </span>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  );
}