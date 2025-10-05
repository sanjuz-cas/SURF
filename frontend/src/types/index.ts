/**
 * SURF Customer Feedback Dashboard - TypeScript Type Definitions
 * ==============================================================
 * Defines the data structures for prioritized customer feedback items.
 */

/**
 * Category types for customer feedback
 */
export type Category = string;

/**
 * Team assignments for feedback items
 */
export type Team = string;

/**
 * Action plan structure for each prioritized item
 */
export interface ActionPlan {
  immediate_steps: string[];
  medium_term_steps: string[];
  long_term_steps: string[];
  estimated_timeline: string;
  required_resources: string;
}

/**
 * Metadata for prioritized items
 */
export interface ItemMetadata {
  total_mentions: number;
  sentiment_score: number;
  first_reported: string;
  last_updated: string;
  affected_user_segments: string[];
  geographic_concentration: string[];
  severity_indicators: string[];
}

/**
 * Main interface for prioritized feedback items
 * REQUIRED fields: title, score, preMortemForecast
 */
export interface PrioritizedItem {
  id: number;
  feedback_id?: number;
  rank: number;
  title: string;
  category: Category;
  score: number;
  team: Team;
  preMortemForecast: string;  // REQUIRED: Financial risk assessment
  action_plan: ActionPlan;
  metadata?: ItemMetadata;
  raw_text?: string;
  source?: string;
  created_at?: string;
}

/**
 * API response metadata
 */
export interface ResponseMetadata {
  analysis_duration_seconds: number;
  llm_model: string;
  confidence_score: number;
}

/**
 * API response wrapper for prioritized items
 */
export interface PrioritiesResponse {
  items: PrioritizedItem[];
  total_analyzed: number;
  total_risk_estimate: string;
  generated_at: string;
  agent_pipeline_version?: string;
  metadata?: ResponseMetadata;
}

/**
 * API error response
 */
export interface ApiError {
  error: string;
  message: string;
  status: number;
}
