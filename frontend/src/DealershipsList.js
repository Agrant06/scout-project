import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
  CircularProgress,
  Alert
} from '@mui/material';
import axios from 'axios';

function DealershipsList() {
  const [dealerships, setDealerships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDealerships = async () => {
      try {
        console.log('Intentando obtener concesionarios...');
        const response = await axios.get('http://localhost:5001/api/directories/dealerships');
        console.log('Respuesta de la API:', response.data);
        setDealerships(response.data.dealerships || []);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching dealerships:', err);
        setError('Error al cargar los concesionarios');
        setLoading(false);
      }
    };

    fetchDealerships();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">{error}</Alert>
    );
  }

  console.log('Concesionarios a mostrar:', dealerships);

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Lista de Concesionarios
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Nombre</TableCell>
              <TableCell>Dirección</TableCell>
              <TableCell>Teléfono</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Categoría</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {dealerships.length > 0 ? (
              dealerships.map((dealership) => (
                <TableRow key={dealership.id}>
                  <TableCell>{dealership.id}</TableCell>
                  <TableCell>{dealership.name}</TableCell>
                  <TableCell>{dealership.address}</TableCell>
                  <TableCell>{dealership.phone || 'N/A'}</TableCell>
                  <TableCell>{dealership.email || 'N/A'}</TableCell>
                  <TableCell>{dealership.category}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  No hay concesionarios disponibles
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default DealershipsList;