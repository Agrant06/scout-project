import React from 'react';
import './App.css';

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-brand">
          <h1>Scout</h1>
          <span className="nav-subtitle">Análisis Digital de Negocios</span>
        </div>
        <div className="nav-links">
          <a href="#/login">Iniciar Sesión</a>
        </div>
      </nav>

      <main className="main-content">
        <h2>Bienvenido a Scout</h2>
        <p>Plataforma para analizar y mejorar la presencia digital de negocios</p>
        <p>El frontend está funcionando correctamente.</p>
      </main>
    </div>
  );
}

export default App;