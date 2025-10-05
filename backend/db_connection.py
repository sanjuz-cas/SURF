"""
SURF Customer Feedback Agent - Database Connection Module (Mock)
================================================================
Mock database module for testing without PostgreSQL.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeedbackDatabase:
    """Mock database for testing."""
    
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")
        self.database = os.getenv("DB_NAME", "surf_feedback_db")
        self.user = os.getenv("DB_USER", "surf_user")
        self.password = os.getenv("DB_PASSWORD", "")
        self._conn = None
        logger.info("✅ Mock database initialized")
    
    def connect(self):
        """Mock connect."""
        self._conn = True
        logger.info("✅ Mock database connected")
        return True
    
    def disconnect(self):
        """Mock disconnect."""
        self._conn = None
        logger.info("Database disconnected")
    
    @contextmanager
    def get_cursor(self):
        """Mock cursor."""
        yield None
    
    def get_unprocessed_feedback(self, limit: int = 10):
        """Mock get feedback."""
        return []
    
    def update_priority_score(self, feedback_id, category, score):
        """Mock update."""
        return True
    
    def save_prioritized_output(self, *args, **kwargs):
        """Mock save."""
        return True
    
    def get_top_priorities(self, limit: int = 10):
        """Mock priorities."""
        return []


DatabaseConnection = FeedbackDatabase
