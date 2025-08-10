import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Chart } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, LineElement, Title, Tooltip, Legend, ArcElement);

function DiagnosisDetail({ user }) {
  const [diagnosis, setDiagnosis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const { id } = useParams();

  useEffect(() => {
    fetchDiagnosis();
  }, [id]);

  const fetchDiagnosis = async () => {
    try {
      const response = await api.get(`/diagnosis/${id}`);
      setDiagnosis(response.data);
    } catch (error) {
      console.error('Error fetching diagnosis:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreData = () => {
    if (!diagnosis) return {};
    
    return {
      labels: ['Google Maps', 'Sitio Web', 'General'],
      datasets: [
        {
          label: 'Puntuación',
          data: [
            diagnosis.google_maps_score,
            diagnosis.website_score,
            diagnosis.overall_score
          ],
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(75, 192, 192, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(75, 192, 192, 1)'
          ],
          borderWidth: 1,
        },
      ],
    };
  };

  const getRecommendationsByPriority = () => {
    if (!diagnosis || !diagnosis.recommendations) return {};
    
    const priorities = { high: [], medium: [], low: [] };
    
    diagnosis.recommendations.forEach(rec => {
      priorities[rec.priority].push(rec);
    });

    return priorities;
  };

  const getInconsistencies = () => {
    if (!diagnosis || !diagnosis.inconsistencies) return [];
    
    return diagnosis.inconsistencies.filter(inc => inc.severity === 'high');
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Cargando diagnóstico...</p>
      </div>
    );
  }

  if (!diagnosis) {
    return (
      <div className="error-container">
        <h2>No se encontró el diagnóstico</h2>
        <Link to="/businesses" className="btn">
          Volver a Negocios
        </Link>
      </div>
    );
  }

  const scoreData = getScoreData();
  const recommendationsByPriority = getRecommendationsByPriority();
  const criticalInconsistencies = getInconsistencies();

  return (
    <div className="diagnosis-detail">
      <div className="diagnosis-header">
        <div className="diagnosis-info">
          <h2>Diagnóstico de {diagnosis.business?.name}</h2>
          <p className="business-info">
            {diagnosis.business?.category} • {diagnosis.business?.address}
          </p>
          <p className="diagnosis-date">
            Realizado el: {new Date(diagnosis.created_at).toLocaleDateString()}
          </p>
        </div>
        
        <div className="diagnosis-summary">
          <div className="score-summary">
            <h3>Puntuación General</h3>
            <div className="score-circle">
              <div className="score-value">{diagnosis.overall_score}</div>
              <div className="score-max">/100</div>
            </div>
          </div>
          
          <div className="score-breakdown">
            <h3>Desglose</h3>
            <div className="score-items">
              <div className="score-item">
                <span>Google Maps</span>
                <span>{diagnosis.google_maps_score}/100</span>
              </div>
              <div className="score-item">
                <span>Sitio Web</span>
                <span>{diagnosis.website_score}/100</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="diagnosis-tabs">
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Resumen
          </button>
          <button 
            className={`tab ${activeTab === 'recommendations' ? 'active' : ''}`}
            onClick={() => setActiveTab('recommendations')}
          >
            Recomendaciones
          </button>
          <button 
            className={`tab ${activeTab === 'charts' ? 'active' : ''}`}
            onClick={() => setActiveTab('charts')}
          >
            Gráficos
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'overview' && (
            <div className="overview-tab">
              <div className="score-chart">
                <h3>Puntuación General</h3>
                <div className="chart-container">
                  <Chart type="doughnut" data={scoreData} options={{
                    responsive: true,
                    plugins: {
                      legend: {
                        position: 'bottom',
                      },
                    },
                  }} />
                </div>
              </div>

              {criticalInconsistencies.length > 0 && (
                <div className="critical-issues">
                  <h3>Problemas Críticos</h3>
                  <div className="issues-list">
                    {criticalInconsistencies.map((issue, index) => (
                      <div key={index} className="issue-item">
                        <span className="issue-type">{issue.type}</span>
                        <span className="issue-description">{issue.description}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'recommendations' && (
            <div className="recommendations-tab">
              <div className="recommendations-container">
                {Object.entries(recommendationsByPriority).map(([priority, recs]) => (
                  recs.length > 0 && (
                    <div key={priority} className="priority-section">
                      <h3 className={`priority-${priority}`}>
                        {priority === 'high' ? 'Alta Prioridad' : 
                         priority === 'medium' ? 'Prioridad Media' : 
                         'Baja Prioridad'}
                      </h3>
                      <div className="recommendations-list">
                        {recs.map((rec, index) => (
                          <div key={index} className="recommendation-card">
                            <h4>{rec.title}</h4>
                            <p>{rec.description}</p>
                            <div className="recommendation-meta">
                              <span className="difficulty">Dificultad: {rec.difficulty}</span>
                              <span className="time">Tiempo: {rec.estimated_time}</span>
                            </div>
                            <div className="recommendation-status">
                              Estado: 
                              <span className={`status-${rec.status}`}>
                                {rec.status === 'completed' ? 'Completado' :
                                 rec.status === 'in_progress' ? 'En Progreso' :
                                 rec.status === 'pending' ? 'Pendiente' : 'Descartado'}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )
                ))}
              </div>
            </div>
          )}

          {activeTab === 'charts' && (
            <div className="charts-tab">
              <div className="charts-grid">
                <div className="chart-card">
                  <h3>Puntuación por Categoría</h3>
                  <div className="chart-container">
                    <Chart type="bar" data={scoreData} options={{
                      responsive: true,
                      scales: {
                        y: {
                          beginAtZero: true,
                          max: 100
                        }
                      },
                      plugins: {
                        legend: {
                          position: 'bottom',
                        },
                      },
                    }} />
                  </div>
                </div>

                <div className="chart-card">
                  <h3>Distribución de Recomendaciones</h3>
                  <div className="chart-container">
                    <Chart type="pie" data={{
                      labels: ['Alta Prioridad', 'Media Prioridad', 'Baja Prioridad'],
                      datasets: [{
                        data: [
                          recommendationsByPriority.high?.length || 0,
                          recommendationsByPriority.medium?.length || 0,
                          recommendationsByPriority.low?.length || 0
                        ],
                        backgroundColor: [
                          'rgba(255, 99, 132, 0.8)',
                          'rgba(54, 162, 235, 0.8)',
                          'rgba(75, 192, 192, 0.8)'
                        ],
                        borderColor: [
                          'rgba(255, 99, 132, 1)',
                          'rgba(54, 162, 235, 1)',
                          'rgba(75, 192, 192, 1)'
                        ],
                        borderWidth: 1,
                      }],
                    }]} options={{
                      responsive: true,
                      plugins: {
                        legend: {
                          position: 'bottom',
                        },
                      },
                    }} />
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="diagnosis-actions">
        <Link to={`/businesses`} className="btn">
          Volver a Negocios
        </Link>
        <button 
          className="btn" 
          onClick={() => {
            if (confirm('¿Quieres crear un nuevo diagnóstico? Se reemplazará el actual.'))
              window.location.reload();
          }}
        >
          Nuevo Diagnóstico
        </button>
      </div>
    </div>
  );
}

export default DiagnosisDetail;