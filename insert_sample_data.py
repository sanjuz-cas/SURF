"""Insert sample prioritized data for testing."""
import psycopg
import json

conn = psycopg.connect(
    host='localhost',
    port=5432,
    dbname='surf_feedback_db',
    user='surf_user',
    password='surf_password_2024'
)

cur = conn.cursor()

# Sample action plans
action_plans = [
    {
        "immediate_steps": ["Reproduce issue on Safari 15.2", "Implement event listener fix", "Add cross-browser compatibility check"],
        "medium_term_steps": ["Create comprehensive browser testing suite", "Add automated browser compatibility tests"],
        "long_term_steps": ["Implement progressive enhancement strategy", "Set up continuous cross-browser testing"]
    },
    {
        "immediate_steps": ["Investigate mobile-specific layout issues", "Fix responsive breakpoints"],
        "medium_term_steps": ["Optimize mobile load time", "Add mobile-specific performance tests"],
        "long_term_steps": ["Redesign mobile UX completely", "Implement mobile-first architecture"]
    },
    {
        "immediate_steps": ["Analyze 2FA implementation options", "Create security requirement document"],
        "medium_term_steps": ["Implement 2FA backend infrastructure", "Add SMS and authenticator app support"],
        "long_term_steps": ["Roll out 2FA to all users", "Add biometric authentication"]
    },
    {
        "immediate_steps": ["Review current dashboard information architecture", "Conduct user research on pain points"],
        "medium_term_steps": ["Create new dashboard wireframes", "A/B test new layouts"],
        "long_term_steps": ["Full dashboard redesign rollout", "Implement customizable dashboards"]
    },
    {
        "immediate_steps": ["Profile slow database queries", "Add query caching"],
        "medium_term_steps": ["Optimize database indexes", "Implement query result caching"],
        "long_term_steps": ["Consider database sharding", "Implement read replicas"]
    },
    {
        "immediate_steps": ["Design CSV export schema", "Implement backend export endpoint"],
        "medium_term_steps": ["Add scheduling for automated exports", "Support multiple export formats"],
        "long_term_steps": ["Add Excel integration", "Create custom report builder"]
    }
]

# Insert sample prioritized output
inserts = [
    (1, "Login button unresponsive on Safari 15.2", "A critical issue blocking a segment of users. The main risk is not having access to a testing device, leading to a speculative fix that may not work.", 98.0, "Engineering", json.dumps(action_plans[0]), 1),
    (2, "User profile page fails to load on mobile", "High severity - affects mobile users who represent 45% of our user base. Risk of losing mobile-first customers.", 95.0, "Engineering", json.dumps(action_plans[1]), 2),
    (3, "Implement two-factor authentication (2FA)", "Security enhancement requested by 30% of enterprise customers. Risk of losing large accounts without this feature.", 92.0, "Security", json.dumps(action_plans[2]), 3),
    (4, "Redesign main dashboard for clarity", "UX improvement affecting all users. Current design confuses new users based on onboarding metrics.", 88.0, "UX", json.dumps(action_plans[3]), 4),
    (5, "Optimize database queries for reporting endpoints", "Performance issue causing slow load times (5-8 seconds) for 20% of users during peak hours.", 85.0, "Engineering", json.dumps(action_plans[4]), 5),
    (6, "Add CSV export functionality to user tables", "Feature request from 15+ enterprise customers. Missing functionality compared to competitors.", 76.0, "Product", json.dumps(action_plans[5]), 6),
]

for insert_data in inserts:
    cur.execute("""
        INSERT INTO prioritized_output 
        (feedback_id, title, pre_mortem_forecast, score, team, action_plan, priority_rank)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, insert_data)

conn.commit()
print(f"✓ Inserted {len(inserts)} sample prioritized items")
conn.close()
