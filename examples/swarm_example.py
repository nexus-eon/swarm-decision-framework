"""
Example usage of the Swarm-integrated Decision Framework.
This example demonstrates how to use the framework for a simple decision-making process.
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from src.decision_framework.config import get_config
from src.decision_framework.swarm_coordinator import SwarmCoordinator
from src.decision_framework.problem_solving_cycle import (
    DecisionCriteria,
    CriteriaCategory
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Load configuration
    try:
        config = get_config()
        logger.info(f"Running in {config.environment} environment")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    
    # Example of customizing models per agent
    custom_models = {
        'problem_identifier': 'gpt-4o-mini',  # Fast model for initial analysis
        'criteria_evaluator': 'gpt-4o-mini',  # Fast model for criteria evaluation
        'cognitive_monitor': 'gpt-4o-mini'    # Fast model for bias detection
    }
    
    # Initialize the coordinator with custom models
    coordinator = SwarmCoordinator(agent_models=custom_models)
    logger.info("Initialized SwarmCoordinator with custom models")
    
    # Start with a problem statement
    problem_statement = """
    Our software development team needs to choose between two competing cloud providers
    for our new microservices architecture. We need to consider costs, scalability,
    vendor lock-in, and team expertise.
    """
    
    logger.info("Starting decision cycle...")
    logger.info("\nStep 1: Problem Analysis")
    
    try:
        # Start the decision cycle
        response = coordinator.start_decision_cycle(problem_statement)
        logger.info(f"Problem analysis complete: {response.value}")
        
        logger.info("\nStep 2: Criteria Evaluation")
        # Define some criteria
        criteria = [
            {
                "name": "cost_efficiency",
                "description": "Total cost of ownership over 2 years",
                "weight": 0.3,
                "category": "FINANCIAL",
                "measurement_method": "Dollar amount",
                "threshold": 100000.0
            },
            {
                "name": "scalability",
                "description": "Ability to handle increased load",
                "weight": 0.25,
                "category": "TECHNICAL",
                "measurement_method": "Response time under load",
                "threshold": 200.0
            }
        ]
        
        # Evaluate criteria
        response = coordinator.evaluate_criteria(criteria)
        logger.info(f"Criteria evaluation complete: {response.value}")
        
        if config.enable_cognitive_monitoring:
            logger.info("\nStep 3: Cognitive Check")
            # Run a cognitive bias check
            response = coordinator.run_cognitive_check()
            logger.info(f"Cognitive check complete: {response.value}")
        
        # Handle transition
        next_agent = coordinator.handle_agent_transition(response)
        if next_agent:
            logger.info(f"\nTransitioning to next agent: {next_agent.name}")
        
        logger.info("\nDecision cycle complete!")
        logger.info("\nContext Variables:")
        for key, value in coordinator.context_variables.items():
            logger.info(f"- {key}: {value}")
            
    except Exception as e:
        logger.error(f"Error during decision cycle: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
