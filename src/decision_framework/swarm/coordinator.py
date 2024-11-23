"""
Swarm Coordinator for managing agent network and transitions.
This module handles the orchestration of different agents in the decision framework.
"""

from typing import Dict, List, Optional, Any, Set, cast
from dataclasses import dataclass
from swarm import Swarm, Agent

from .swarm_agents import (
    ProblemIdentifierAgent,
    CriteriaEvaluatorAgent,
    CognitiveMonitorAgent,
    Result
)
from .config import get_config

@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    name: str
    max_tokens: int = 16384
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for agent initialization."""
        return {
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty
        }


class SwarmCoordinator:
    """Coordinates the network of agents in the decision framework."""
    
    # Available models and their configurations
    AVAILABLE_MODELS = {
        'gpt-4o-mini': ModelConfig(
            name='gpt-4o-mini',
            max_tokens=16384
        ),
        'gpt-4o': ModelConfig(
            name='gpt-4o',
            max_tokens=16384 
        ),
        'o1-mini': ModelConfig(
            name='o1-mini',
            max_tokens=65536
        )
    }
    
    # Default models for each agent type
    DEFAULT_AGENT_MODELS = {
        'problem_identifier': 'gpt-4o-mini',  # Fast model for initial analysis
        'criteria_evaluator': 'gpt-4o',       # More powerful model for complex evaluation
        'cognitive_monitor': 'o1-mini'        # Reasoning model for bias detection
    }
    
    def __init__(self, agent_models: Optional[Dict[str, str]] = None):
        """
        Initialize the SwarmCoordinator.
        
        Args:
            agent_models: Optional dictionary mapping agent types to specific models.
                        If not provided, DEFAULT_AGENT_MODELS will be used.
        
        Raises:
            ValueError: If an invalid model is specified or if required agent type is missing.
        """
        config = get_config()
        self.client = Swarm(api_key=config.openai_api_key)
        self.config = config
        
        # Validate and merge model configurations
        models = self._validate_and_merge_models(agent_models or {})
        
        # Initialize agents with their specific models
        self.agents = self._initialize_agents(models)
        self.current_agent = self.agents['problem_identifier']
        
        # Set up context variables
        self.context_variables = {
            'environment': config.environment,
            'enable_cognitive_monitoring': config.enable_cognitive_monitoring,
            'agent_models': models  # Store the actual model names
        }
    
    def _validate_and_merge_models(self, custom_models: Dict[str, str]) -> Dict[str, str]:
        """
        Validate custom models and merge with defaults.
        
        Args:
            custom_models: Dictionary of custom model assignments.
        
        Returns:
            Dictionary of validated and merged model assignments.
        
        Raises:
            ValueError: If an invalid model is specified.
        """
        # Check for invalid model names
        invalid_models = set(custom_models.values()) - set(self.AVAILABLE_MODELS.keys())
        if invalid_models:
            raise ValueError(
                f"Invalid models specified: {invalid_models}. "
                f"Available models: {list(self.AVAILABLE_MODELS.keys())}"
            )
        
        # Check for invalid agent types
        invalid_agents = set(custom_models.keys()) - set(self.DEFAULT_AGENT_MODELS.keys())
        if invalid_agents:
            raise ValueError(
                f"Invalid agent types specified: {invalid_agents}. "
                f"Available agents: {list(self.DEFAULT_AGENT_MODELS.keys())}"
            )
        
        # Merge with defaults
        return {**self.DEFAULT_AGENT_MODELS, **custom_models}
    
    def _initialize_agents(self, models: Dict[str, str]) -> Dict[str, Agent]:
        """
        Initialize agents with their specified models.
        
        Args:
            models: Dictionary mapping agent types to model names.
        
        Returns:
            Dictionary of initialized agents.
        """
        return {
            'problem_identifier': ProblemIdentifierAgent(
                model=models['problem_identifier'],
                **self.AVAILABLE_MODELS[models['problem_identifier']].to_dict()
            ),
            'criteria_evaluator': CriteriaEvaluatorAgent(
                model=models['criteria_evaluator'],
                **self.AVAILABLE_MODELS[models['criteria_evaluator']].to_dict()
            ),
            'cognitive_monitor': CognitiveMonitorAgent(
                model=models['cognitive_monitor'],
                **self.AVAILABLE_MODELS[models['cognitive_monitor']].to_dict()
            )
        }
    
    def _determine_next_step(self, result: Result) -> str:
        """
        Determine the next step based on the result.
        
        Args:
            result: Result object containing the response and context.
        
        Returns:
            String indicating the next step to take.
        """
        # Cast the value to str since we know it will be a string
        return cast(str, result.value)
    
    def handle_agent_transition(self, result: Result) -> Optional[Agent]:
        """Handle transition between agents based on the result."""
        next_step = self._determine_next_step(result)
        
        # Determine next agent based on current state
        current_step = self.context_variables.get('current_step', 'problem_identification')
        if next_step in self.agents:
            return self.agents[next_step]
        return None
    
    def start_decision_cycle(self, problem_statement: str) -> Result:
        """Start a new decision cycle with the problem identifier agent."""
        messages = [{
            "role": "user",
            "content": f"Analyze this problem: {problem_statement}"
        }]
        
        return self.client.run(
            agent=self.current_agent,
            messages=messages,
            context_variables=self.context_variables
        )
    
    def run_cognitive_check(self) -> Result:
        """Run a cognitive bias check using the cognitive monitor agent."""
        messages = [{
            "role": "user",
            "content": "Perform a cognitive bias check on the current decision process."
        }]
        
        return self.client.run(
            agent=self.agents['cognitive_monitor'],
            messages=messages,
            context_variables=self.context_variables
        )
    
    def evaluate_criteria(self, criteria: List[Dict[str, Any]]) -> Result:
        """Evaluate decision criteria using the criteria evaluator agent."""
        messages = [{
            "role": "user",
            "content": f"Evaluate these criteria: {criteria}"
        }]
        
        return self.client.run(
            agent=self.agents['criteria_evaluator'],
            messages=messages,
            context_variables=self.context_variables
        )

    @property
    def current_model_config(self) -> ModelConfig:
        """Get the configuration for the current agent's model."""
        agent_type = next(
            name for name, agent in self.agents.items() 
            if agent == self.current_agent
        )
        model_name = self.context_variables['agent_models'][agent_type]
        return self.AVAILABLE_MODELS[model_name]
