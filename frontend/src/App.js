import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AppBar, Toolbar, Typography, Container, Box, Paper } from '@mui/material';
import axios from 'axios';
import DealershipsList from './DealershipsList';
import CreateDealership from './CreateDealership';

// Crear tema
const theme = createTheme();

function App() {
  const [backendStatus, setBackendStatus] = useState('Checking...');
  const [authStatus, setAuthStatus] = useState('Not tested');

  useEffect(() => {
    // Probar conexión con el backend
    axios.get('http://localhost:5001/')
      .then(response => {
        setBackendStatus('Connected');
        console.log('Backend response:', response.data);
      })
      .catch(error => {
        setBackendStatus('Error');
        console.error('Backend connection error:', error);
      });

    // Probar autenticación
    const testAuth = async () => {
      try {
        const response = await axios.post('http://localhost:5001/api/auth/login', {
          username: 'test',
          password: 'test'
        });
        setAuthStatus('Authenticated');
        console.log('Auth response:', response.data);
      } catch (error) {
        setAuthStatus('Failed');
        console.error('Auth error:', error);
      }
    };

    testAuth();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                Scout Project
              </Typography>
            </Toolbar>
          </AppBar>
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h4" gutterBottom>
                Scout Dashboard
              </Typography>
              
              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  System Status
                </Typography>
                <Paper elevation={1} sx={{ p: 2, mb: 2 }}>
                  <Typography variant="body1">
                    Backend Status: {backendStatus}
                  </Typography>
                </Paper>
                <Paper elevation={1} sx={{ p: 2 }}>
                  <Typography variant="body1">
                    Authentication Status: {authStatus}
                  </Typography>
                </Paper>
              </Box>
            </Paper>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;