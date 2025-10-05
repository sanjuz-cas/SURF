"""
SURF Customer Feedback Agent - PostgreSQL Tool
==============================================
Custom CrewAI tool for database operations.
"""

from typing import Type, List, Dict, Any
from pydantic import BaseModel, Field
try:
    from crewai_tools import BaseTool
except ImportError:
    # Fallback for newer CrewAI versions
    from crewai.tools import BaseTool
import logging

from backend.db_connection import FeedbackDatabase

logger = logging.getLogger(__name__)


class ReadTopItemsInput(BaseModel):
    """Input schema for read_top_items."""
    limit: int = Field(
        default=3,
        description="Number of top items to retrieve"
    )


class UpdateItemScoreInput(BaseModel):
    """Input schema for update_item_score."""
    feedback_id: int = Field(
        description="The ID of the feedback item to update"
    )
    category: str = Field(
        description="Category: Bug, Feature, UX, or Other"
    )
    score: float = Field(
        description="Severity-Volume score (0.0 to 10.0)"
    )


class GetUnprocessedFeedbackInput(BaseModel):
    """Input schema for get_unprocessed_feedback."""
    limit: int = Field(
        default=10,
        description="Number of unprocessed items to retrieve"
    )


class PostgresTool(BaseTool):
    """
    Custom CrewAI tool for PostgreSQL database operations.
    Provides methods to read and update feedback data.
    """
    
    name: str = "PostgreSQL Database Tool"
    description: str = (
        "A tool for interacting with the PostgreSQL database. "
        "Use this to read top prioritized items, update feedback scores, "
        "and retrieve unprocessed feedback. "
        "Operations: read_top_items(limit=3), "
        "update_item_score(feedback_id, category, score), "
        "get_unprocessed_feedback(limit=10)"
    )
    
    def _run(self, operation: str, **kwargs) -> str:
        """
        Execute database operations.
        
        Args:
            operation: The operation to perform
            **kwargs: Operation-specific parameters
        
        Returns:
            JSON string with operation results
        """
        try:
            if operation == "read_top_items":
                return self._read_top_items(kwargs.get("limit", 3))
            elif operation == "update_item_score":
                return self._update_item_score(
                    kwargs.get("feedback_id"),
                    kwargs.get("category"),
                    kwargs.get("score")
                )
            elif operation == "get_unprocessed_feedback":
                return self._get_unprocessed_feedback(
                    kwargs.get("limit", 10)
                )
            elif operation == "get_all_feedback":
                return self._get_all_feedback()
            else:
                return f"Unknown operation: {operation}"
        except Exception as e:
            logger.error(f"PostgresTool error: {e}")
            return f"Error: {str(e)}"
    
    def _read_top_items(self, limit: int = 3) -> str:
        """
        Read top feedback items by score.
        
        Args:
            limit: Number of items to retrieve (default: 3)
        
        Returns:
            JSON string with top items
        """
        try:
            items = FeedbackDatabase.get_top_feedback(limit=limit)
            logger.info(f"🔝 Retrieved {len(items)} top items")
            
            result = {
                "success": True,
                "count": len(items),
                "items": items
            }
            
            import json
            return json.dumps(result, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error reading top items: {e}")
            return f'{{"success": false, "error": "{str(e)}"}}'
    
    def _update_item_score(
        self,
        feedback_id: int,
        category: str,
        score: float
    ) -> str:
        """
        Update feedback item with category and score.
        
        Args:
            feedback_id: ID of the feedback item
            category: Category (Bug/Feature/UX/Other)
            score: Severity-Volume score
        
        Returns:
            JSON string with update status
        """
        try:
            FeedbackDatabase.update_feedback_analysis(
                feedback_id=feedback_id,
                category=category,
                score=score,
                processed=True
            )
            
            result = {
                "success": True,
                "feedback_id": feedback_id,
                "category": category,
                "score": score,
                "message": f"Updated feedback {feedback_id} successfully"
            }
            
            import json
            return json.dumps(result, indent=2)
        except Exception as e:
            logger.error(f"Error updating item score: {e}")
            return f'{{"success": false, "error": "{str(e)}"}}'
    
    def _get_unprocessed_feedback(self, limit: int = 10) -> str:
        """
        Get unprocessed feedback items.
        
        Args:
            limit: Number of items to retrieve
        
        Returns:
            JSON string with unprocessed items
        """
        try:
            items = FeedbackDatabase.get_unprocessed_feedback(limit=limit)
            
            result = {
                "success": True,
                "count": len(items),
                "items": items
            }
            
            import json
            return json.dumps(result, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error getting unprocessed feedback: {e}")
            return f'{{"success": false, "error": "{str(e)}"}}'
    
    def _get_all_feedback(self) -> str:
        """
        Get all raw feedback from database.
        
        Returns:
            JSON string with all feedback items
        """
        try:
            items = FeedbackDatabase.get_all_raw_feedback()
            
            result = {
                "success": True,
                "count": len(items),
                "items": items
            }
            
            import json
            return json.dumps(result, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error getting all feedback: {e}")
            return f'{{"success": false, "error": "{str(e)}"}}'


# Create singleton instance for easy import
postgres_tool = PostgresTool()
