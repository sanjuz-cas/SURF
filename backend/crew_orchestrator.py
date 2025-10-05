"""
SURF Customer Feedback Agent - Crew Orchestrator
================================================
Orchestrates the sequential execution of the 5-agent pipeline.
"""

import logging
from crewai import Crew, Process
from backend.agents import create_all_agents
from backend.tasks.task_definitions import create_all_tasks

logger = logging.getLogger(__name__)


class FeedbackCrew:
    """
    Orchestrates the SURF Customer Feedback Agent pipeline.
    Manages the sequential execution of 5 agents.
    """
    
    def __init__(self):
        """Initialize the crew with agents and tasks."""
        logger.info("🚀 Initializing SURF Feedback Crew...")
        
        # Create all agents
        self.agents = create_all_agents()
        logger.info(f"✅ Created {len(self.agents)} agents")
        
        # Create all tasks with proper sequencing
        self.tasks = create_all_tasks(self.agents)
        logger.info(f"✅ Created {len(self.tasks)} tasks")
        
        # Create the crew with sequential process
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            process=Process.sequential,  # Sequential execution is critical
            verbose=True,
            full_output=True
        )
        logger.info("✅ Crew assembled and ready for execution")
    
    def execute(self) -> dict:
        """
        Execute the complete feedback processing pipeline.
        
        Returns:
            dict: Results from the crew execution
        """
        logger.info("="*70)
        logger.info("🎯 STARTING SURF CUSTOMER FEEDBACK AGENT PIPELINE")
        logger.info("="*70)
        
        try:
            # Execute the crew
            result = self.crew.kickoff()
            
            logger.info("="*70)
            logger.info("✅ PIPELINE EXECUTION COMPLETE")
            logger.info("="*70)
            
            return {
                "success": True,
                "result": result,
                "message": "Feedback processing pipeline completed successfully"
            }
            
        except Exception as e:
            logger.error(f"❌ Pipeline execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Pipeline execution encountered an error"
            }
    
    def get_agent_info(self) -> dict:
        """
        Get information about all agents in the crew.
        
        Returns:
            dict: Agent information
        """
        return {
            agent_name: {
                "role": agent.role,
                "goal": agent.goal,
                "tools": [tool.name for tool in agent.tools] if agent.tools else []
            }
            for agent_name, agent in self.agents.items()
        }
    
    def get_task_info(self) -> list:
        """
        Get information about all tasks in the crew.
        
        Returns:
            list: Task information
        """
        return [
            {
                "description": task.description[:100] + "...",
                "agent": task.agent.role,
                "has_context": task.context is not None
            }
            for task in self.tasks
        ]


def create_and_run_crew() -> dict:
    """
    Convenience function to create and run the crew.
    
    Returns:
        dict: Execution results
    """
    crew = FeedbackCrew()
    return crew.execute()
