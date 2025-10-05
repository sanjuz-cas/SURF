/**
 * SURF Customer Feedback Dashboard - Main Dashboard Component
 * ===========================================================
 * Fetches and displays prioritized customer feedback items.
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PriorityCard from './PriorityCard';
import { PrioritizedItem, PrioritiesResponse, ApiError } from '../types';
import './PrioritizationDashboard.css';

/**
 * PrioritizationDashboard Component
 * Main component that fetches prioritized items from /api/priorities
 * and renders them using PriorityCard components.
 */
const PrioritizationDashboard: React.FC = () => {
  const [items, setItems] = useState<PrioritizedItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [totalAnalyzed, setTotalAnalyzed] = useState<number>(0);
  const [totalRiskEstimate, setTotalRiskEstimate] = useState<string>('');
  const [lastUpdated, setLastUpdated] = useState<string>('');

  /**
   * Fetch prioritized items from API on component mount
   */
  useEffect(() => {
    const fetchPriorities = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch data from API endpoint
        const response = await axios.get<PrioritiesResponse>('/api/priorities');

        // Update state with response data
        setItems(response.data.items);
        setTotalAnalyzed(response.data.total_analyzed);
        setTotalRiskEstimate(response.data.total_risk_estimate);
        setLastUpdated(response.data.generated_at);

        console.log('✅ Loaded prioritized items:', response.data.items.length);
      } catch (err) {
        console.error('❌ Error fetching priorities:', err);

        if (axios.isAxiosError(err)) {
          const apiError = err.response?.data as ApiError;
          setError(
            apiError?.message ||
            `Failed to load priorities: ${err.message}`
          );
        } else {
          setError('An unexpected error occurred while loading priorities.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchPriorities();
  }, []); // Empty dependency array = run once on mount

  /**
   * Render loading state
   */
  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p className="loading-text">Loading prioritized feedback...</p>
        </div>
      </div>
    );
  }

  /**
   * Render error state
   */
  if (error) {
    return (
      <div className="dashboard-container">
        <div className="error-container">
          <div className="error-icon">❌</div>
          <h2 className="error-title">Error Loading Priorities</h2>
          <p className="error-message">{error}</p>
          <button
            className="retry-button"
            onClick={() => window.location.reload()}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  /**
   * Render empty state
   */
  if (items.length === 0) {
    return (
      <div className="dashboard-container">
        <div className="empty-container">
          <div className="empty-icon">📭</div>
          <h2 className="empty-title">No Prioritized Feedback</h2>
          <p className="empty-message">
            There are currently no prioritized feedback items to display.
          </p>
        </div>
      </div>
    );
  }

  /**
   * Render main dashboard with prioritized items
   */
  return (
    <div className="dashboard-container">
      {/* Dashboard Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1 className="dashboard-title">
            🌊 SURF Customer Feedback Dashboard
          </h1>
          <p className="dashboard-subtitle">
            Strategic User Retention & Feedback - Priority Analysis
          </p>
        </div>

        {/* Summary Stats */}
        <div className="stats-container">
          <div className="stat-card">
            <div className="stat-label">Total Analyzed</div>
            <div className="stat-value">{totalAnalyzed}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Prioritized Items</div>
            <div className="stat-value">{items.length}</div>
          </div>
          <div className="stat-card risk-stat">
            <div className="stat-label">Total Risk Estimate</div>
            <div className="stat-value risk-value">{totalRiskEstimate}</div>
          </div>
        </div>

        {/* Last Updated */}
        {lastUpdated && (
          <div className="last-updated">
            Last updated: {new Date(lastUpdated).toLocaleString()}
          </div>
        )}
      </header>

      {/* Priority Items List */}
      <main className="dashboard-content">
        <div className="items-list">
          {items.map((item) => (
            <PriorityCard key={item.id} item={item} />
          ))}
        </div>
      </main>

      {/* Dashboard Footer */}
      <footer className="dashboard-footer">
        <p className="footer-text">
          Powered by SURF AI Agent Pipeline | CrewAI + Python + PostgreSQL
        </p>
      </footer>
    </div>
  );
};

export default PrioritizationDashboard;
