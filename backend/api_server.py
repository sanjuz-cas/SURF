"""
FastAPI server for SURF feedback prioritization system.
Provides REST API endpoints for the frontend dashboard.
"""
import os
from typing import List, Dict, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="SURF Feedback API", version="1.0.0")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "surf_feedback_db"),
    "user": os.getenv("DB_USER", "surf_user"),
    "password": os.getenv("DB_PASSWORD", "surf_password_2024"),
}


def get_db_connection():
    """Create database connection."""
    try:
        conn = psycopg.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "SURF Feedback API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/priorities")
async def get_priorities() -> Dict[str, Any]:
    """
    Get prioritized feedback from the database.
    
    Returns:
        JSON response with prioritized items and action plans
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query prioritized output with raw feedback
        cursor.execute("""
            SELECT 
                po.id,
                po.title,
                po.priority_rank,
                rf.category,
                po.score,
                rf.severity_volume_score,
                0 as effort_score,
                po.pre_mortem_forecast,
                po.action_plan,
                po.created_at,
                rf.raw_text,
                po.team
            FROM prioritized_output po
            LEFT JOIN raw_feedback rf ON po.feedback_id = rf.id
            ORDER BY po.priority_rank ASC, po.score DESC
            LIMIT 100
        """)
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Transform to frontend format
        items = []
        for row in rows:
            item = {
                "id": row[0],
                "rank": row[2] if row[2] else 999,  # priority_rank
                "title": row[1] if row[1] else "Untitled Feedback",  # po.title
                "category": row[3] if row[3] else "General",
                "score": float(row[4]) if row[4] else 0.0,  # score
                "team": row[11] if row[11] else "Engineering",  # po.team
                "preMortemForecast": row[7] if row[7] else "No forecast available",  # pre_mortem_forecast
                "action_plan": {
                    "immediate_steps": row[8].get("immediate_steps", []) if isinstance(row[8], dict) else [],
                    "medium_term_steps": row[8].get("medium_term_steps", []) if isinstance(row[8], dict) else [],
                    "long_term_steps": row[8].get("long_term_steps", []) if isinstance(row[8], dict) else [],
                    "estimated_timeline": "2-4 weeks",
                    "required_resources": "Engineering team"
                },
                "raw_text": row[10],  # rf.raw_text
                "created_at": row[9].isoformat() if row[9] else None
            }
            items.append(item)
        
        return {
            "items": items,
            "total_analyzed": len(items),
            "total_risk_estimate": "$150K in potential revenue at risk",
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch priorities: {str(e)}")


@app.get("/api/stats")
async def get_stats() -> Dict[str, Any]:
    """
    Get statistics about feedback processing.
    
    Returns:
        JSON with counts by priority, category, etc.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get counts by priority rank
        cursor.execute("""
            SELECT priority_rank, COUNT(*) as count
            FROM prioritized_output
            GROUP BY priority_rank
            ORDER BY priority_rank ASC
        """)
        priority_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Get counts by category from raw_feedback
        cursor.execute("""
            SELECT rf.category, COUNT(*) as count
            FROM prioritized_output po
            LEFT JOIN raw_feedback rf ON po.feedback_id = rf.id
            GROUP BY rf.category
            ORDER BY count DESC
        """)
        category_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Get total raw feedback
        cursor.execute("SELECT COUNT(*) FROM raw_feedback")
        total_raw = cursor.fetchone()[0]
        
        # Get total processed
        cursor.execute("SELECT COUNT(*) FROM prioritized_output")
        total_processed = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return {
            "total_raw_feedback": total_raw,
            "total_processed": total_processed,
            "by_priority": priority_counts,
            "by_category": category_counts,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("Starting SURF Feedback API server...")
    print(f"Database: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")
    print("API will be available at http://localhost:8000")
    print("Docs at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
