# SURF Customer Feedback Agent - Complete Setup Guide
# ===================================================

## 🎯 Project Overview

SURF (Strategic User Retention & Feedback) is an industrial-grade, AI-powered customer feedback processing system that uses a 5-agent CrewAI pipeline to:

1. **Ingest** customer feedback from multiple sources
2. **Analyze** and categorize feedback (Bug/Feature/UX)
3. **Score** items based on severity and volume
4. **Prioritize** the top 3 critical issues
5. **Assess** financial risk (90-day ARR loss estimates)
6. **Deliver** actionable reports to Slack

---

## 📋 Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Python 3.9+** installed
- [ ] **PostgreSQL 13+** installed and running
- [ ] **OpenAI API Key** (for GPT-4 agents)
- [ ] **Slack Webhook URL** (optional, for delivery)
- [ ] **Git** (to clone the repository)

---

## 🚀 Installation Steps

### Step 1: Setup Python Environment

```powershell
# Navigate to the project directory
cd C:\Users\SANJAY\Desktop\SURF

# Run the automated setup script
python setup.py
```

The setup script will:
- ✅ Check Python version (3.9+ required)
- ✅ Create virtual environment in `venv/`
- ✅ Install all dependencies from `requirements.txt`
- ✅ Create `.env` file from `.env.example`
- ✅ Create necessary directories (`logs/`)

### Step 2: Configure Environment

Edit the `.env` file with your credentials:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# PostgreSQL Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=surf_feedback_db
DB_USER=surf_user
DB_PASSWORD=your_secure_password

# Slack Integration (Optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_CHANNEL=#customer-feedback
```

### Step 3: Setup PostgreSQL Database

```powershell
# Create the database
createdb surf_feedback_db

# Create database user (optional)
psql -c "CREATE USER surf_user WITH PASSWORD 'your_secure_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE surf_feedback_db TO surf_user;"

# Initialize schema and mock data
psql -d surf_feedback_db -f db/init_schema.sql
```

This will create:
- `raw_feedback` table (stores incoming feedback)
- `prioritized_output` table (stores processed results)
- 10 mock feedback items for testing

### Step 4: Verify Installation

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Run in dry-run mode to test configuration
python backend/main.py --dry-run
```

Expected output:
```
✅ Environment configuration validated
✅ Database connection pool initialized
🔍 DRY RUN MODE - Configuration validated
```

---

## 🎮 Usage

### Option 1: Using the Run Script (Recommended)

```powershell
# Simple execution
.\run.ps1

# With verbose logging
.\run.ps1 --verbose --log-level DEBUG
```

### Option 2: Direct Python Execution

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Run the pipeline
python backend/main.py

# With options
python backend/main.py --verbose --log-level DEBUG
python backend/main.py --dry-run
```

---

## 📊 Understanding the Pipeline

### Pipeline Flow

```
Step 1: IngestorAgent
├─ Retrieves all raw feedback from database
├─ Verifies data integrity
└─ Outputs: {total_items: 10, sources: [...]}

Step 2: AnalyzerAgent
├─ Categorizes each item (Bug/Feature/UX)
├─ Calculates Severity-Volume Score (0-10)
├─ Updates database with scores
└─ Outputs: {total_analyzed: 10, avg_score: 6.5, ...}

Step 3: PrioritizerAgent
├─ Selects top 3 highest-scored items
├─ Generates action plans for each
├─ Assigns teams and timelines
└─ Outputs: {top_3_items: [...]}

Step 4: RetentionCriticAgent
├─ Conducts pre-mortem financial analysis
├─ Estimates 90-day ARR loss if ignored
├─ Calculates churn risk percentages
└─ Outputs: {items with pre_mortem_forecast: "..."}

Step 5: DelivererAgent
├─ Formats final report as JSON
├─ Posts to Slack with rich formatting
└─ Outputs: {slack_delivery_status: "success"}
```

### Expected Execution Time

- **Total Duration**: 2-5 minutes (depending on LLM response times)
- **Per Agent**: 30-60 seconds average

---

## 🔍 Monitoring & Debugging

### Logs

All execution logs are saved to `logs/surf_execution_YYYYMMDD_HHMMSS.log`

```powershell
# View logs directory
ls logs\

# View the latest log
Get-Content logs\surf_execution_*.log | Select-Object -Last 50

# Monitor in real-time (requires tail utility or PowerShell 7+)
Get-Content logs\surf_execution_*.log -Wait
```

### Common Issues

#### Issue: Database Connection Failed

**Error**: `❌ Failed to connect to database`

**Solution**:
1. Verify PostgreSQL is running: `pg_isready`
2. Check credentials in `.env` file
3. Test connection: `psql -h localhost -U surf_user -d surf_feedback_db`

#### Issue: OpenAI API Error

**Error**: `❌ OpenAI API authentication failed`

**Solution**:
1. Verify API key in `.env` file
2. Check API key validity: `curl https://api.openai.com/v1/models -H "Authorization: Bearer YOUR_KEY"`
3. Ensure sufficient OpenAI credits

#### Issue: Slack Delivery Failed

**Error**: `⚠️ Slack webhook error`

**Solution**:
1. Verify webhook URL in `.env`
2. Test webhook: 
   ```powershell
   Invoke-RestMethod -Uri $env:SLACK_WEBHOOK_URL -Method Post -Body '{"text":"Test"}' -ContentType 'application/json'
   ```
3. Note: Pipeline continues even if Slack fails (logs locally)

---

## 🧪 Testing with Mock Data

The database initialization includes 10 realistic mock feedback items:

| ID | Category | Source | Severity | Description |
|----|----------|--------|----------|-------------|
| 1 | Bug | Slack | High | iOS app crash on photo upload |
| 2 | Feature | Email | Low | Dark mode request |
| 3 | Bug | Notion | Critical | Confusing checkout flow |
| 4 | Bug | Slack | Critical | API response time 300% increase |
| 5 | UX | Survey | Medium | Outdated onboarding tutorial |
| 6 | Feature | Email | High | Missing bulk export feature |
| 7 | Bug | Slack | Low | UI dropdown overlap |
| 8 | Bug | Email | Critical | Password visible in console |
| 9 | Feature | Notion | Medium | Salesforce integration request |
| 10 | UX | Survey | High | Slow customer support response |

Expected top 3 prioritized items:
1. **API response time degradation** (Score: ~9.0)
2. **Security: Password in console** (Score: ~9.0)
3. **Checkout flow confusion** (Score: ~8.5)

---

## 📈 Customization

### Adjusting Scoring Weights

Edit `.env`:
```bash
SEVERITY_WEIGHT=0.6  # Weight for severity (default: 0.6)
VOLUME_WEIGHT=0.4    # Weight for volume (default: 0.4)
TOP_ITEMS_COUNT=3    # Number of top items (default: 3)
```

### Changing LLM Model

Edit `.env`:
```bash
OPENAI_MODEL=gpt-4-turbo-preview  # For best results
# OR
OPENAI_MODEL=gpt-3.5-turbo        # For faster, cheaper execution
```

### Adding More Feedback Sources

Edit `db/init_schema.sql` and add more INSERT statements:
```sql
INSERT INTO raw_feedback (raw_text, source, metadata) VALUES
('Your new feedback text', 'NewSource', '{"user_tier": "Enterprise"}');
```

---

## 📚 Architecture Details

### Database Tables

**raw_feedback**
- Primary table for all incoming feedback
- Updated by AnalyzerAgent with scores
- Supports JSONB metadata for flexible attributes

**prioritized_output**
- Stores final prioritized results
- Tracks Slack delivery status
- Contains action plans and risk assessments

### Agent Roles

1. **IngestorAgent**: Data quality gatekeeper
2. **AnalyzerAgent**: Scoring engine with business logic
3. **PrioritizerAgent**: Strategic planning expert
4. **RetentionCriticAgent**: Financial analyst (CFO-level thinking)
5. **DelivererAgent**: Communication specialist

### Tools

**PostgresTool** (`backend/tools/postgres_tool.py`)
- Custom CrewAI tool for database operations
- Methods: read_top_items, update_item_score, get_unprocessed_feedback

**PostToSlackTool** (`backend/tools/slack_tool.py`)
- Custom CrewAI tool for Slack integration
- Supports webhook and bot token methods
- Rich message formatting with blocks

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** (already in `.gitignore`)
2. **Use strong database passwords**
3. **Rotate OpenAI API keys regularly**
4. **Restrict database user permissions**
5. **Use HTTPS for Slack webhooks**

---

## 🤝 Support & Troubleshooting

### Getting Help

1. Check logs in `logs/` directory
2. Run with `--verbose` flag for detailed output
3. Review `README.md` for detailed documentation
4. Open an issue on GitHub

### Performance Tips

1. Use `gpt-4-turbo-preview` for best quality
2. Consider `gpt-3.5-turbo` for faster execution
3. Adjust `max_iter` in agent definitions for complexity control
4. Use database indexes (already configured in schema)

---

## ✅ Success Criteria

Your setup is successful when:

✅ `python backend/main.py --dry-run` completes without errors
✅ All 5 agents are created successfully
✅ Database connection is established
✅ Mock data is processed (10 items)
✅ Top 3 items are prioritized with financial forecasts
✅ Slack message is delivered (or logged locally)

---

## 🎉 Next Steps

After successful setup:

1. **Test with real data**: Replace mock data with actual customer feedback
2. **Integrate sources**: Connect to Slack/Notion/Email APIs
3. **Customize scoring**: Adjust weights based on your business metrics
4. **Schedule execution**: Run periodically (daily/weekly) via cron/Task Scheduler
5. **Build dashboard**: Use the frontend/ directory for React UI (future)

---

**Need Help?** Check `README.md` or open an issue!

**Built with ❤️ using CrewAI, Python, and PostgreSQL**
