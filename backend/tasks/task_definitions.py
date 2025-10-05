"""
SURF Customer Feedback Agent - Task Definitions
==============================================
Defines specific tasks for each agent in the pipeline.
"""

from crewai import Task


def create_ingestion_task(agent) -> Task:
    """
    Task 1: Data Ingestion & Standardization
    Agent: IngestorAgent
    """
    return Task(
        description=(
            "Retrieve all raw customer feedback from the PostgreSQL database "
            "using the PostgresTool. Your objectives:\n"
            "1. Use get_all_feedback operation to retrieve all feedback items\n"
            "2. Verify data integrity (non-empty text, valid source)\n"
            "3. Count total items retrieved\n"
            "4. Log a summary of feedback sources (Slack, Email, Notion, etc.)\n"
            "5. Prepare data for the next agent (AnalyzerAgent)\n\n"
            "Expected output: A JSON report containing:\n"
            "- total_items: number of feedback items\n"
            "- sources: list of unique sources\n"
            "- status: 'ready_for_analysis'\n"
            "- sample_items: first 3 items for verification"
        ),
        expected_output=(
            "JSON report with total_items count, unique sources list, "
            "status='ready_for_analysis', and sample of first 3 items"
        ),
        agent=agent
    )


def create_analysis_task(agent, context_task=None) -> Task:
    """
    Task 2: Category & Scoring Analysis
    Agent: AnalyzerAgent
    """
    return Task(
        description=(
            "Analyze all unprocessed feedback and calculate precise scores. "
            "For EACH feedback item:\n\n"
            "1. Read unprocessed feedback using PostgresTool "
            "get_unprocessed_feedback operation\n"
            "2. Categorize into: Bug, Feature, UX, or Other\n"
            "3. Calculate Severity-Volume Score (0.0-10.0 FLOAT) based on:\n"
            "   - Severity factors:\n"
            "     * Security issues: 9-10\n"
            "     * Enterprise customer issues: 7-10\n"
            "     * Performance degradation: 7-9\n"
            "     * Critical bugs: 7-9\n"
            "     * UX problems: 4-6\n"
            "     * Feature requests: 3-8\n"
            "   - Volume factors (from metadata):\n"
            "     * user_tier: Enterprise (+2), Pro (+1), Free (+0)\n"
            "     * urgency: critical (+2), high (+1), medium (+0.5), low (+0)\n"
            "4. Update each item using update_item_score operation\n"
            "5. Log statistics: avg score, highest score, category distribution\n\n"
            "Expected output: Analysis report with:\n"
            "- total_analyzed: count\n"
            "- avg_score: float\n"
            "- category_distribution: {Bug: X, Feature: Y, UX: Z, Other: W}\n"
            "- top_3_scores: list of top scores\n"
            "- status: 'analysis_complete'"
        ),
        expected_output=(
            "Analysis report JSON with total_analyzed, avg_score, "
            "category_distribution, top_3_scores, and status='analysis_complete'"
        ),
        agent=agent,
        context=[context_task] if context_task else None
    )


def create_prioritization_task(agent, context_task=None) -> Task:
    """
    Task 3: Strategic Prioritization
    Agent: PrioritizerAgent
    """
    return Task(
        description=(
            "Select and prioritize the top 3 feedback items. Steps:\n\n"
            "1. Use PostgresTool read_top_items operation (limit=3)\n"
            "2. For EACH of the top 3 items, create an action plan JSON:\n"
            "   {\n"
            "     'feedback_id': int,\n"
            "     'title': 'Clear, concise title (max 100 chars)',\n"
            "     'category': 'Bug/Feature/UX/Other',\n"
            "     'score': float,\n"
            "     'team': 'Engineering/Product/UX/Support',\n"
            "     'action_plan': {\n"
            "       'immediate_action': 'What to do first',\n"
            "       'timeline': 'Estimated completion time',\n"
            "       'success_metric': 'How to measure success',\n"
            "       'dependencies': 'Required resources/teams'\n"
            "     }\n"
            "   }\n"
            "3. Rank items 1-3 by priority\n"
            "4. Pass to RetentionCriticAgent for financial analysis\n\n"
            "Expected output: JSON with:\n"
            "- total_analyzed: total feedback count from previous step\n"
            "- top_3_items: array of 3 prioritized items with action plans\n"
            "- status: 'ready_for_risk_assessment'"
        ),
        expected_output=(
            "JSON containing total_analyzed count, top_3_items array with "
            "detailed action plans, and status='ready_for_risk_assessment'"
        ),
        agent=agent,
        context=[context_task] if context_task else None
    )


def create_risk_assessment_task(agent, context_task=None) -> Task:
    """
    Task 4: Pre-Mortem Financial Risk Assessment
    Agent: RetentionCriticAgent
    """
    return Task(
        description=(
            "Conduct pre-mortem financial analysis on the top 3 items. "
            "For EACH item, answer: What happens if we IGNORE this for 90 days?\n\n"
            "Calculate and document:\n"
            "1. Customer churn risk:\n"
            "   - % of customers likely to churn\n"
            "   - $ ARR loss (use Enterprise=$100K-500K, Pro=$10K-50K)\n"
            "2. Revenue impact from lost new deals\n"
            "3. Support cost increases\n"
            "4. Brand/reputation damage in $$\n\n"
            "For EACH of the top 3 items, add a 'pre_mortem_forecast' field:\n"
            "{\n"
            "  'pre_mortem_forecast': 'STRING with specific $ estimates. Example:\n"
            "    Estimated 90-day impact if ignored:\n"
            "    - Churn: 15-20% of Enterprise customers (~$750K-$1.5M ARR loss)\n"
            "    - Lost deals: 10 prospects, ~$500K pipeline impact\n"
            "    - Support costs: +30% ticket volume, ~$50K additional costs\n"
            "    - Total estimated loss: $1.3M-$2.0M over 90 days'\n"
            "}\n\n"
            "BE SPECIFIC with dollar amounts and percentages. Use conservative "
            "estimates based on issue severity and customer tier.\n\n"
            "Expected output: Enhanced JSON with pre_mortem_forecast added to "
            "each of the top 3 items, plus:\n"
            "- total_risk_estimate: sum of worst-case scenarios\n"
            "- status: 'ready_for_delivery'"
        ),
        expected_output=(
            "Enhanced JSON with pre_mortem_forecast strings containing specific "
            "dollar amounts for each top 3 item, total_risk_estimate, "
            "and status='ready_for_delivery'"
        ),
        agent=agent,
        context=[context_task] if context_task else None
    )


def create_delivery_task(agent, context_task=None) -> Task:
    """
    Task 5: Slack Delivery
    Agent: DelivererAgent
    """
    return Task(
        description=(
            "Deliver the final prioritized feedback report to Slack. Steps:\n\n"
            "1. Take the complete prioritized list from RetentionCriticAgent\n"
            "2. Format as a clean, professional JSON payload:\n"
            "   {\n"
            "     'items': [\n"
            "       {\n"
            "         'rank': 1,\n"
            "         'title': 'Issue title',\n"
            "         'category': 'Bug/Feature/UX',\n"
            "         'score': 8.5,\n"
            "         'team': 'Engineering',\n"
            "         'pre_mortem_forecast': 'Financial risk assessment...',\n"
            "         'action_plan': {...}\n"
            "       }\n"
            "     ],\n"
            "     'total_analyzed': 10,\n"
            "     'total_risk_estimate': '$1.5M-$3M over 90 days',\n"
            "     'generated_at': 'timestamp'\n"
            "   }\n"
            "3. Use PostToSlackTool to send the message\n"
            "4. Verify delivery and log the final payload\n\n"
            "Expected output:\n"
            "- slack_delivery_status: 'success' or 'fallback_logged'\n"
            "- message_preview: first 200 chars of the payload\n"
            "- delivery_timestamp: ISO timestamp\n"
            "- final_payload: the complete JSON sent to Slack"
        ),
        expected_output=(
            "Delivery confirmation JSON with slack_delivery_status, "
            "message_preview, delivery_timestamp, and the complete final_payload"
        ),
        agent=agent,
        context=[context_task] if context_task else None
    )


def create_all_tasks(agents_dict: dict) -> list:
    """
    Create all tasks in sequential order with proper context chaining.
    
    Args:
        agents_dict: Dictionary of agents from create_all_agents()
    
    Returns:
        List of tasks in execution order
    """
    # Create tasks with sequential dependencies
    task1 = create_ingestion_task(agents_dict["ingestor"])
    task2 = create_analysis_task(agents_dict["analyzer"], context_task=task1)
    task3 = create_prioritization_task(
        agents_dict["prioritizer"],
        context_task=task2
    )
    task4 = create_risk_assessment_task(
        agents_dict["retention_critic"],
        context_task=task3
    )
    task5 = create_delivery_task(agents_dict["deliverer"], context_task=task4)
    
    return [task1, task2, task3, task4, task5]
