import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './components/Login';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Marches from './pages/Marches';
import Prestataires from './pages/Prestataires';
import MaitreOuvrage from './pages/MaitreOuvrage';
import Services from './pages/Services';
import Maintenance from './pages/Maintenance';
import Fournitures from './pages/Fournitures';
import OrdreService from './pages/OrdreService';
import Decomptes from './pages/Decomptes';
import PV from './pages/PV';
import Documents from './pages/Documents';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Toaster position="top-right" />
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={
              <ProtectedRoute>
                <Layout>
                  <Dashboard />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/marches" element={
              <ProtectedRoute>
                <Layout>
                  <Marches />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/prestataires" element={
              <ProtectedRoute>
                <Layout>
                  <Prestataires />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/maitre-ouvrage" element={
              <ProtectedRoute>
                <Layout>
                  <MaitreOuvrage />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/services" element={
              <ProtectedRoute>
                <Layout>
                  <Services />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/maintenance" element={
              <ProtectedRoute>
                <Layout>
                  <Maintenance />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/fournitures" element={
              <ProtectedRoute>
                <Layout>
                  <Fournitures />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/ordre-service" element={
              <ProtectedRoute>
                <Layout>
                  <OrdreService />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/decomptes" element={
              <ProtectedRoute>
                <Layout>
                  <Decomptes />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/pv" element={
              <ProtectedRoute>
                <Layout>
                  <PV />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/documents" element={
              <ProtectedRoute>
                <Layout>
                  <Documents />
                </Layout>
              </ProtectedRoute>
            } />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;