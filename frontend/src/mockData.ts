/**
 * SURF Customer Feedback Dashboard - Mock Data
 * =============================================
 * Temporary mock data for frontend development.
 * This file will be replaced with actual API integration.
 */

import { PrioritiesResponse } from './types';

/**
 * Mock prioritized feedback items
 * These represent the output of the SURF AI Agent Pipeline
 */
export const mockPrioritiesData: PrioritiesResponse = {
  items: [
    {
      id: 1,
      rank: 1,
      title: "Payment Processing Failures During Checkout",
      score: 95.2,
      category: "Transaction Reliability",
      team: "Payment Engineering",
      preMortemForecast: "Financial Risk: If payment failures persist for 30 more days, we project losing $487K in revenue (12% of monthly recurring revenue) and 340+ enterprise customers churning to competitors with more reliable payment systems. Historical data shows 68% of users who experience payment failures never retry.",
      action_plan: {
        immediate_steps: [
          "Roll back to previous payment gateway version (proven stable)",
          "Enable fallback payment processor for failed transactions",
          "Deploy hot-fix to handle timeout errors gracefully",
          "Send apology email to affected customers with discount code"
        ],
        medium_term_steps: [
          "Conduct root cause analysis with payment vendor",
          "Implement circuit breaker pattern for payment service",
          "Add comprehensive payment error monitoring",
          "Build automated payment retry logic with exponential backoff"
        ],
        long_term_steps: [
          "Migrate to multi-vendor payment redundancy architecture",
          "Establish payment SLA with 99.99% uptime requirement",
          "Create dedicated payment reliability team",
          "Implement real-time payment health dashboard"
        ],
        estimated_timeline: "Immediate: 24-48 hours | Medium: 2-3 weeks | Long: 2-3 months",
        required_resources: "5 engineers, 1 product manager, payment vendor support, $50K budget for infrastructure"
      },
      metadata: {
        total_mentions: 127,
        sentiment_score: -0.82,
        first_reported: "2024-01-10T14:23:00Z",
        last_updated: "2024-01-15T09:45:00Z",
        affected_user_segments: ["Enterprise", "SMB", "High-Value Customers"],
        geographic_concentration: ["North America", "Europe"],
        severity_indicators: ["revenue_impact", "churn_risk", "legal_risk"]
      }
    },
    {
      id: 2,
      rank: 2,
      title: "Data Export Feature Takes 45+ Minutes for Large Datasets",
      score: 87.6,
      category: "Performance",
      team: "Data Platform",
      preMortemForecast: "Retention Risk: If export performance doesn't improve within 60 days, we'll lose 180+ data-intensive enterprise accounts ($2.1M ARR) who are already evaluating competitor solutions with 10x faster exports. Survey data shows 73% of power users cite export speed as a critical factor in renewal decisions.",
      action_plan: {
        immediate_steps: [
          "Add progress indicator with estimated time remaining",
          "Implement export job status email notifications",
          "Increase export worker pool capacity by 3x",
          "Document workarounds for large dataset exports"
        ],
        medium_term_steps: [
          "Migrate export service to async job queue architecture",
          "Implement incremental/paginated export functionality",
          "Add export compression to reduce file size by 60%",
          "Build export performance optimization algorithm"
        ],
        long_term_steps: [
          "Redesign data export system with streaming architecture",
          "Implement distributed processing for parallel exports",
          "Build real-time export analytics dashboard",
          "Create premium 'instant export' tier with dedicated infrastructure"
        ],
        estimated_timeline: "Immediate: 1 week | Medium: 4-6 weeks | Long: 3-4 months",
        required_resources: "4 backend engineers, 1 DevOps engineer, 2 data engineers, $75K infrastructure budget"
      },
      metadata: {
        total_mentions: 94,
        sentiment_score: -0.71,
        first_reported: "2023-12-15T08:30:00Z",
        last_updated: "2024-01-14T16:20:00Z",
        affected_user_segments: ["Enterprise", "Data Analysts", "Power Users"],
        geographic_concentration: ["Global"],
        severity_indicators: ["retention_risk", "competitive_threat", "product_quality"]
      }
    },
    {
      id: 3,
      rank: 3,
      title: "Mobile App Crashes on Android 14 Devices",
      score: 82.3,
      category: "Stability",
      team: "Mobile Engineering",
      preMortemForecast: "User Acquisition Risk: If Android 14 crashes aren't fixed within 45 days, we'll lose 25% of our mobile user growth (15K+ new users/month) as Android 14 adoption accelerates. App store ratings have dropped from 4.7 to 3.2 stars, directly impacting organic acquisition and costing $120K+ in additional paid UA spend.",
      action_plan: {
        immediate_steps: [
          "Deploy emergency patch to force-downgrade Android 14 users to stable version",
          "Add crash monitoring specific to Android 14 devices",
          "Respond to all 1-star app store reviews with status update",
          "Create Android 14 testing device lab with 10+ devices"
        ],
        medium_term_steps: [
          "Refactor Android lifecycle management for Android 14 compatibility",
          "Implement automated crash reporting with stack traces",
          "Add pre-release testing on Android beta versions",
          "Build automated regression test suite for all Android versions"
        ],
        long_term_steps: [
          "Establish continuous Android OS beta testing program",
          "Implement feature flag system for OS-specific rollouts",
          "Build mobile stability monitoring dashboard",
          "Create mobile platform engineering team"
        ],
        estimated_timeline: "Immediate: 3-5 days | Medium: 3-4 weeks | Long: 2-3 months",
        required_resources: "3 Android engineers, 1 QA engineer, 1 DevOps, $25K for device lab + monitoring tools"
      },
      metadata: {
        total_mentions: 78,
        sentiment_score: -0.79,
        first_reported: "2024-01-05T11:15:00Z",
        last_updated: "2024-01-15T14:30:00Z",
        affected_user_segments: ["Mobile Users", "Android 14 Early Adopters"],
        geographic_concentration: ["North America", "Western Europe", "Asia-Pacific"],
        severity_indicators: ["app_store_rating", "acquisition_impact", "brand_reputation"]
      }
    }
  ],
  total_analyzed: 312,
  total_risk_estimate: "$2.7M ARR at risk + 550+ customers",
  generated_at: "2024-01-15T15:00:00Z",
  agent_pipeline_version: "1.0.0",
  metadata: {
    analysis_duration_seconds: 127,
    llm_model: "gpt-4-turbo-preview",
    confidence_score: 0.91
  }
};

/**
 * Simulate API call with mock data
 * This function can be used for local development before backend is ready
 */
export const fetchMockPriorities = (): Promise<PrioritiesResponse> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log('📦 Returning mock priorities data');
      resolve(mockPrioritiesData);
    }, 800); // Simulate network delay
  });
};

export default mockPrioritiesData;
