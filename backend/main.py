"""
SURF Customer Feedback Agent - Main Execution Script
===================================================
Entry point for running the complete 5-agent feedback processing pipeline.

Usage:
    python backend/main.py
    
    # Or with custom configuration:
    python backend/main.py --verbose --log-level DEBUG
"""

import os
import sys
import logging
import argparse
from datetime import datetime
from dotenv import load_dotenv
import json

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.crew_orchestrator import FeedbackCrew
from backend.db_connection import DatabaseConnection

# Load environment variables
load_dotenv()


def setup_logging(log_level: str = "INFO"):
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                f'logs/surf_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
            )
        ]
    )


def check_environment() -> bool:
    """
    Check that all required environment variables are set.
    
    Returns:
        bool: True if environment is properly configured
    """
    logger = logging.getLogger(__name__)
    
    required_vars = [
        "OPENAI_API_KEY",
        "DB_HOST",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error("❌ Missing required environment variables:")
        for var in missing_vars:
            logger.error(f"   - {var}")
        logger.error("\n💡 Copy .env.example to .env and configure your values")
        return False
    
    logger.info("✅ Environment configuration validated")
    return True


def display_banner():
    """Display the SURF banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   🌊 SURF - Customer Feedback Agent                          ║
    ║   Strategic User Retention & Feedback                        ║
    ║                                                               ║
    ║   5-Agent Pipeline:                                          ║
    ║   1. IngestorAgent      → Data Unification                   ║
    ║   2. AnalyzerAgent      → Category & Scoring                 ║
    ║   3. PrioritizerAgent   → Strategic Planning                 ║
    ║   4. RetentionCritic    → Financial Risk Assessment          ║
    ║   5. DelivererAgent     → Slack Delivery                     ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main execution function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="SURF Customer Feedback Agent Pipeline"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set logging level"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show configuration without executing"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    os.makedirs("logs", exist_ok=True)
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Display banner
    display_banner()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Initialize database connection
    try:
        DatabaseConnection.initialize_pool()
        logger.info("✅ Database connection pool initialized")
    except Exception as e:
        logger.error(f"❌ Failed to connect to database: {e}")
        logger.error("💡 Check your database credentials in .env file")
        sys.exit(1)
    
    if args.dry_run:
        logger.info("🔍 DRY RUN MODE - Configuration validated")
        crew = FeedbackCrew()
        logger.info("\n📋 Agent Information:")
        for name, info in crew.get_agent_info().items():
            logger.info(f"   {name}: {info['role']}")
        logger.info("\n📋 Task Information:")
        for idx, task_info in enumerate(crew.get_task_info(), 1):
            logger.info(f"   Task {idx}: {task_info['agent']}")
        sys.exit(0)
    
    # Execute the pipeline
    try:
        logger.info("🚀 Initializing SURF Feedback Crew...")
        crew = FeedbackCrew()
        
        logger.info("▶️  Starting pipeline execution...")
        start_time = datetime.now()
        
        result = crew.execute()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Log results
        logger.info("\n" + "="*70)
        logger.info("📊 EXECUTION SUMMARY")
        logger.info("="*70)
        logger.info(f"Status: {'✅ SUCCESS' if result['success'] else '❌ FAILED'}")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Timestamp: {end_time.isoformat()}")
        
        if result['success']:
            logger.info("\n📦 Final Output:")
            logger.info(json.dumps(result.get('result', {}), indent=2, default=str))
            
            logger.info("\n✅ Pipeline executed successfully!")
            logger.info("📨 Check Slack for the prioritized feedback report")
        else:
            logger.error(f"\n❌ Pipeline failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Pipeline interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Cleanup
        try:
            DatabaseConnection.close_pool()
            logger.info("🔒 Database connection pool closed")
        except Exception as e:
            logger.warning(f"⚠️  Error closing database pool: {e}")


if __name__ == "__main__":
    main()