import React, { useState, useEffect } from 'react';
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
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { format } from 'date-fns';
import { Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';
import axios from 'axios';

const BusinessList = () => {
  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedBusiness, setSelectedBusiness] = useState(null);

  useEffect(() => {
    const fetchBusinesses = async () => {
      try {
        const response = await axios.get('http://localhost:5001/api/scout/businesses');
        setBusinesses(response.data);
      } catch (err) {
        setError('Error al cargar los negocios');
        console.error('Error fetching businesses:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchBusinesses();
  }, []);

  const handleDeleteClick = (business) => {
    setSelectedBusiness(business);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    try {
      await axios.delete(`http://localhost:5001/api/scout/businesses/${selectedBusiness.id}`);
      setBusinesses(businesses.filter(b => b.id !== selectedBusiness.id));
      setDeleteDialogOpen(false);
      setSelectedBusiness(null);
    } catch (err) {
      console.error('Error deleting business:', err);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false);
    setSelectedBusiness(null);
  };

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

  return (
    <Box m={3}>
      <Typography variant="h4" gutterBottom>
        Lista de Negocios
      </Typography>
      
      <Grid container spacing={2}>
        {businesses.map((business) => (
          <Grid item xs={12} md={6} lg={4} key={business.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {business.name}
                </Typography>
                
                <Divider sx={{ my: 1 }} />
                
                <Typography variant="body2" color="text.secondary">
                  <strong>Dirección:</strong> {business.address}
                </Typography>
                
                {business.phone && (
                  <Typography variant="body2" color="text.secondary">
                    <strong>Teléfono:</strong> {business.phone}
                  </Typography>
                )}
                
                {business.website && (
                  <Typography variant="body2" color="text.secondary">
                    <strong>Website:</strong> {business.website}
                  </Typography>
                )}
                
                <Typography variant="body2" color="text.secondary">
                  <strong>Categoría:</strong> 
                  <Chip label={business.category} size="small" sx={{ ml: 1 }} />
                </Typography>
                
                {business.google_maps_rating && (
                  <Typography variant="body2" color="text.secondary">
                    <strong>Rating:</strong> {business.google_maps_rating}/5 ({business.google_maps_reviews} reviews)
                  </Typography>
                )}
                
                <Typography variant="body2" color="text.secondary">
                  <strong>Website:</strong> 
                  <Chip 
                    label={business.website_exists ? 'Existe' : 'No existe'} 
                    color={business.website_exists ? 'success' : 'error'}
                    size="small"
                    sx={{ ml: 1 }}
                  />
                </Typography>
                
                <Typography variant="body2" color="text.secondary">
                  <strong>Creado:</strong> {format(new Date(business.created_at), 'dd/MM/yyyy')}
                </Typography>
                
                <Box mt={2} display="flex" justifyContent="flex-end">
                  <IconButton size="small" color="primary">
                    <EditIcon />
                  </IconButton>
                  <IconButton 
                    size="small" 
                    color="error"
                    onClick={() => handleDeleteClick(business)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      <Dialog
        open={deleteDialogOpen}
        onClose={handleDeleteCancel}
      >
        <DialogTitle>Confirmar Eliminación</DialogTitle>
        <DialogContent>
          ¿Estás seguro de que deseas eliminar el negocio "{selectedBusiness?.name}"?
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteCancel}>Cancelar</Button>
          <Button onClick={handleDeleteConfirm} color="error" autoFocus>
            Eliminar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default BusinessList;