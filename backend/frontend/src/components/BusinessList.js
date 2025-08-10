import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

function BusinessList({ user }) {
  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBusinesses();
  }, []);

  const fetchBusinesses = async () => {
    try {
      const response = await api.get('/businesses');
      setBusinesses(response.data.businesses || []);
    } catch (error) {
      console.error('Error fetching businesses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDiagnose = async (businessId) => {
    try {
      const response = await api.post(`/diagnosis/business/${businessId}`);
      
      if (response.status === 201) {
        alert('Diagnóstico creado exitosamente');
        // Recargar la lista para mostrar el diagnóstico
        fetchBusinesses();
      }
    } catch (error) {
      alert('Error al crear diagnóstico: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleBatchDiagnose = async () => {
    if (businesses.length === 0) {
      alert('No hay negocios para diagnosticar');
      return;
    }

    if (!confirm(`¿Estás seguro de que quieres diagnosticar todos los ${businesses.length} negocios?`)) {
      return;
    }

    try {
      const businessIds = businesses.map(b => b.id);
      const response = await api.post('/diagnosis/batch', { business_ids: businessIds });
      
      alert(`Diagnóstico completado. 
        Éxito: ${response.data.successful}
        Fallidos: ${response.data.failed}`);
      
      // Recargar la lista
      fetchBusinesses();
    } catch (error) {
      alert('Error al realizar diagnóstico por lotes: ' + (error.response?.data?.error || error.message));
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Cargando negocios...</p>
      </div>
    );
  }

  return (
    <div className="business-list-container">
      <div className="business-list-header">
        <h2>Tus Negocios</h2>
        <div className="business-list-actions">
          <button 
            className="btn" 
            onClick={handleBatchDiagnose}
            disabled={businesses.length === 0}
          >
            Diagnosticar Todos
          </button>
        </div>
      </div>

      {businesses.length > 0 ? (
        <div className="business-list">
          {businesses.map((business) => (
            <div key={business.id} className="business-card">
              <h3>{business.name}</h3>
              <p className="category">{business.category}</p>
              <p className="address">{business.address}, {business.city}</p>
              
              <div className="business-actions">
                <button 
                  className="diagnosis-btn"
                  onClick={() => handleDiagnose(business.id)}
                >
                  Diagnosticar
                </button>
                
                {business.latest_diagnosis && (
                  <Link 
                    to={`/diagnosis/${business.latest_diagnosis.id}`}
                    className="view-btn"
                  >
                    Ver Último Diagnóstico
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <p>No tienes negocios registrados.</p>
          <Link to="/dashboard" className="btn">
            Volver al Dashboard
          </Link>
        </div>
      )}
    </div>
  );
}

export default BusinessList;