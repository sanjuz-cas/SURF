"""
SURF Customer Feedback Agent - Slack Integration Tool
====================================================
Custom CrewAI tool for posting to Slack.
"""

import os
import json
import logging
from typing import Dict, Any
from pydantic import BaseModel, Field
try:
    from crewai_tools import BaseTool
except ImportError:
    # Fallback for newer CrewAI versions
    from crewai.tools import BaseTool
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

logger = logging.getLogger(__name__)


class PostToSlackInput(BaseModel):
    """Input schema for post_to_slack."""
    message: str = Field(
        description="The message to post to Slack (JSON or plain text)"
    )
    channel: str = Field(
        default="#customer-feedback",
        description="Slack channel to post to"
    )


class PostToSlackTool(BaseTool):
    """
    Custom CrewAI tool for posting messages to Slack.
    Supports both webhook and bot token methods.
    """
    
    name: str = "Post to Slack Tool"
    description: str = (
        "A tool for posting messages to Slack channels. "
        "Use this to deliver the final prioritized feedback list "
        "to the team. Accepts formatted JSON or plain text messages. "
        "Usage: post_message(message, channel='#customer-feedback')"
    )
    
    def _run(self, message: str, channel: str = "#customer-feedback") -> str:
        """
        Post a message to Slack.
        
        Args:
            message: Message content (JSON or text)
            channel: Slack channel (default: #customer-feedback)
        
        Returns:
            JSON string with post status
        """
        try:
            # Try webhook method first
            webhook_url = os.getenv("SLACK_WEBHOOK_URL")
            if webhook_url:
                return self._post_via_webhook(message, webhook_url)
            
            # Fall back to bot token method
            bot_token = os.getenv("SLACK_BOT_TOKEN")
            if bot_token:
                return self._post_via_bot(message, channel, bot_token)
            
            # No credentials configured
            logger.warning("⚠️ No Slack credentials found. Logging locally.")
            return self._log_locally(message, channel)
            
        except Exception as e:
            logger.error(f"Error posting to Slack: {e}")
            return json.dumps({
                "success": False,
                "error": str(e),
                "fallback": "Message logged locally"
            }, indent=2)
    
    def _post_via_webhook(self, message: str, webhook_url: str) -> str:
        """Post message using Slack webhook."""
        try:
            # Format message for Slack
            payload = self._format_message(message)
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ Message posted to Slack via webhook")
                return json.dumps({
                    "success": True,
                    "method": "webhook",
                    "message": "Posted to Slack successfully"
                }, indent=2)
            else:
                logger.error(f"Slack webhook error: {response.text}")
                return self._log_locally(message, "webhook-fallback")
                
        except Exception as e:
            logger.error(f"Webhook post error: {e}")
            return self._log_locally(message, "webhook-fallback")
    
    def _post_via_bot(
        self,
        message: str,
        channel: str,
        bot_token: str
    ) -> str:
        """Post message using Slack bot token."""
        try:
            client = WebClient(token=bot_token)
            
            # Format message
            payload = self._format_message(message)
            
            response = client.chat_postMessage(
                channel=channel,
                text=payload.get("text", message),
                blocks=payload.get("blocks", None)
            )
            
            logger.info(f"✅ Message posted to Slack channel: {channel}")
            return json.dumps({
                "success": True,
                "method": "bot_token",
                "channel": channel,
                "timestamp": response.get("ts", "")
            }, indent=2)
            
        except SlackApiError as e:
            logger.error(f"Slack API error: {e.response['error']}")
            return self._log_locally(message, channel)
    
    def _format_message(self, message: str) -> Dict[str, Any]:
        """
        Format message for Slack with rich formatting.
        
        Args:
            message: Raw message (JSON or text)
        
        Returns:
            Formatted Slack payload
        """
        try:
            # Try to parse as JSON
            data = json.loads(message) if isinstance(message, str) else message
            
            if isinstance(data, dict):
                return self._create_rich_message(data)
            else:
                return {"text": str(message)}
        except json.JSONDecodeError:
            # Plain text message
            return {"text": message}
    
    def _create_rich_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create rich formatted Slack message with blocks."""
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 SURF: Top Priority Customer Feedback",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            }
        ]
        
        # Add feedback items
        items = data.get("items", [])
        for idx, item in enumerate(items, 1):
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*#{idx} - {item.get('title', 'No title')}*\n"
                        f"*Category:* {item.get('category', 'N/A')} | "
                        f"*Score:* {item.get('score', 0):.2f}\n"
                        f"*Team:* {item.get('team', 'Unassigned')}\n\n"
                        f"*💰 Financial Risk:*\n"
                        f"{item.get('pre_mortem_forecast', 'N/A')}\n\n"
                        f"*📋 Action Plan:*\n"
                        f"{self._format_action_plan(item.get('action_plan', {}))}"
                    )
                }
            })
            blocks.append({"type": "divider"})
        
        # Add footer
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": (
                        f"Generated by SURF Customer Feedback Agent | "
                        f"Total items analyzed: {data.get('total_analyzed', 0)}"
                    )
                }
            ]
        })
        
        return {
            "text": "SURF: Top Priority Customer Feedback",
            "blocks": blocks
        }
    
    def _format_action_plan(self, action_plan: Dict[str, Any]) -> str:
        """Format action plan for display."""
        if not action_plan:
            return "_No action plan available_"
        
        formatted = []
        for key, value in action_plan.items():
            formatted.append(f"• {key}: {value}")
        
        return "\n".join(formatted) if formatted else "_No action plan_"
    
    def _log_locally(self, message: str, channel: str) -> str:
        """
        Fallback: Log message locally when Slack is unavailable.
        
        Args:
            message: Message to log
            channel: Target channel
        
        Returns:
            JSON status
        """
        logger.info("="*60)
        logger.info(f"📢 SLACK MESSAGE (Channel: {channel})")
        logger.info("="*60)
        logger.info(message)
        logger.info("="*60)
        
        return json.dumps({
            "success": True,
            "method": "local_logging",
            "channel": channel,
            "message": "Logged locally (Slack unavailable)"
        }, indent=2)


# Create singleton instance for easy import
slack_tool = PostToSlackTool()
