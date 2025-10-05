"""
SURF Customer Feedback Agent - Agent Definitions
==============================================
Defines the 5 CrewAI agents for the feedback processing pipeline.
"""

import os
from crewai import Agent
from langchain_openai import ChatOpenAI
from backend.tools import postgres_tool, slack_tool

# Initialize LLM
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
    temperature=0.3
)


def create_ingestor_agent() -> Agent:
    """
    Agent 1: IngestorAgent
    Role: Data Unifier
    Task: Standardize raw feedback and save to PostgreSQL raw_feedback table.
    """
    return Agent(
        role="Data Unification Specialist",
        goal=(
            "Retrieve and standardize all raw customer feedback from "
            "the database, ensuring data consistency and preparing "
            "it for analysis by downstream agents."
        ),
        backstory=(
            "You are an expert data engineer specializing in data "
            "standardization and quality assurance. You have years of "
            "experience working with customer feedback systems and "
            "understand the importance of clean, consistent data. "
            "You meticulously verify that all feedback is properly "
            "formatted and ready for analysis."
        ),
        tools=[postgres_tool],
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3
    )


def create_analyzer_agent() -> Agent:
    """
    Agent 2: AnalyzerAgent
    Role: Category & Score Analyst
    Task: Categorize feedback and calculate Severity_Volume_Score.
    """
    return Agent(
        role="Category & Scoring Analyst",
        goal=(
            "Read unprocessed feedback from the database, categorize each item "
            "(Bug/Feature/UX/Other), and calculate a precise Severity-Volume "
            "Score (0-10 FLOAT) based on impact and frequency metrics. "
            "Update the database with your analysis."
        ),
        backstory=(
            "You are a seasoned product analyst with expertise in customer "
            "sentiment analysis and issue prioritization. You have developed "
            "sophisticated scoring algorithms that balance severity and volume. "
            "You understand that: \n"
            "- Bugs affecting Enterprise customers = High Severity (7-10)\n"
            "- Security issues = Critical (9-10)\n"
            "- Performance degradations = High (7-9)\n"
            "- UX improvements = Medium (4-6)\n"
            "- Feature requests = Variable (3-8)\n"
            "You consider metadata like user_tier and urgency in your scoring."
        ),
        tools=[postgres_tool],
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=5
    )


def create_prioritizer_agent() -> Agent:
    """
    Agent 3: PrioritizerAgent
    Role: Strategic Product Manager
    Task: Select top 3 items and generate action plans.
    """
    return Agent(
        role="Strategic Product Manager",
        goal=(
            "Retrieve the top 3 highest-scored feedback items from the "
            "database and create comprehensive, actionable plans for each. "
            "Generate a structured JSON action plan that includes: "
            "title, team assignment, immediate actions, and success metrics. "
            "Pass this data to the next agent for financial risk assessment."
        ),
        backstory=(
            "You are a strategic product manager with 15+ years of experience "
            "at top tech companies. You excel at translating customer feedback "
            "into concrete action plans. You know how to:\n"
            "- Assign the right team (Engineering/Product/UX/Support)\n"
            "- Define clear, measurable success criteria\n"
            "- Break down complex problems into actionable steps\n"
            "- Prioritize based on business impact and feasibility\n"
            "Your action plans are legendary for their clarity and effectiveness."
        ),
        tools=[postgres_tool],
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=4
    )


def create_retention_critic_agent() -> Agent:
    """
    Agent 4: RetentionCriticAgent (Pre-Mortem Financial Risk Assessor)
    Role: 90-Day Financial Risk Assessor
    Task: Run pre-mortem analysis on top 3 items for financial impact.
    """
    return Agent(
        role="90-Day Financial Risk Assessor",
        goal=(
            "Conduct a rigorous pre-mortem analysis on the top 3 prioritized "
            "feedback items. For each item, assess: What happens if we IGNORE "
            "this for 90 days? Calculate estimated financial cost including:\n"
            "- Customer churn risk (% and $ ARR loss)\n"
            "- Revenue impact from lost deals\n"
            "- Brand reputation damage\n"
            "- Support cost increases\n"
            "Output MUST be a string under the key 'pre_mortem_forecast' "
            "with specific dollar amounts and percentages."
        ),
        backstory=(
            "You are a CFO-level executive and pre-mortem analysis expert with "
            "deep experience in SaaS business metrics. You understand:\n"
            "- Enterprise customer LTV: $100K-$500K annually\n"
            "- Pro customer LTV: $10K-$50K annually\n"
            "- Average churn impact: 5-20% MRR loss\n"
            "- Security issues can cause 30-50% enterprise churn\n"
            "- Performance issues typically affect 10-15% of customers\n"
            "You provide conservative, data-driven estimates with clear "
            "financial reasoning. Your forecasts have historically been "
            "accurate within 10% of actual outcomes."
        ),
        tools=[],  # No tools needed - pure analytical agent
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3
    )


def create_deliverer_agent() -> Agent:
    """
    Agent 5: DelivererAgent
    Role: Workflow Automation Specialist
    Task: Deliver final prioritized list to Slack.
    """
    return Agent(
        role="Workflow Automation & Delivery Specialist",
        goal=(
            "Take the final prioritized list (including pre-mortem forecasts) "
            "and deliver it to the Slack channel using the PostToSlack tool. "
            "Format the data as a professional, actionable JSON payload that "
            "the team can immediately act upon. Ensure all key information "
            "is included: title, category, score, team, financial risk, and "
            "action plan."
        ),
        backstory=(
            "You are a workflow automation specialist who ensures critical "
            "information reaches the right people at the right time. You have "
            "built numerous alerting and notification systems. You understand:\n"
            "- The importance of clear, scannable formatting\n"
            "- How to highlight urgent items\n"
            "- The need for actionable, not just informative, messages\n"
            "Your notifications have a 95% engagement rate because they are "
            "always clear, concise, and action-oriented. You never send "
            "information dumps - only curated, high-value alerts."
        ),
        tools=[slack_tool],
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=2
    )


# Agent factory function for easy creation
def create_all_agents() -> dict:
    """
    Create all 5 agents and return as a dictionary.
    
    Returns:
        Dictionary with agent names as keys and Agent objects as values
    """
    return {
        "ingestor": create_ingestor_agent(),
        "analyzer": create_analyzer_agent(),
        "prioritizer": create_prioritizer_agent(),
        "retention_critic": create_retention_critic_agent(),
        "deliverer": create_deliverer_agent()
    }
