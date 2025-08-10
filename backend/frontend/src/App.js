import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import BusinessList from './components/BusinessList';
import DiagnosisDetail from './components/DiagnosisDetail';
import Login from './components/Login';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Verificar si hay un token en localStorage
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
      // Aquí podrías validar el token con el backend
      setUser({ id: 'user-id', email: 'user@example.com' });
    }
  }, []);

  const handleLogin = (userData, token) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-brand">
            <h1>Scout</h1>
            <span className="nav-subtitle">Análisis Digital de Negocios</span>
          </div>
          
          <div className="nav-links">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/businesses">Negocios</Link>
                <button onClick={handleLogout} className="logout-btn">
                  Cerrar Sesión
                </button>
              </>
            ) : (
              <Link to="/login">Iniciar Sesión</Link>
            )}
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route 
              path="/login" 
              element={<Login onLogin={handleLogin} />} 
            />
            <Route 
              path="/dashboard" 
              element={isAuthenticated ? <Dashboard user={user} /> : <Login onLogin={handleLogin} />} 
            />
            <Route 
              path="/businesses" 
              element={isAuthenticated ? <BusinessList user={user} /> : <Login onLogin={handleLogin} />} 
            />
            <Route 
              path="/diagnosis/:id" 
              element={isAuthenticated ? <DiagnosisDetail user={user} /> : <Login onLogin={handleLogin} />} 
            />
            <Route 
              path="/" 
              element={isAuthenticated ? <Dashboard user={user} /> : <Login onLogin={handleLogin} />} 
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;