import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Auth from './pages/Auth';
import ResumeAnalyzer from './pages/ResumeAnalyzer';
import Interview from './pages/Interview';
import Admin from './pages/Admin';
import './index.css';

import { useState, useEffect } from 'react';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    window.location.href = '/';
  };

  return (
    <Router>
      <div className="app-container">
        <nav className="glass-panel" style={{ padding: '1rem 2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', margin: '1rem' }}>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }} className="gradient-text">
            AI Interviewer
          </div>
          <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
            <Link to="/" style={{ color: 'var(--text-primary)', textDecoration: 'none' }}>Home</Link>
            {isAuthenticated && (
              <Link to="/resume-analyzer" style={{ color: 'var(--text-primary)', textDecoration: 'none' }}>Resume Analyzer</Link>
            )}
            {isAuthenticated ? (
              <button onClick={handleLogout} className="btn-primary" style={{ textDecoration: 'none', padding: '0.5rem 1rem' }}>Logout</button>
            ) : (
              <div style={{ display: 'flex', gap: '1rem' }}>
                <Link to="/login" className="btn-primary" style={{ textDecoration: 'none', padding: '0.5rem 1rem', background: 'transparent', border: '1px solid var(--primary-color)' }}>Login</Link>
                <Link to="/register" className="btn-primary" style={{ textDecoration: 'none', padding: '0.5rem 1rem' }}>Register</Link>
              </div>
            )}
          </div>
        </nav>

        <main style={{ padding: '2rem' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Auth type="login" setIsAuthenticated={setIsAuthenticated} />} />
            <Route path="/register" element={<Auth type="register" setIsAuthenticated={setIsAuthenticated} />} />
            <Route path="/resume-analyzer" element={<ResumeAnalyzer />} />
            <Route path="/interview" element={<Interview />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
