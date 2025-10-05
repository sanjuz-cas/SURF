/**
 * SURF Modern Dashboard - Main Layout Component
 * ==============================================
 * Three-column layout: Sidebar | Feedback List | Detail View
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ModernDashboard.css';

interface FeedbackItem {
  id: number;
  rank: number;
  title: string;
  category: string;
  score: number;
  team: string;
  preMortemForecast: string;
  action_plan?: {
    immediate_steps: string[];
    medium_term_steps: string[];
    long_term_steps: string[];
  };
  raw_text?: string;
  created_at?: string;
  reporter?: string;
  date?: string;
  source?: string;
  impact?: string;
}

const ModernDashboard: React.FC = () => {
  const [items, setItems] = useState<FeedbackItem[]>([]);
  const [selectedItem, setSelectedItem] = useState<FeedbackItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeNav, setActiveNav] = useState('dashboard');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/priorities');
      setItems(response.data.items);
      if (response.data.items.length > 0) {
        setSelectedItem(response.data.items[0]);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryColor = (category: string) => {
    const colors: { [key: string]: string } = {
      'Bug Fix': '#dc3545',
      'Feature Request': '#5856d6',
      'UI/UX Improvement': '#9b59b6',
      'Performance': '#28a745',
      'General': '#6c757d'
    };
    return colors[category] || '#6c757d';
  };

  const getCategoryBadge = (category: string) => {
    return category || 'General';
  };

  const filteredItems = items.filter(item =>
    item.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <div className="modern-dashboard">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading feedback...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="modern-dashboard">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <h1>SURF</h1>
          <p className="tagline">Intelligently Prioritizing Customer Voices with AI</p>
        </div>
        
        <nav className="nav-menu">
          <button 
            className={`nav-item ${activeNav === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveNav('dashboard')}
          >
            <svg className="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
            Dashboard
          </button>
          
          <button 
            className={`nav-item ${activeNav === 'reports' ? 'active' : ''}`}
            onClick={() => setActiveNav('reports')}
          >
            <svg className="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            Reports
          </button>
          
          <button 
            className={`nav-item ${activeNav === 'settings' ? 'active' : ''}`}
            onClick={() => setActiveNav('settings')}
          >
            <svg className="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M12 1v6m0 6v6m6-6h6m-6 0H1m17-5.5l-3.5 3.5m-7 0L4 4m11 16l3.5-3.5m-11 0L4 20"></path>
            </svg>
            Settings
          </button>
        </nav>
      </aside>

      {/* Feedback List */}
      <div className="feedback-list">
        <div className="list-header">
          <h2>Feedback Items</h2>
          <div className="search-box">
            <svg className="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
            <input
              type="text"
              placeholder="Search by title..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        <div className="items-container">
          {filteredItems.map((item) => (
            <div
              key={item.id}
              className={`feedback-card ${selectedItem?.id === item.id ? 'selected' : ''}`}
              onClick={() => setSelectedItem(item)}
            >
              <div className="card-header">
                <span 
                  className="category-badge"
                  style={{ backgroundColor: getCategoryColor(item.category) }}
                >
                  {getCategoryBadge(item.category)}
                </span>
                <span className="score">Score: {Math.round(item.score)}</span>
              </div>
              <h3 className="card-title">{item.title}</h3>
              <button className="view-details">View Details</button>
            </div>
          ))}
        </div>

        <button className="download-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          Download CSV
        </button>
      </div>

      {/* Detail View */}
      <div className="detail-view">
        {selectedItem ? (
          <>
            <div className="detail-header">
              <h1 className="detail-title">{selectedItem.title}</h1>
            </div>

            <div className="detail-grid">
              <div className="detail-item">
                <label>CATEGORY</label>
                <span 
                  className="category-badge large"
                  style={{ backgroundColor: getCategoryColor(selectedItem.category) }}
                >
                  {getCategoryBadge(selectedItem.category)}
                </span>
              </div>

              <div className="detail-item">
                <label>SCORE</label>
                <div className="score-large">{Math.round(selectedItem.score)}</div>
              </div>

              <div className="detail-item">
                <label>ITEM ID</label>
                <div className="item-id">#{selectedItem.id}</div>
              </div>
            </div>

            <div className="detail-grid">
              <div className="detail-item">
                <label>REPORTER</label>
                <div className="reporter-info">
                  <div>Grace Hall</div>
                  <div className="reporter-meta">Guest • Free Tier</div>
                </div>
              </div>

              <div className="detail-item">
                <label>DATE & SOURCE</label>
                <div className="date-info">
                  <div>2024-07-22</div>
                  <div className="source-meta">Support Ticket</div>
                </div>
              </div>

              <div className="detail-item">
                <label>IMPACT</label>
                <div className="impact-value">50 Users</div>
              </div>
            </div>

            <div className="risk-assessment">
              <div className="risk-header">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
                RISK ASSESSMENT
              </div>
              <p className="risk-content">
                {selectedItem.preMortemForecast || 
                 'A critical issue blocking a segment of users. The main risk is not having access to a testing device, leading to a speculative fix that may not work.'}
              </p>
            </div>

            {selectedItem.action_plan && (
              <div className="action-plans">
                <h3>Action Plan</h3>
                
                {selectedItem.action_plan.immediate_steps && selectedItem.action_plan.immediate_steps.length > 0 && (
                  <div className="action-section">
                    <h4>Immediate Steps</h4>
                    <ul>
                      {selectedItem.action_plan.immediate_steps.map((step, idx) => (
                        <li key={idx}>{step}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {selectedItem.action_plan.medium_term_steps && selectedItem.action_plan.medium_term_steps.length > 0 && (
                  <div className="action-section">
                    <h4>Medium-Term Steps</h4>
                    <ul>
                      {selectedItem.action_plan.medium_term_steps.map((step, idx) => (
                        <li key={idx}>{step}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {selectedItem.action_plan.long_term_steps && selectedItem.action_plan.long_term_steps.length > 0 && (
                  <div className="action-section">
                    <h4>Long-Term Steps</h4>
                    <ul>
                      {selectedItem.action_plan.long_term_steps.map((step, idx) => (
                        <li key={idx}>{step}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </>
        ) : (
          <div className="no-selection">
            <p>Select a feedback item to view details</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ModernDashboard;
