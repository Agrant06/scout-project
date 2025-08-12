import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  Grid,
  Chip,
  Divider,
  Box,
  Button,
} from '@mui/material';
import { format } from 'date-fns';
import axios from 'axios';

const DiagnosisDetail = () => {
  const { id } = useParams();
  const [diagnosis, setDiagnosis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadDiagnosis = async () => {
      try {
        const response = await axios.get(`http://localhost:5001/api/scout/diagnostics/${id}`);
        setDiagnosis(response.data);
      } catch (err) {
        setError('Error al cargar el diagnóstico');
        console.error('Error fetching diagnosis:', err);
      } finally {
        setLoading(false);
      }
    };
    
    loadDiagnosis();
  }, [id]); // Solo depende de id, que es un parámetro de useParams

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box m={2}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  if (!diagnosis) {
    return (
      <Box m={2}>
        <Alert severity="warning">Diagnóstico no encontrado</Alert>
      </Box>
    );
  }

  return (
    <Box m={3}>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            Detalles del Diagnóstico
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6">Información General</Typography>
              <Divider sx={{ my: 1 }} />
              
              <Typography variant="body1">
                <strong>ID del Negocio:</strong> {diagnosis.business_id}
              </Typography>
              
              <Typography variant="body1">
                <strong>Puntuación de Presencia Digital:</strong> 
                <Chip 
                  label={`${diagnosis.digital_presence_score}/100`} 
                  color={diagnosis.digital_presence_score > 70 ? 'success' : diagnosis.digital_presence_score > 40 ? 'warning' : 'error'}
                  size="small"
                  sx={{ ml: 1 }}
                />
              </Typography>
              
              <Typography variant="body1">
                <strong>Puntuación de Google Maps:</strong> 
                <Chip 
                  label={`${diagnosis.google_maps_score}/100`} 
                  color={diagnosis.google_maps_score > 70 ? 'success' : diagnosis.google_maps_score > 40 ? 'warning' : 'error'}
                  size="small"
                  sx={{ ml: 1 }}
                />
              </Typography>
              
              <Typography variant="body1">
                <strong>Puntuación del Sitio Web:</strong> 
                <Chip 
                  label={`${diagnosis.website_score}/100`} 
                  color={diagnosis.website_score > 70 ? 'success' : diagnosis.website_score > 40 ? 'warning' : 'error'}
                  size="small"
                  sx={{ ml: 1 }}
                />
              </Typography>
              
              <Typography variant="body1">
                <strong>Puntuación de Redes Sociales:</strong> 
                <Chip 
                  label={`${diagnosis.social_media_score}/100`} 
                  color={diagnosis.social_media_score > 70 ? 'success' : diagnosis.social_media_score > 40 ? 'warning' : 'error'}
                  size="small"
                  sx={{ ml: 1 }}
                />
              </Typography>
              
              <Typography variant="body1" sx={{ mt: 1 }}>
                <strong>Fecha de Creación:</strong> {format(new Date(diagnosis.created_at), 'dd/MM/yyyy HH:mm')}
              </Typography>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Typography variant="h6">Recomendaciones</Typography>
              <Divider sx={{ my: 1 }} />
              
              {diagnosis.recommendations ? (
                <Box>
                  {JSON.parse(diagnosis.recommendations).map((rec, index) => (
                    <Alert key={index} severity="info" sx={{ mb: 1 }}>
                      {rec}
                    </Alert>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No hay recomendaciones disponibles
                </Typography>
              )}
            </Grid>
          </Grid>
          
          <Box mt={3} display="flex" justifyContent="flex-end">
            <Button variant="outlined" onClick={() => window.history.back()}>
              Volver
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DiagnosisDetail;