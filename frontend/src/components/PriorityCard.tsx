/**
 * SURF Customer Feedback Dashboard - Priority Card Component
 * ==========================================================
 * Displays individual prioritized feedback items with financial risk warnings.
 */

import React from 'react';
import { PrioritizedItem } from '../types';
import './PriorityCard.css';

interface PriorityCardProps {
  item: PrioritizedItem;
}

/**
 * PriorityCard Component
 * Renders a detailed card for each prioritized feedback item.
 * The preMortemForecast is displayed in a visually striking warning box.
 */
const PriorityCard: React.FC<PriorityCardProps> = ({ item }) => {
  // Determine badge color based on score
  const getScoreBadgeClass = (score: number): string => {
    if (score >= 9.0) return 'score-badge critical';
    if (score >= 7.0) return 'score-badge high';
    if (score >= 5.0) return 'score-badge medium';
    return 'score-badge low';
  };

  // Determine category icon
  const getCategoryIcon = (category: string): string => {
    switch (category) {
      case 'Bug':
        return '🐛';
      case 'Feature':
        return '✨';
      case 'UX':
        return '🎨';
      default:
        return '📝';
    }
  };

  return (
    <div className="priority-card">
      {/* Header Section */}
      <div className="card-header">
        <div className="header-left">
          <span className="rank-badge">#{item.rank}</span>
          <h2 className="card-title">
            {getCategoryIcon(item.category)} {item.title}
          </h2>
        </div>
        <div className={getScoreBadgeClass(item.score)}>
          {item.score.toFixed(1)}
        </div>
      </div>

      {/* Metadata Section */}
      <div className="card-metadata">
        <div className="metadata-item">
          <span className="metadata-label">Category:</span>
          <span className="metadata-value category-badge">{item.category}</span>
        </div>
        <div className="metadata-item">
          <span className="metadata-label">Team:</span>
          <span className="metadata-value team-badge">{item.team}</span>
        </div>
      </div>

      {/* PRE-MORTEM FORECAST - VISUALLY STRIKING WARNING BOX */}
      <div className="pre-mortem-warning-box">
        <div className="warning-header">
          <span className="warning-icon">⚠️</span>
          <h3 className="warning-title">90-Day Financial Risk Assessment</h3>
        </div>
        <div className="warning-content">
          <p className="forecast-text">{item.preMortemForecast}</p>
        </div>
        <div className="warning-footer">
          <span className="warning-badge">CRITICAL BUSINESS IMPACT</span>
        </div>
      </div>

      {/* Action Plan Section */}
      <div className="action-plan-section">
        <h3 className="section-title">📋 Action Plan</h3>
        
        {/* Immediate Steps */}
        <div className="action-steps">
          <h4 className="steps-title">🚨 Immediate Steps:</h4>
          <ul className="steps-list">
            {item.action_plan.immediate_steps.map((step, idx) => (
              <li key={idx}>{step}</li>
            ))}
          </ul>
        </div>

        {/* Timeline and Resources */}
        <div className="action-plan-grid">
          <div className="action-item">
            <span className="action-label">Timeline:</span>
            <span className="action-value">{item.action_plan.estimated_timeline}</span>
          </div>
          <div className="action-item">
            <span className="action-label">Resources Needed:</span>
            <span className="action-value">{item.action_plan.required_resources}</span>
          </div>
        </div>
      </div>

      {/* Optional: Raw Feedback Preview */}
      {item.raw_text && (
        <div className="raw-feedback-section">
          <h4 className="section-subtitle">Original Feedback:</h4>
          <p className="raw-feedback-text">{item.raw_text}</p>
          {item.source && (
            <span className="feedback-source">Source: {item.source}</span>
          )}
        </div>
      )}
    </div>
  );
};

export default PriorityCard;
