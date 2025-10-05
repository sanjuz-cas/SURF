# 🌊 SURF - Strategic User Retention & Feedback Agent

An industrial-grade, AI-powered customer feedback processing system built with **CrewAI**, **Python**, and **PostgreSQL**. SURF uses a 5-agent pipeline to automatically prioritize customer feedback and assess financial risk.

## 🎯 Overview

SURF (Strategic User Retention & Feedback) is a multi-agent system that:
- 📥 **Ingests** customer feedback from multiple sources (Slack, Email, Notion, Surveys)
- 🔍 **Analyzes** and categorizes feedback (Bug/Feature/UX)
- 📊 **Scores** items based on severity and volume
- 🎯 **Prioritizes** the top 3 critical issues
- 💰 **Assesses** 90-day financial risk if issues are ignored
- 📨 **Delivers** actionable reports to Slack

## 🏗️ Architecture

### 5-Agent Pipeline

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ 1. Ingestor  │───▶│ 2. Analyzer  │───▶│ 3. Prioritizer│
│    Agent     │    │    Agent     │    │     Agent     │
└──────────────┘    └──────────────┘    └──────────────┘
       ▼                   ▼                    ▼
  Standardize        Categorize &          Select Top 3
  Raw Feedback      Calculate Score       + Action Plans
                                                 │
                                                 ▼
┌──────────────┐    ┌──────────────────────────────┐
│ 5. Deliverer │◀───│ 4. Retention Critic Agent    │
│    Agent     │    │    (Financial Risk)          │
└──────────────┘    └──────────────────────────────┘
       ▼                        ▼
   Post to Slack          Pre-Mortem Analysis
                         ($$ ARR Loss Estimate)
```

### Agent Details

| Agent | Role | Responsibility |
|-------|------|----------------|
| **IngestorAgent** | Data Unifier | Retrieve and standardize raw feedback from PostgreSQL |
| **AnalyzerAgent** | Category & Score Analyst | Categorize (Bug/Feature/UX) and calculate Severity-Volume Score (0-10) |
| **PrioritizerAgent** | Strategic Product Manager | Select top 3 items and generate action plans (team, timeline, metrics) |
| **RetentionCriticAgent** | 90-Day Financial Risk Assessor | Conduct pre-mortem analysis: estimate churn, ARR loss, and total financial impact |
| **DelivererAgent** | Workflow Automation Specialist | Format and deliver final report to Slack with rich formatting |

## 📁 Project Structure

```
SURF/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agent_definitions.py      # 5 CrewAI agents
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── task_definitions.py       # Sequential tasks
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── postgres_tool.py          # Custom PostgreSQL tool
│   │   └── slack_tool.py             # Custom Slack posting tool
│   ├── crew_orchestrator.py          # Crew assembly & execution
│   ├── db_connection.py              # PostgreSQL connection pool
│   └── main.py                       # Main execution script
├── db/
│   ├── init_schema.sql               # Database schema + mock data
│   └── schema.sql                    # Original schema
├── frontend/                         # (Future: React dashboard)
├── integrations/                     # (Future: API connectors)
├── .env.example                      # Environment configuration template
├── .gitignore
├── requirements.txt                  # Python dependencies
├── package.json
└── README.md                         # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **PostgreSQL 13+**
- **OpenAI API Key** (for LLM agents)
- **Slack Webhook URL** (optional, for delivery)

### 1. Clone & Setup Environment

```bash
# Clone the repository
cd SURF

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your credentials:
# - OPENAI_API_KEY
# - DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
# - SLACK_WEBHOOK_URL (optional)
```

### 3. Setup Database

```bash
# Create PostgreSQL database
createdb surf_feedback_db

# Run the schema initialization
psql -d surf_feedback_db -f db/init_schema.sql

# This creates tables and inserts 10 mock feedback items
```

### 4. Run SURF

```bash
# Execute the complete pipeline
python backend/main.py

# With verbose logging
python backend/main.py --verbose --log-level DEBUG

# Dry run (check configuration without executing)
python backend/main.py --dry-run
```

## 📊 Database Schema

### `raw_feedback` Table
```sql
id                      SERIAL PRIMARY KEY
raw_text                TEXT NOT NULL
source                  VARCHAR(100) NOT NULL
category                VARCHAR(50)
severity_volume_score   FLOAT DEFAULT 0.0
created_at              TIMESTAMP
updated_at              TIMESTAMP
processed               BOOLEAN DEFAULT FALSE
metadata                JSONB
```

### `prioritized_output` Table
```sql
id                      SERIAL PRIMARY KEY
feedback_id             INTEGER (FK → raw_feedback)
title                   VARCHAR(500) NOT NULL
pre_mortem_forecast     TEXT
score                   FLOAT NOT NULL
team                    VARCHAR(100)
action_plan             JSONB
priority_rank           INTEGER
created_at              TIMESTAMP
slack_delivered         BOOLEAN DEFAULT FALSE
slack_delivered_at      TIMESTAMP
```

## 🛠️ Custom Tools

### PostgresTool
```python
# Operations:
- read_top_items(limit=3)
- update_item_score(feedback_id, category, score)
- get_unprocessed_feedback(limit=10)
- get_all_feedback()
```

### PostToSlackTool
```python
# Features:
- Rich message formatting with blocks
- Webhook and Bot Token support
- Automatic fallback to local logging
- Professional formatting for feedback reports
```

## 📈 Example Output

```json
{
  "items": [
    {
      "rank": 1,
      "title": "API Response Time Degradation",
      "category": "Bug",
      "score": 9.0,
      "team": "Engineering",
      "pre_mortem_forecast": "Estimated 90-day impact if ignored:\n- Churn: 20-25% of Enterprise customers (~$1M-$1.5M ARR loss)\n- Lost deals: 15 prospects, ~$750K pipeline impact\n- Support costs: +40% ticket volume, ~$80K additional costs\n- Total estimated loss: $1.8M-$2.3M over 90 days",
      "action_plan": {
        "immediate_action": "Deploy APM monitoring, identify bottlenecks",
        "timeline": "1 week investigation, 2 weeks optimization",
        "success_metric": "Response time < 200ms, 0 timeouts",
        "dependencies": "Engineering, DevOps, Database team"
      }
    }
  ],
  "total_analyzed": 10,
  "total_risk_estimate": "$3.5M-$5.0M over 90 days"
}
```

## 🔧 Configuration

### Scoring Algorithm

The **AnalyzerAgent** uses the following scoring criteria:

| Category | Severity Range | Factors |
|----------|---------------|---------|
| **Security Issues** | 9-10 | Critical vulnerabilities |
| **Enterprise Bugs** | 7-10 | Customer tier: Enterprise (+2) |
| **Performance** | 7-9 | Degradation severity |
| **UX Issues** | 4-6 | User experience impact |
| **Feature Requests** | 3-8 | Business value + urgency |

**Metadata Modifiers:**
- `user_tier`: Enterprise (+2), Pro (+1), Free (+0)
- `urgency`: critical (+2), high (+1), medium (+0.5), low (+0)

### Financial Risk Assessment

The **RetentionCriticAgent** uses these benchmarks:

- Enterprise customer LTV: **$100K-$500K** annually
- Pro customer LTV: **$10K-$50K** annually
- Security issue churn: **30-50%** of enterprise customers
- Performance issue impact: **10-15%** customer base
- Average support cost increase: **20-40%** for unresolved issues

## 📝 Logging

Logs are saved to `logs/surf_execution_YYYYMMDD_HHMMSS.log`

```bash
# View recent logs
ls -lt logs/

# Tail the latest log
tail -f logs/surf_execution_*.log
```

## 🧪 Testing

```bash
# Run with mock data (included in init_schema.sql)
python backend/main.py

# The pipeline will process 10 pre-loaded feedback items:
# - 3 Enterprise critical issues
# - 2 Security concerns
# - 2 Feature requests
# - 2 UX improvements
# - 1 Support issue
```

## 🔌 Integrations

### Slack
- Supports webhook URL (easiest setup)
- Supports bot token for channel selection
- Automatic fallback to console logging

### Future Integrations (Planned)
- **Notion**: Sync to Notion database
- **Email**: SMTP delivery
- **Jira**: Auto-create tickets for top items

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Built with:
- **[CrewAI](https://github.com/joaomdmoura/crewAI)** - Multi-agent framework
- **[LangChain](https://langchain.com/)** - LLM orchestration
- **[OpenAI](https://openai.com/)** - GPT-4 models
- **[PostgreSQL](https://www.postgresql.org/)** - Database
- **[Slack API](https://api.slack.com/)** - Notifications

---

**Built with ❤️ by the SURF Team**

For questions or support, please open an issue on GitHub.