import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  Alert,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

function CreateDealership() {
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    phone: '',
    email: '',
    category: 'autos'
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const response = await axios.post('http://localhost:5001/api/directories/dealerships', formData);
      console.log('Dealership created:', response.data);
      setSuccess(true);
      setFormData({
        name: '',
        address: '',
        phone: '',
        email: '',
        category: 'autos'
      });
    } catch (err) {
      setError('Error al crear el concesionario');
      console.error('Error creating dealership:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Crear Nuevo Concesionario
      </Typography>
      <Paper elevation={3} sx={{ p: 3 }}>
        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Concesionario creado exitosamente!
          </Alert>
        )}
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField
            fullWidth
            label="Nombre"
            name="name"
            value={formData.name}
            onChange={handleChange}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Dirección"
            name="address"
            value={formData.address}
            onChange={handleChange}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Teléfono"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            margin="normal"
            type="email"
          />
          <TextField
            fullWidth
            label="Categoría"
            name="category"
            value={formData.category}
            onChange={handleChange}
            margin="normal"
            select
            SelectProps={{ native: true }}
          >
            <option value="autos">Autos</option>
            <option value="motos">Motos</option>
            <option value="restaurant">Restaurant</option>
          </TextField>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Crear Concesionario'}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}

export default CreateDealership;