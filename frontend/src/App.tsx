/**
 * SURF Customer Feedback Dashboard - Main App Component
 * =====================================================
 * Root component for the React application.
 */

import React from 'react';
import ModernDashboard from './components/ModernDashboard';
import './App.css';

/**
 * App Component
 * Main entry point for the SURF Dashboard application
 */
const App: React.FC = () => {
  return (
    <div className="app">
      <ModernDashboard />
    </div>
  );
};

export default App;
