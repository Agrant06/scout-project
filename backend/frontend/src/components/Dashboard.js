import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

function Dashboard({ user }) {
  const [stats, setStats] = useState({
    totalBusinesses: 0,
    totalDiagnoses: 0,
    avgScore: 0,
    recentDiagnoses: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Obtener lista de negocios del usuario
      const businessesResponse = await api.get('/businesses');
      const businesses = businessesResponse.data.businesses || [];
      
      // Obtener diagnósticos recientes
      const diagnosesResponse = await api.get('/diagnosis/recent');
      const diagnoses = diagnosesResponse.data.diagnoses || [];
      
      // Calcular estadísticas
      const totalBusinesses = businesses.length;
      const totalDiagnoses = diagnoses.length;
      const avgScore = totalDiagnoses > 0 
        ? Math.round(diagnoses.reduce((sum, d) => sum + d.overall_score, 0) / totalDiagnoses)
        : 0;

      setStats({
        totalBusinesses,
        totalDiagnoses,
        avgScore,
        recentDiagnoses: diagnoses.slice(0, 5)
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Cargando dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Bienvenido, {user?.email}</h2>
        <p>Panel de control de análisis digital de negocios</p>
      </div>

      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>Total Negocios</h3>
          <div className="value">{stats.totalBusinesses}</div>
        </div>

        <div className="stat-card">
          <h3>Diagnósticos Realizados</h3>
          <div className="value">{stats.totalDiagnoses}</div>
        </div>

        <div className="stat-card">
          <h3>Puntuación Promedio</h3>
          <div className="value">{stats.avgScore}/100</div>
        </div>

        <div className="stat-card">
          <h3>Acciones Rápidas</h3>
          <div className="actions">
            <Link to="/businesses" className="btn btn-full">
              Ver Negocios
            </Link>
          </div>
        </div>
      </div>

      <div className="recent-diagnoses">
        <h3>Diagnósticos Recientes</h3>
        
        {stats.recentDiagnoses.length > 0 ? (
          <div className="business-list">
            {stats.recentDiagnoses.map((diagnosis) => (
              <div key={diagnosis.id} className="business-card">
                <h3>{diagnosis.business?.name || 'Negocio sin nombre'}</h3>
                <p>{diagnosis.business?.category || 'Sin categoría'}</p>
                <div className="score">
                  <div className="score-item">
                    <span className="label">General</span>
                    <span className="value">{diagnosis.overall_score}/100</span>
                  </div>
                  <div className="score-item">
                    <span className="label">Google Maps</span>
                    <span className="value">{diagnosis.google_maps_score}/100</span>
                  </div>
                  <div className="score-item">
                    <span className="label">Sitio Web</span>
                    <span className="value">{diagnosis.website_score}/100</span>
                  </div>
                </div>
                <Link 
                  to={`/diagnosis/${diagnosis.id}`} 
                  className="diagnosis-btn"
                >
                  Ver Detalles
                </Link>
              </div>
            ))}
          </div>
        ) : (
          <p>No hay diagnósticos recientes. 
            <Link to="/businesses">Analiza tu primer negocio</Link>
          </p>
        )}
      </div>
    </div>
  );
}

export default Dashboard;