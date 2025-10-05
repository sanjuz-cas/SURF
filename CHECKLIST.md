# 🚀 SURF Quick Start Checklist

## Before You Begin

### ✅ Prerequisites Check
- [ ] Python 3.9 or higher installed
- [ ] PostgreSQL 13+ installed and running
- [ ] Git installed (optional, for version control)
- [ ] OpenAI API account with credits
- [ ] Slack workspace (optional, for delivery)

---

## 📦 Installation (5 Steps)

### Step 1: Environment Setup
```powershell
# Run automated setup
python setup.py
```
- [ ] Virtual environment created in `venv/`
- [ ] Dependencies installed from `requirements.txt`
- [ ] `.env` file created from template
- [ ] `logs/` directory created

### Step 2: Configure Credentials
```powershell
# Edit .env file
notepad .env
```
Add your credentials:
- [ ] `OPENAI_API_KEY` = Your OpenAI API key
- [ ] `DB_HOST` = localhost (or your DB host)
- [ ] `DB_NAME` = surf_feedback_db
- [ ] `DB_USER` = surf_user
- [ ] `DB_PASSWORD` = Your secure password
- [ ] `SLACK_WEBHOOK_URL` = Your Slack webhook (optional)

### Step 3: Database Setup
```powershell
# Create database
createdb surf_feedback_db

# Initialize schema + mock data
psql -d surf_feedback_db -f db/init_schema.sql
```
- [ ] Database created
- [ ] Tables created (`raw_feedback`, `prioritized_output`)
- [ ] 10 mock feedback items inserted
- [ ] Indexes and triggers created

### Step 4: Test Configuration
```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Run dry-run test
python backend/main.py --dry-run
```
Expected output:
- [ ] ✅ Environment configuration validated
- [ ] ✅ Database connection pool initialized
- [ ] ✅ 5 agents created successfully
- [ ] ✅ 5 tasks created successfully

### Step 5: Run SURF
```powershell
# Execute the complete pipeline
python backend/main.py

# OR use the quick-start script
.\run.ps1
```
- [ ] Pipeline starts without errors
- [ ] All 5 agents execute in sequence
- [ ] Slack message delivered (or logged locally)
- [ ] Execution log created in `logs/`

---

## 🔍 Verification Checklist

### Database Verification
```sql
-- Check raw feedback
SELECT COUNT(*) FROM raw_feedback;
-- Expected: 10 rows

-- Check processed feedback
SELECT COUNT(*) FROM raw_feedback WHERE processed = TRUE;
-- Expected: 10 rows (after pipeline runs)

-- Check prioritized output
SELECT COUNT(*) FROM prioritized_output;
-- Expected: 3 rows (top 3 items)

-- View top items
SELECT id, title, score, team FROM prioritized_output ORDER BY score DESC;
```
- [ ] 10 raw feedback items exist
- [ ] All items marked as processed
- [ ] Top 3 items in prioritized_output
- [ ] Scores calculated correctly

### Slack Verification (if configured)
- [ ] Message posted to #customer-feedback channel
- [ ] Rich formatting with blocks visible
- [ ] All 3 prioritized items displayed
- [ ] Financial forecasts included
- [ ] Action plans visible

### Log Verification
```powershell
# View latest log
ls logs\ | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```
- [ ] Log file created with timestamp
- [ ] Contains agent execution logs
- [ ] Final payload logged
- [ ] No critical errors

---

## 🎯 Expected Results

### Agent 1: IngestorAgent
```json
{
  "total_items": 10,
  "sources": ["Slack", "Email", "Notion", "Survey"],
  "status": "ready_for_analysis"
}
```

### Agent 2: AnalyzerAgent
```json
{
  "total_analyzed": 10,
  "avg_score": 6.8,
  "category_distribution": {
    "Bug": 5,
    "Feature": 3,
    "UX": 2
  },
  "top_3_scores": [9.0, 9.0, 8.5]
}
```

### Agent 3: PrioritizerAgent
```json
{
  "top_3_items": [
    {
      "id": 4,
      "title": "API Response Time 300% Increase",
      "score": 9.0,
      "team": "Engineering",
      "action_plan": { "immediate_action": "...", "timeline": "..." }
    }
    // ... 2 more items
  ]
}
```

### Agent 4: RetentionCriticAgent
```json
{
  "items": [
    {
      "id": 4,
      "pre_mortem_forecast": "Estimated 90-day impact: $1.8M-$2.3M loss..."
    }
    // ... 2 more with forecasts
  ],
  "total_risk_estimate": "$3.5M-$5.0M over 90 days"
}
```

### Agent 5: DelivererAgent
```json
{
  "slack_delivery_status": "success",
  "delivery_timestamp": "2025-10-03T12:34:56",
  "final_payload": { "items": [...] }
}
```

---

## 🐛 Troubleshooting

### Issue: Database Connection Failed
**Symptoms**: `❌ Failed to connect to database`

**Solutions**:
1. Check PostgreSQL is running: `pg_isready`
2. Verify credentials in `.env`
3. Test connection: `psql -h localhost -U surf_user -d surf_feedback_db`
4. Check firewall settings

### Issue: OpenAI API Error
**Symptoms**: `❌ OpenAI API authentication failed`

**Solutions**:
1. Verify API key in `.env` (starts with `sk-`)
2. Check API key validity at https://platform.openai.com/api-keys
3. Ensure sufficient credits in OpenAI account
4. Try a different model: `OPENAI_MODEL=gpt-3.5-turbo`

### Issue: Slack Delivery Failed
**Symptoms**: `⚠️ Slack webhook error`

**Solutions**:
1. Verify webhook URL in `.env`
2. Test webhook manually:
   ```powershell
   Invoke-RestMethod -Uri $env:SLACK_WEBHOOK_URL -Method Post -Body '{"text":"Test"}' -ContentType 'application/json'
   ```
3. Check Slack app permissions
4. Note: Pipeline continues with local logging even if Slack fails

### Issue: Import Errors
**Symptoms**: `ModuleNotFoundError: No module named 'crewai'`

**Solutions**:
1. Activate virtual environment: `.\venv\Scripts\activate`
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python version: `python --version` (must be 3.9+)

---

## 📚 Next Steps After Setup

### 1. Explore the System
- [ ] Read `README.md` for comprehensive documentation
- [ ] Review `SETUP_GUIDE.md` for detailed instructions
- [ ] Check `PROJECT_SUMMARY.md` for overview
- [ ] View `ARCHITECTURE.txt` for system diagram

### 2. Customize Configuration
- [ ] Adjust scoring weights in `.env`
- [ ] Change top items count (default: 3)
- [ ] Switch LLM model for cost/speed optimization
- [ ] Configure Slack channel

### 3. Add Real Data
- [ ] Replace mock data with actual feedback
- [ ] Integrate with Slack for live ingestion
- [ ] Connect to email/Notion APIs
- [ ] Setup automated data pipelines

### 4. Schedule Execution
- [ ] Create Windows Task Scheduler job (daily)
- [ ] Or setup cron job (Unix/Mac)
- [ ] Configure email notifications
- [ ] Setup monitoring/alerting

### 5. Extend Functionality
- [ ] Build React frontend dashboard
- [ ] Add Jira integration for ticket creation
- [ ] Implement sentiment analysis
- [ ] Create historical trend reports

---

## 🎓 Learning Resources

### CrewAI Documentation
- Official Docs: https://docs.crewai.com/
- GitHub: https://github.com/joaomdmoura/crewAI
- Examples: https://github.com/joaomdmoura/crewAI-examples

### LangChain Documentation
- Official Docs: https://python.langchain.com/
- Tutorials: https://python.langchain.com/docs/tutorials/

### PostgreSQL Resources
- Official Docs: https://www.postgresql.org/docs/
- Tutorial: https://www.postgresqltutorial.com/

---

## ✅ Success Criteria

Your SURF installation is successful when:

- [x] ✅ Setup script completes without errors
- [x] ✅ `.env` file configured with valid credentials
- [x] ✅ Database initialized with schema + mock data
- [x] ✅ Dry-run mode passes all checks
- [x] ✅ All 5 agents execute in sequence
- [x] ✅ Top 3 feedback items prioritized
- [x] ✅ Financial forecasts generated
- [x] ✅ Slack delivery successful (or logged locally)
- [x] ✅ Execution completes in 2-5 minutes

---

## 🆘 Need Help?

1. **Documentation**: Check `README.md` and `SETUP_GUIDE.md`
2. **Logs**: Review `logs/surf_execution_*.log` for errors
3. **Verbose Mode**: Run with `--verbose --log-level DEBUG`
4. **GitHub Issues**: Open an issue at https://github.com/sanjuz-cas/SURF/issues

---

## 🎉 You're Ready!

Once all checkboxes are complete, your SURF Customer Feedback Agent is:
- ✅ Fully installed
- ✅ Properly configured
- ✅ Ready for production use

**Run the pipeline**: `.\run.ps1` or `python backend/main.py`

**Welcome to SURF! 🌊**
