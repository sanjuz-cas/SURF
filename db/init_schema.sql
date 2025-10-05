-- =========================================================
-- SURF Customer Feedback Agent - Database Schema
-- =========================================================
-- PostgreSQL Schema for Customer Feedback Processing

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS prioritized_output CASCADE;
DROP TABLE IF EXISTS raw_feedback CASCADE;

-- Create raw_feedback table
-- Stores all incoming customer feedback before processing
CREATE TABLE raw_feedback (
    id SERIAL PRIMARY KEY,
    raw_text TEXT NOT NULL,
    source VARCHAR(100) NOT NULL,  -- e.g., 'Slack', 'Email', 'Notion', 'Survey'
    category VARCHAR(50),  -- 'Bug', 'Feature', 'UX', 'Other'
    severity_volume_score FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE,
    metadata JSONB  -- Additional structured data
);

-- Create prioritized_output table
-- Stores the final prioritized feedback with action plans
CREATE TABLE prioritized_output (
    id SERIAL PRIMARY KEY,
    feedback_id INTEGER REFERENCES raw_feedback(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    pre_mortem_forecast TEXT,  -- Financial risk assessment from RetentionCriticAgent
    score FLOAT NOT NULL,
    team VARCHAR(100),  -- Assigned team: 'Engineering', 'Product', 'UX', 'Support'
    action_plan JSONB,  -- Structured action plan
    priority_rank INTEGER,  -- 1 = highest priority
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    slack_delivered BOOLEAN DEFAULT FALSE,
    slack_delivered_at TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_raw_feedback_processed ON raw_feedback(processed);
CREATE INDEX idx_raw_feedback_score ON raw_feedback(severity_volume_score DESC);
CREATE INDEX idx_raw_feedback_created ON raw_feedback(created_at DESC);
CREATE INDEX idx_prioritized_output_rank ON prioritized_output(priority_rank);
CREATE INDEX idx_prioritized_output_score ON prioritized_output(score DESC);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to auto-update updated_at
CREATE TRIGGER update_raw_feedback_updated_at 
    BEFORE UPDATE ON raw_feedback
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample mock data for testing (10 items as specified)
INSERT INTO raw_feedback (raw_text, source, metadata) VALUES
('Our mobile app crashes every time I try to upload a photo on iOS 17. This is blocking my entire workflow!', 'Slack', '{"user_tier": "Enterprise", "urgency": "high"}'),
('Would love to see dark mode support in the dashboard. My eyes hurt after long sessions.', 'Email', '{"user_tier": "Pro", "urgency": "low"}'),
('The new checkout flow is confusing. Lost 3 customers this week because they couldnt figure out payment.', 'Notion', '{"user_tier": "Enterprise", "urgency": "critical"}'),
('API response times have increased 300% since last update. Timeout errors everywhere.', 'Slack', '{"user_tier": "Enterprise", "urgency": "critical"}'),
('Love the product but the onboarding tutorial is outdated. References features that dont exist anymore.', 'Survey', '{"user_tier": "Free", "urgency": "medium"}'),
('Bulk export feature is missing. We need to export 50K records monthly for compliance.', 'Email', '{"user_tier": "Enterprise", "urgency": "high"}'),
('Minor UI bug: dropdown menu overlaps with the header on smaller screens.', 'Slack', '{"user_tier": "Pro", "urgency": "low"}'),
('Security concern: passwords are visible in plain text in the browser console during login.', 'Email', '{"user_tier": "Enterprise", "urgency": "critical"}'),
('Feature request: integration with Salesforce would be a game changer for our sales team.', 'Notion', '{"user_tier": "Enterprise", "urgency": "medium"}'),
('Customer support response time is too slow. Waited 48 hours for a reply on a critical issue.', 'Survey', '{"user_tier": "Pro", "urgency": "high"}');

-- Verify data insertion
SELECT COUNT(*) as total_feedback FROM raw_feedback;

COMMENT ON TABLE raw_feedback IS 'Stores raw customer feedback from all sources';
COMMENT ON TABLE prioritized_output IS 'Stores prioritized feedback with action plans and risk assessments';
COMMENT ON COLUMN raw_feedback.severity_volume_score IS 'Calculated score based on severity and volume metrics';
COMMENT ON COLUMN prioritized_output.pre_mortem_forecast IS 'Financial risk assessment if feedback is ignored (from RetentionCriticAgent)';