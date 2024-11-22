from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum, unique
from typing import Dict, List, Optional, Any, Union, Tuple, TypeVar
from uuid import uuid4, UUID
from pathlib import Path
import json
import logging
from collections import Counter

T = TypeVar('T', bound=Union[Any])

@unique
class Status(str, Enum):
    """Represents the current state of a task or process in the decision framework.
    
    Values:
        NOT_STARTED: Task has not been initiated
        IN_PROGRESS: Task is currently being worked on
        COMPLETED: Task has been successfully finished
        BLOCKED: Task cannot proceed due to dependencies or issues
        CANCELLED: Task has been terminated before completion
    """
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

@unique
class RiskLevel(str, Enum):
    """Represents the level of risk associated with a decision or alternative.
    
    Values:
        LOW: Minimal risk with limited potential negative impact
        MEDIUM: Moderate risk requiring careful consideration
        HIGH: Significant risk requiring thorough analysis and mitigation strategies
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@unique
class CriteriaCategory(str, Enum):
    """Categorizes decision criteria into different domains of impact.
    
    Values:
        FINANCIAL: Economic and monetary considerations
        TECHNICAL: Technology and implementation aspects
        OPERATIONAL: Day-to-day functioning and processes
        STRATEGIC: Long-term goals and organizational alignment
        SOCIAL: Impact on people and relationships
        ENVIRONMENTAL: Impact on environment and sustainability
    """
    FINANCIAL = "financial"
    TECHNICAL = "technical"
    OPERATIONAL = "operational"
    STRATEGIC = "strategic"
    SOCIAL = "social"
    ENVIRONMENTAL = "environmental"

@unique
class SourceType(str, Enum):
    """Classifies the type of information source used in decision making.
    
    Values:
        DOCUMENT: Written materials like reports or documentation
        INTERVIEW: Information gathered through conversations
        DATA: Quantitative or qualitative datasets
        OBSERVATION: Direct observations or field studies
        ANALYSIS: Results from data analysis or research
        EXPERT_OPINION: Input from subject matter experts
    """
    DOCUMENT = "document"
    INTERVIEW = "interview"
    DATA = "data"
    OBSERVATION = "observation"
    ANALYSIS = "analysis"
    EXPERT_OPINION = "expert_opinion"

@unique
class VerificationStatus(str, Enum):
    """Indicates the verification state of information sources.
    
    Values:
        UNVERIFIED: Information has not been validated
        VERIFIED: Information has been confirmed as accurate
        DISPUTED: Information accuracy is contested
        PENDING: Verification is in progress
    """
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    DISPUTED = "disputed"
    PENDING = "pending"

@unique
class GenerationTechnique(str, Enum):
    """Describes methods used to generate decision alternatives.
    
    Values:
        BRAINSTORMING: Collaborative idea generation
        ANALYSIS: Systematic breakdown and examination
        ANALOGIES: Drawing parallels with similar situations
        MORPHOLOGICAL: Systematic exploration of solution space
        DELPHI: Structured communication technique
        SCENARIO: Future-oriented alternative generation
    """
    BRAINSTORMING = "brainstorming"
    ANALYSIS = "analysis"
    ANALOGIES = "analogies"
    MORPHOLOGICAL = "morphological"
    DELPHI = "delphi"
    SCENARIO = "scenario"

@unique
class CognitiveState(str, Enum):
    """Represents the mental state during decision making.
    
    Values:
        CLEAR: Focused and rational thinking
        OVERLOADED: Experiencing cognitive burden
        UNCERTAIN: Lack of confidence or clarity
        BIASED: Potentially influenced by cognitive biases
        REFLECTIVE: Engaged in metacognitive thinking
    """
    CLEAR = "clear"
    OVERLOADED = "overloaded"
    UNCERTAIN = "uncertain"
    BIASED = "biased"
    REFLECTIVE = "reflective"

@unique
class DiscussionType(str, Enum):
    """Categorizes different types of decision-related discussions.
    
    Values:
        DEBATE: Structured argument of different viewpoints
        BRAINSTORMING: Creative idea generation session
        FEEDBACK: Review and input gathering
        REFLECTION: Thoughtful consideration of process/outcomes
        DECISION: Final decision-making discussion
    """
    DEBATE = "debate"
    BRAINSTORMING = "brainstorming"
    FEEDBACK = "feedback"
    REFLECTION = "reflection"
    DECISION = "decision"

@unique
class DiscussionStatus(str, Enum):
    """Indicates the current state of a discussion.
    
    Values:
        OPEN: Discussion is active and ongoing
        CLOSED: Discussion has been concluded
    """
    OPEN = "open"
    CLOSED = "closed"

@unique
class ProblemCategory(str, Enum):
    """Classifies the type and scope of the problem being addressed.
    
    Values:
        STRATEGIC: Long-term organizational direction issues
        OPERATIONAL: Day-to-day process and efficiency issues
        TECHNICAL: Technology and system-related problems
        RESOURCE: Resource allocation and management issues
        HUMAN: People and relationship-focused problems
        COMPLIANCE: Regulatory and policy-related issues
    """
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    TECHNICAL = "technical"
    RESOURCE = "resource"
    HUMAN = "human"
    COMPLIANCE = "compliance"

class DecisionFrameworkError(Exception):
    """Base exception class for all decision framework related errors."""
    pass

class ValidationError(DecisionFrameworkError):
    """Raised when validation fails for a decision framework component."""
    pass

@dataclass
class DecisionCriteria:
    """Represents a criterion used to evaluate decision alternatives.
    
    Attributes:
        name: Unique identifier for the criterion
        description: Detailed explanation of what this criterion measures
        weight: Importance weight (0.0 to 1.0) used in scoring
        category: Domain category this criterion belongs to
        measurement_method: How this criterion should be measured/evaluated
        threshold: Optional minimum acceptable value for this criterion
    """
    name: str
    description: str
    weight: float
    category: CriteriaCategory
    measurement_method: str
    threshold: Optional[float] = None
    
    def __post_init__(self) -> None:
        """Validate the criterion attributes after initialization."""
        if not self.name:
            raise ValidationError("Criterion name cannot be empty")
        if not self.description:
            raise ValidationError("Criterion description cannot be empty")
        if not self.validate_weight():
            raise ValidationError(f"Weight {self.weight} must be between 0.0 and 1.0")
        if self.threshold is not None and self.threshold < 0:
            raise ValidationError(f"Threshold {self.threshold} cannot be negative")
    
    def validate_weight(self) -> bool:
        """Check if the weight is within valid range (0.0 to 1.0)."""
        return 0.0 <= self.weight <= 1.0
    
    def validate_score(self, score: float) -> bool:
        """Check if a score meets the threshold requirement if one exists.
        
        Args:
            score: The score to validate
            
        Returns:
            bool: True if score is valid, False otherwise
        """
        if self.threshold is not None:
            return score >= self.threshold
        return True

@dataclass
class AlternativeEvaluation:
    """Represents an evaluation of a decision alternative against criteria.
    
    Attributes:
        alternative: The alternative being evaluated
        criteria_scores: Raw scores for each criterion
        evaluation_notes: List of notes about the evaluation
        evaluator: Person/entity performing the evaluation
        weighted_scores: Scores adjusted by criteria weights (calculated automatically)
        total_score: Overall evaluation score (calculated automatically)
        timestamp: When the evaluation was performed
    """
    alternative: 'Alternative'
    criteria_scores: Dict[str, float]  # criteria_name -> score
    evaluation_notes: List[str]
    evaluator: str
    weighted_scores: Dict[str, float] = field(default_factory=dict)  # criteria_name -> weighted_score
    total_score: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """Validate the evaluation after initialization."""
        if not self.evaluator:
            raise ValidationError("Evaluator cannot be empty")
        for criterion, score in self.criteria_scores.items():
            if score < 0:
                raise ValidationError(f"Score for criterion '{criterion}' cannot be negative")
        
        # Initialize weighted scores with same values as raw scores
        # These will be properly calculated when recalculate_scores is called
        self.weighted_scores = dict(self.criteria_scores)
        self.total_score = sum(self.criteria_scores.values())

    def recalculate_scores(self, criteria: Dict[str, DecisionCriteria]) -> None:
        """Recalculate weighted scores and total score based on criteria weights.
        
        Args:
            criteria: Dictionary mapping criterion names to DecisionCriteria objects
        
        Raises:
            ValidationError: If a criterion is missing or invalid
        """
        self.weighted_scores = {}
        total = 0.0
        
        for name, score in self.criteria_scores.items():
            if name not in criteria:
                raise ValidationError(f"No criterion found with name '{name}'")
            weight = criteria[name].weight
            weighted_score = score * weight
            self.weighted_scores[name] = weighted_score
            total += weighted_score
        
        self.total_score = total

@dataclass
class DecisionOutcome:
    decision_id: str
    implementation_date: datetime
    success_metrics: Dict[str, float]
    actual_outcomes: Dict[str, Any]
    lessons_learned: List[str] = field(default_factory=list)
    follow_up_actions: List[str] = field(default_factory=list)
    
    def calculate_success_rate(self) -> float:
        """Calculate the overall success rate based on metrics"""
        if not self.success_metrics:
            return 0.0
        return sum(self.success_metrics.values()) / len(self.success_metrics)

@dataclass
class Alternative:
    """Represents a potential solution alternative with its attributes and evaluation metrics."""
    name: str
    description: str
    attributes: Dict[str, Any]
    alternative_id: str = field(default_factory=lambda: str(uuid4()))
    evaluation_scores: Dict[str, float] = field(default_factory=dict)
    implementation_plan: Optional[List['ImplementationStep']] = None
    confidence_level: float = 0.0

    def __getitem__(self, key: str) -> Any:
        """Enable dictionary-like access to attributes."""
        if key in self.attributes:
            return self.attributes[key]
        raise KeyError(f"Attribute '{key}' not found")

    def __setitem__(self, key: str, value: Any) -> None:
        """Enable dictionary-like setting of attributes."""
        self.attributes[key] = value

    def get_score(self, metric: str) -> float:
        """Safely retrieve an evaluation score."""
        return self.evaluation_scores.get(metric, 0.0)

    def set_score(self, metric: str, value: float) -> None:
        """Set an evaluation score."""
        self.evaluation_scores[metric] = value

    def add_implementation_step(self, step: 'ImplementationStep') -> None:
        """Add a new implementation step to the plan."""
        if self.implementation_plan is None:
            self.implementation_plan = []
        self.implementation_plan.append(step)

    def add_evaluation(self, evaluation: 'AlternativeEvaluation') -> None:
        """Add evaluation scores from an AlternativeEvaluation."""
        for metric, score in evaluation.weighted_scores.items():
            self.evaluation_scores[metric] = score

@dataclass
class StepProgress:
    """Tracks the progress of a step in the decision-making process."""
    step_number: int
    status: Status = Status.NOT_STARTED
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    assigned_to: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def start(self, user: Optional[str] = None) -> None:
        """Mark the step as started."""
        self.status = Status.IN_PROGRESS
        self.started_at = datetime.now()
        if user:
            self.assigned_to.append(user)

    def complete(self, user: Optional[str] = None) -> None:
        """Mark the step as completed."""
        self.status = Status.COMPLETED
        self.completed_at = datetime.now()
        if user:
            self.assigned_to.append(user)

    def block(self, reason: str) -> None:
        """Mark the step as blocked."""
        self.status = Status.BLOCKED
        self.notes.append(f"BLOCKED: {reason}")

    def unblock(self) -> None:
        """Remove blocked status."""
        self.status = Status.IN_PROGRESS
        self.notes.append("UNBLOCKED: Continuing progress")

    def add_note(self, note: str) -> None:
        """Add a note to the step."""
        self.notes.append(note)

@dataclass
class InformationSource:
    """Represents a source of information used in decision making."""
    source_type: SourceType
    title: str
    description: str
    content: str
    verification_status: VerificationStatus
    url: Optional[str]
    notes: List[str]
    metadata: Dict[str, Any]
    source_id: str = field(default_factory=lambda: str(uuid4()))
    collection_date: datetime = field(default_factory=datetime.now)
    reliability: float = 0.0  # 0.0 to 1.0

    def __post_init__(self):
        if not 0.0 <= self.reliability <= 1.0:
            raise ValueError("Reliability must be between 0.0 and 1.0")

@dataclass
class Evidence:
    """Represents evidence supporting or opposing a decision."""
    related_sources: List[InformationSource]
    strength: float  # 0.0 to 1.0
    relevance: float  # 0.0 to 1.0
    impact_areas: List[str]
    confidence_level: float  # 0.0 to 1.0
    evidence_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("Strength must be between 0.0 and 1.0")
        if not 0.0 <= self.relevance <= 1.0:
            raise ValueError("Relevance must be between 0.0 and 1.0")
        if not 0.0 <= self.confidence_level <= 1.0:
            raise ValueError("Confidence level must be between 0.0 and 1.0")

@dataclass
class AlternativeGeneration:
    """Tracks the process of generating alternatives."""
    session_id: str
    method: GenerationTechnique
    participants: List[str]
    alternatives_generated: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class EvidenceEvaluation:
    """Evaluates evidence for a specific decision criteria."""
    criteria: DecisionCriteria
    supporting_evidence: List[Evidence]
    opposing_evidence: List[Evidence]
    confidence_score: float  # 0.0 to 1.0
    uncertainty_factors: List[str]
    assumptions: List[str]

    def __post_init__(self):
        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")

    def calculate_net_evidence_strength(self) -> float:
        """Calculate the net strength of evidence considering both supporting and opposing evidence."""
        supporting_strength = sum(e.strength * e.relevance * e.confidence_level for e in self.supporting_evidence)
        opposing_strength = sum(e.strength * e.relevance * e.confidence_level for e in self.opposing_evidence)
        return supporting_strength - opposing_strength

@dataclass
class ImplementationStep:
    """Represents a single step in the implementation plan."""
    description: str
    dependencies: List[str]
    resources_required: Dict[str, float]
    timeline: tuple
    step_id: str = field(default_factory=lambda: str(uuid4()))
    blockers: List[str] = field(default_factory=list)
    progress_metrics: Dict[str, float] = field(default_factory=dict)
    status: Status = Status.NOT_STARTED

    def is_blocked(self) -> bool:
        """Check if the step is currently blocked."""
        return len(self.blockers) > 0

    def update_progress(self, metric_name: str, value: float) -> None:
        """Update a progress metric for this step."""
        self.progress_metrics[metric_name] = value

@dataclass
class CognitiveCheck:
    """Track cognitive state and mindfulness during decision making."""
    check_id: str
    check_type: str
    description: str
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    performed_by: Optional[str] = None
    performed_at: datetime = field(default_factory=datetime.now)

    def add_note(self, note: str) -> None:
        """Add a note to the cognitive check."""
        self.findings.append(note)

@dataclass
class Discussion:
    """Track debates, discussions, and reflections during decision making."""
    discussion_id: str
    type: DiscussionType
    topic: str
    participants: List[str]
    messages: List[Dict[str, Any]]
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "open"

@dataclass
class DecisionVisualizer:
    """Helper class for generating visualizations of the decision-making process."""

    @staticmethod
    def create_decision_tree(cycle: 'ProblemSolvingCycle') -> Dict[str, Any]:
        """Generate a decision tree representation.
        
        Args:
            cycle: The problem-solving cycle to visualize
            
        Returns:
            Dict containing the tree structure
        """
        tree = {
            "problem": {
                "statement": cycle.problem_statement,
                "category": cycle.problem_category.value if cycle.problem_category else None,
                "scope": cycle.problem_scope
            },
            "criteria": {
                criterion.name: {
                    "weight": criterion.weight,
                    "category": criterion.category.value
                } for criterion in cycle.criteria.values()
            },
            "alternatives": [
                {
                    "name": alt.name,
                    "scores": alt.evaluation_scores,
                    "confidence": alt.confidence_level
                } for alt in cycle.alternatives
            ]
        }
        return tree

    @staticmethod
    def create_evidence_network(cycle: 'ProblemSolvingCycle') -> Dict[str, Any]:
        """Generate a network representation of evidence relationships.
        
        Args:
            cycle: The problem-solving cycle to visualize
            
        Returns:
            Dict containing the network structure
        """
        network: Dict[str, List[Any]] = {
            "nodes": [],
            "edges": []
        }
        
        # Add evidence nodes
        for eval_name, evaluation in cycle.evidence_evaluations.items():
            network["nodes"].append({
                "id": eval_name,
                "type": "criteria",
                "data": {
                    "name": eval_name,
                    "confidence": evaluation.confidence_score
                }
            })
            
            # Add evidence nodes and connections
            for evidence in evaluation.supporting_evidence:
                evidence_id = evidence.evidence_id
                network["nodes"].append({
                    "id": evidence_id,
                    "type": "evidence",
                    "data": {
                        "strength": evidence.strength,
                        "confidence": evidence.confidence_level
                    }
                })
                network["edges"].append({
                    "source": evidence_id,
                    "target": eval_name,
                    "type": "supports"
                })
            
            for evidence in evaluation.opposing_evidence:
                evidence_id = evidence.evidence_id
                network["nodes"].append({
                    "id": evidence_id,
                    "type": "evidence",
                    "data": {
                        "strength": evidence.strength,
                        "confidence": evidence.confidence_level
                    }
                })
                network["edges"].append({
                    "source": evidence_id,
                    "target": eval_name,
                    "type": "opposes"
                })
        
        return network

    @staticmethod
    def create_progress_dashboard(cycle: 'ProblemSolvingCycle') -> Dict[str, Any]:
        """Generate a dashboard representation of decision progress.
        
        Args:
            cycle: The problem-solving cycle to visualize
            
        Returns:
            Dict containing the dashboard data
        """
        progress = cycle.get_progress_summary()
        
        dashboard = {
            "overall_progress": {
                "completed": len([s for s in progress.values() if s["status"] == Status.COMPLETED]),
                "total_steps": len(progress),
                "blocked_steps": len([s for s in progress.values() if s["status"] == Status.BLOCKED])
            },
            "steps": progress,
            "timeline": [
                {
                    "step": step_num,
                    "started": step["started_at"].isoformat() if step["started_at"] else None,
                    "completed": step["completed_at"].isoformat() if step["completed_at"] else None,
                    "status": step["status"]
                } for step_num, step in progress.items()
            ],
            "cognitive_states": cycle.get_cognitive_state_summary(),
            "discussions": cycle.get_discussion_summary()
        }
        return dashboard

@dataclass
class AIAnalysis:
    """AI-powered analysis of decision components."""
    analysis_type: str
    input_data: Dict[str, Any]
    model_used: str
    confidence: float
    recommendations: List[str]
    analysis_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AnalyticsReport:
    """Analytics report for decision quality and efficiency."""
    metrics: Dict[str, float]
    predictions: Dict[str, Any]
    patterns: List[Dict[str, Any]]
    recommendations: List[str]
    report_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class CollaborationSession:
    """Tracks multi-user collaboration sessions."""
    participants: List[str]
    changes: List[Dict[str, Any]]
    comments: List[Dict[str, Any]]
    version: int
    session_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

class ProblemSolvingCycle:
    """
    Enhanced decision-making process that follows a cyclical approach with
    criteria-based evaluation and outcome tracking.
    """
    def __init__(self, title: str, created_by: Optional[str] = None):
        self.title = title
        self.created_at = datetime.now()
        self.created_by = created_by
        self.cycle_id: str = str(uuid4())
        
        # Step 1: Problem Identification
        self.problem_statement: str = ""
        self.problem_context: str = ""
        self.problem_category: Optional[ProblemCategory] = None
        self.problem_scope: Dict[str, Any] = {}
        
        # Step 2-3: Decision Criteria
        self.criteria: Dict[str, DecisionCriteria] = {}
        
        # Step 4-6: Alternatives and Evaluation
        self.alternatives: List[Alternative] = []
        self.chosen_alternative: Optional[Alternative] = None
        
        # Step 7-8: Implementation and Evaluation
        self.implementation_plan: str = ""
        self.decision_outcome: Optional[DecisionOutcome] = None
        
        # Progress tracking
        self.progress: Dict[int, StepProgress] = {
            i: StepProgress(step_number=i) for i in range(1, 9)
        }
        
        # Collaboration
        self.stakeholders: List[str] = []
        self.comments: List[Dict[str, Any]] = []
        
        # Information collection and evidence evaluation
        self.information_sources: List[InformationSource] = []
        self.evidence_evaluations: Dict[str, EvidenceEvaluation] = {}
        self.implementation_steps: List[ImplementationStep] = []
        self.alternative_generations: List[AlternativeGeneration] = []
        
        # Cognitive process tracking
        self.cognitive_checks: List[CognitiveCheck] = []
        self.discussions: List[Discussion] = []
        
        # AI and Analytics
        self.ai_analyses: List[AIAnalysis] = []
        self.analytics_reports: List[AnalyticsReport] = []
        self.collaboration_sessions: List[CollaborationSession] = []
        
        self.visualizer = DecisionVisualizer()
        
        # Quality and efficiency metrics
        self._evidence_quality_score: float = 0.0
        self._criteria_coverage_score: float = 0.0
        self._stakeholder_alignment_score: float = 0.0
        self._implementation_readiness_score: float = 0.0
    
    def step1_identify_problem(self, 
                             statement: str, 
                             context: str, 
                             category: ProblemCategory,
                             scope: Dict[str, Any],
                             user: Optional[str] = None):
        """Identify and document the problem with enhanced classification.
        
        Args:
            statement: Clear statement of the problem
            context: Background information and context
            category: Classification of the problem type
            scope: Dictionary defining the boundaries and impact areas
            user: Optional user identifier
        """
        self.progress[1].start(user)
        self.problem_statement = statement
        self.problem_context = context
        self.problem_category = category
        self.problem_scope = scope
        self.progress[1].complete(user)
    
    def step2_establish_criteria(self, criteria_list: List[DecisionCriteria], user: Optional[str] = None) -> None:
        """Establish decision criteria"""
        self.progress[2].start(user)
        for criterion in criteria_list:
            if not criterion.validate_weight():
                raise ValueError(f"Invalid weight for criterion: {criterion.name}")
            self.criteria[criterion.name] = criterion
        self.progress[2].complete(user)
    
    def step3_weigh_criteria(self, weights: Dict[str, float], user: Optional[str] = None) -> None:
        """Update weights for decision criteria"""
        self.progress[3].start(user)
        total_weight = sum(weights.values())
        if not (0.99 <= total_weight <= 1.01):  # Allow for floating-point imprecision
            raise ValueError(f"Criteria weights must sum to 1.0, got {total_weight}")
            
        for name, weight in weights.items():
            if name in self.criteria:
                self.criteria[name].weight = weight
        self.progress[3].complete(user)
    
    def step4_generate_alternatives(self, alternatives: List[Alternative], user: Optional[str] = None) -> None:
        """Generate potential alternatives"""
        self.progress[4].start(user)
        self.alternatives = alternatives
        self.progress[4].complete(user)
    
    def step5_evaluate_alternatives(self, evaluations: List[AlternativeEvaluation], user: Optional[str] = None) -> Dict[str, float]:
        """Evaluate alternatives against criteria"""
        self.progress[5].start(user)
        scores = {}
        for eval in evaluations:
            eval.recalculate_scores(self.criteria)
            alt = eval.alternative
            alt.add_evaluation(eval)
            scores[alt.description] = eval.total_score
        self.progress[5].complete(user)
        return scores
    
    def step6_choose_alternative(self, user: Optional[str] = None) -> Alternative:
        """Choose the best alternative based on evaluation scores."""
        self.progress[6].start(user)
        if not self.alternatives:
            raise ValueError("No alternatives to choose from")
            
        # Get the alternative with the highest total score
        # The key function returns float (not Optional[float]) so max works correctly
        self.chosen_alternative = max(
            self.alternatives,
            key=lambda a: a.get_score('total_score')
        )
        self.progress[6].complete(user)
        return self.chosen_alternative
    
    def step7_implement_decision(self, implementation_plan: str, user: Optional[str] = None) -> None:
        """Document and begin implementation of the chosen alternative"""
        self.progress[7].start(user)
        if not self.chosen_alternative:
            raise ValueError("No alternative has been chosen yet")
        self.implementation_plan = implementation_plan
        self.progress[7].complete(user)
    
    def step8_evaluate_decision(self, outcome: DecisionOutcome, user: Optional[str] = None) -> None:
        """Evaluate the implementation and outcomes"""
        self.progress[8].start(user)
        self.decision_outcome = outcome
        success_rate = outcome.calculate_success_rate()
        self.progress[8].add_note(f"Decision success rate: {success_rate:.2%}")
        self.progress[8].complete(user)
    
    def get_progress_summary(self) -> Dict[int, Dict[str, Any]]:
        """Get a summary of progress for all steps"""
        return {
            step: {
                "status": prog.status.value,
                "started_at": prog.started_at,
                "completed_at": prog.completed_at,
                "assigned_to": prog.assigned_to,
                "notes_count": len(prog.notes)
            }
            for step, prog in self.progress.items()
        }
    
    def save_to_file(self, filename: str) -> None:
        """Save the current state of the problem-solving cycle to a JSON file."""
        data = {
            "title": self.title,
            "cycle_id": self.cycle_id,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "problem_statement": self.problem_statement,
            "problem_context": self.problem_context,
            "problem_category": self.problem_category.value if self.problem_category else None,
            "problem_scope": self.problem_scope,
            "criteria": [
                {
                    "name": criterion.name,
                    "description": criterion.description,
                    "weight": criterion.weight,
                    "category": criterion.category.value,
                    "measurement_method": criterion.measurement_method,
                    "threshold": criterion.threshold
                }
                for criterion in self.criteria.values()
            ],
            "alternatives": [
                {
                    "alternative_id": alt.alternative_id,
                    "name": alt.name,
                    "description": alt.description,
                    "attributes": alt.attributes,
                    "evaluation_scores": alt.evaluation_scores,
                    "implementation_plan": alt.implementation_plan,
                    "confidence_level": alt.confidence_level
                }
                for alt in self.alternatives
            ],
            "chosen_alternative": (
                {
                    "alternative_id": self.chosen_alternative.alternative_id,
                    "name": self.chosen_alternative.name,
                    "description": self.chosen_alternative.description,
                    "attributes": self.chosen_alternative.attributes,
                    "evaluation_scores": self.chosen_alternative.evaluation_scores,
                    "implementation_plan": self.chosen_alternative.implementation_plan,
                    "confidence_level": self.chosen_alternative.confidence_level
                }
                if self.chosen_alternative else None
            ),
            "implementation_plan": self.implementation_plan,
            "decision_outcome": (
                {
                    "decision_id": self.decision_outcome.decision_id,
                    "implementation_date": self.decision_outcome.implementation_date.isoformat(),
                    "success_metrics": self.decision_outcome.success_metrics,
                    "actual_outcomes": self.decision_outcome.actual_outcomes,
                    "lessons_learned": self.decision_outcome.lessons_learned,
                    "follow_up_actions": self.decision_outcome.follow_up_actions
                }
                if self.decision_outcome else None
            ),
            "progress": {
                step: {
                    "status": prog.status.value,
                    "started_at": prog.started_at.isoformat() if prog.started_at else None,
                    "completed_at": prog.completed_at.isoformat() if prog.completed_at else None,
                    "assigned_to": prog.assigned_to,
                    "notes": prog.notes
                }
                for step, prog in self.progress.items()
            },
            "stakeholders": self.stakeholders,
            "comments": self.comments,
            "information_sources": [asdict(source) for source in self.information_sources],
            "evidence_evaluations": {
                name: asdict(eval_) for name, eval_ in self.evidence_evaluations.items()
            },
            "implementation_steps": [asdict(step) for step in self.implementation_steps],
            "alternative_generations": [asdict(gen) for gen in self.alternative_generations],
            "cognitive_checks": [asdict(check) for check in self.cognitive_checks],
            "discussions": [asdict(discussion) for discussion in self.discussions],
            "ai_analyses": [asdict(analysis) for analysis in self.ai_analyses],
            "analytics_reports": [asdict(report) for report in self.analytics_reports],
            "collaboration_sessions": [asdict(session) for session in self.collaboration_sessions]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
            
    @classmethod
    def load_from_file(cls, filename: str) -> 'ProblemSolvingCycle':
        """Load a problem-solving cycle from a JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
            
        cycle = cls(
            title=data["title"],
            created_by=data.get("created_by")
        )
        cycle.cycle_id = data.get("cycle_id", str(uuid4()))
        cycle.created_at = datetime.fromisoformat(data["created_at"])
        cycle.problem_statement = data["problem_statement"]
        cycle.problem_context = data["problem_context"]
        cycle.problem_category = ProblemCategory(data["problem_category"]) if data.get("problem_category") else None
        cycle.problem_scope = data["problem_scope"]
        
        cycle.criteria = {
            criterion["name"]: DecisionCriteria(
                name=criterion["name"],
                description=criterion["description"],
                weight=criterion["weight"],
                category=CriteriaCategory(criterion["category"]),
                measurement_method=criterion["measurement_method"],
                threshold=criterion.get("threshold")
            )
            for criterion in data["criteria"]
        }
        
        cycle.alternatives = [
            Alternative(
                alternative_id=alt["alternative_id"],
                name=alt["name"],
                description=alt["description"],
                attributes=alt["attributes"],
                evaluation_scores=alt["evaluation_scores"],
                implementation_plan=alt.get("implementation_plan"),
                confidence_level=alt.get("confidence_level", 0.0)
            )
            for alt in data["alternatives"]
        ]
        
        if data["chosen_alternative"]:
            alt = data["chosen_alternative"]
            cycle.chosen_alternative = Alternative(
                alternative_id=alt["alternative_id"],
                name=alt["name"],
                description=alt["description"],
                attributes=alt["attributes"],
                evaluation_scores=alt["evaluation_scores"],
                implementation_plan=alt.get("implementation_plan"),
                confidence_level=alt.get("confidence_level", 0.0)
            )
        
        cycle.implementation_plan = data["implementation_plan"]
        
        if data["decision_outcome"]:
            outcome = data["decision_outcome"]
            cycle.decision_outcome = DecisionOutcome(
                decision_id=outcome["decision_id"],
                implementation_date=datetime.fromisoformat(outcome["implementation_date"]),
                success_metrics=outcome["success_metrics"],
                actual_outcomes=outcome["actual_outcomes"],
                lessons_learned=outcome["lessons_learned"],
                follow_up_actions=outcome["follow_up_actions"]
            )
        
        # Load progress data
        for step, prog_data in data["progress"].items():
            step_num = int(step)
            progress = cycle.progress[step_num]
            progress.status = Status(prog_data["status"])
            if prog_data["started_at"]:
                progress.started_at = datetime.fromisoformat(prog_data["started_at"])
            if prog_data["completed_at"]:
                progress.completed_at = datetime.fromisoformat(prog_data["completed_at"])
            progress.assigned_to = prog_data["assigned_to"]
            progress.notes = prog_data["notes"]
            
        cycle.stakeholders = data.get("stakeholders", [])
        cycle.comments = data.get("comments", [])
        
        # Load information sources
        cycle.information_sources = [
            InformationSource(**source_data) for source_data in data.get("information_sources", [])
        ]
        
        # Load evidence evaluations
        cycle.evidence_evaluations = {
            name: EvidenceEvaluation(**eval_data)
            for name, eval_data in data.get("evidence_evaluations", {}).items()
        }
        
        # Load implementation steps
        cycle.implementation_steps = [
            ImplementationStep(**step_data) for step_data in data.get("implementation_steps", [])
        ]
        
        # Load alternative generations
        cycle.alternative_generations = [
            AlternativeGeneration(**gen_data) for gen_data in data.get("alternative_generations", [])
        ]
        
        # Load cognitive checks
        cycle.cognitive_checks = [
            CognitiveCheck(**check_data) for check_data in data.get("cognitive_checks", [])
        ]
        
        # Load discussions
        cycle.discussions = [
            Discussion(**discussion_data) for discussion_data in data.get("discussions", [])
        ]
        
        # Load AI analyses
        cycle.ai_analyses = [
            AIAnalysis(**analysis_data) for analysis_data in data.get("ai_analyses", [])
        ]
        
        # Load analytics reports
        cycle.analytics_reports = [
            AnalyticsReport(**report_data) for report_data in data.get("analytics_reports", [])
        ]
        
        # Load collaboration sessions
        cycle.collaboration_sessions = [
            CollaborationSession(**session_data) for session_data in data.get("collaboration_sessions", [])
        ]
        
        return cycle

    @classmethod
    def load_v1_format(cls, filename: str) -> 'ProblemSolvingCycle':
        """Load and migrate a version 1 format problem-solving cycle file."""
        with open(filename, 'r') as f:
            old_data = json.load(f)
        
        new_data = cls.migrate_v1_to_v2(old_data)
        
        # Create new instance using migrated data
        cycle = cls(title=new_data["title"])
        
        # Load all the migrated data
        cycle.created_at = datetime.fromisoformat(new_data["created_at"])
        cycle.created_by = new_data["created_by"]
        cycle.cycle_id = new_data["cycle_id"]
        
        cycle.problem_statement = new_data["problem_statement"]
        cycle.problem_context = new_data["problem_context"]
        cycle.problem_category = ProblemCategory(new_data["problem_category"]) if new_data.get("problem_category") else None
        cycle.problem_scope = new_data["problem_scope"]
        
        # Load criteria
        cycle.criteria = {
            criterion["name"]: DecisionCriteria(
                name=criterion["name"],
                description=criterion["description"],
                weight=criterion["weight"],
                category=CriteriaCategory(criterion["category"]),
                measurement_method=criterion["measurement_method"],
                threshold=criterion.get("threshold")
            )
            for criterion in new_data["criteria"]
        }
        
        # Load alternatives with evaluations
        cycle.alternatives = [
            Alternative(
                alternative_id=alt["alternative_id"],
                name=alt["name"],
                description=alt["description"],
                attributes=alt["attributes"],
                evaluation_scores=alt["evaluation_scores"],
                implementation_plan=alt.get("implementation_plan"),
                confidence_level=alt.get("confidence_level", 0.0)
            )
            for alt in new_data["alternatives"]
        ]
        
        if new_data.get("chosen_alternative"):
            alt = new_data["chosen_alternative"]
            cycle.chosen_alternative = Alternative(
                alternative_id=alt["alternative_id"],
                name=alt["name"],
                description=alt["description"],
                attributes=alt["attributes"],
                evaluation_scores=alt["evaluation_scores"],
                implementation_plan=alt.get("implementation_plan"),
                confidence_level=alt.get("confidence_level", 0.0)
            )
        
        cycle.implementation_plan = new_data["implementation_plan"]
        
        if new_data["decision_outcome"]:
            outcome = new_data["decision_outcome"]
            cycle.decision_outcome = DecisionOutcome(
                decision_id=outcome["decision_id"],
                implementation_date=datetime.fromisoformat(outcome["implementation_date"]),
                success_metrics=outcome["success_metrics"],
                actual_outcomes=outcome["actual_outcomes"],
                lessons_learned=outcome["lessons_learned"],
                follow_up_actions=outcome["follow_up_actions"]
            )
        
        # Load progress data
        for step, prog_data in new_data["progress"].items():
            step_num = int(step)
            progress = cycle.progress[step_num]
            progress.status = Status(prog_data["status"])
            if prog_data["started_at"]:
                progress.started_at = datetime.fromisoformat(prog_data["started_at"])
            if prog_data["completed_at"]:
                progress.completed_at = datetime.fromisoformat(prog_data["completed_at"])
            progress.assigned_to = prog_data["assigned_to"]
            progress.notes = prog_data["notes"]
            
        cycle.stakeholders = new_data.get("stakeholders", [])
        cycle.comments = new_data.get("comments", [])
        
        # Load information sources
        cycle.information_sources = [
            InformationSource(**source_data) for source_data in new_data.get("information_sources", [])
        ]
        
        # Load evidence evaluations
        cycle.evidence_evaluations = {
            name: EvidenceEvaluation(**eval_data)
            for name, eval_data in new_data.get("evidence_evaluations", {}).items()
        }
        
        # Load implementation steps
        cycle.implementation_steps = [
            ImplementationStep(**step_data) for step_data in new_data.get("implementation_steps", [])
        ]
        
        # Load alternative generations
        cycle.alternative_generations = [
            AlternativeGeneration(**gen_data) for gen_data in new_data.get("alternative_generations", [])
        ]
        
        # Load cognitive checks
        cycle.cognitive_checks = [
            CognitiveCheck(**check_data) for check_data in new_data.get("cognitive_checks", [])
        ]
        
        # Load discussions
        cycle.discussions = [
            Discussion(**discussion_data) for discussion_data in new_data.get("discussions", [])
        ]
        
        # Load AI analyses
        cycle.ai_analyses = [
            AIAnalysis(**analysis_data) for analysis_data in new_data.get("ai_analyses", [])
        ]
        
        # Load analytics reports
        cycle.analytics_reports = [
            AnalyticsReport(**report_data) for report_data in new_data.get("analytics_reports", [])
        ]
        
        # Load collaboration sessions
        cycle.collaboration_sessions = [
            CollaborationSession(**session_data) for session_data in new_data.get("collaboration_sessions", [])
        ]
        
        return cycle

    @staticmethod
    def migrate_v1_to_v2(old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Migrate data from version 1 format to version 2 format.
        Version 1: Original problem-solving cycle
        Version 2: Enhanced decision-making cycle with criteria
        """
        new_data = {
            "title": old_data["title"],
            "created_at": old_data["created_at"],
            "created_by": old_data.get("created_by"),
            "cycle_id": old_data.get("cycle_id", str(uuid4())),
            
            # Step 1: Problem Identification
            "problem_statement": old_data.get("problem_definition", ""),
            "problem_context": old_data.get("situation", ""),
            "problem_category": None,
            "problem_scope": {},
            
            # Step 2-3: Decision Criteria
            "criteria": [
                {
                    "name": f"objective_{i}",
                    "description": obj,
                    "weight": 1.0 / len(old_data.get("objectives", [])) if old_data.get("objectives") else 1.0,
                    "category": "STRATEGIC",
                    "measurement_method": "qualitative",
                    "threshold": None
                }
                for i, obj in enumerate(old_data.get("objectives", []))
            ],
            
            # Step 4-6: Alternatives
            "alternatives": [
                {
                    "alternative_id": str(uuid4()),
                    "name": alt["description"],
                    "description": alt["description"],
                    "attributes": {},
                    "evaluation_scores": {
                        "total_score": alt.get("score", 0.0)
                    },
                    "implementation_plan": None,
                    "confidence_level": 0.0
                }
                for alt in old_data.get("alternatives", [])
            ],
            
            # Step 7-8: Implementation and Evaluation
            "implementation_plan": old_data.get("implementation_notes", ""),
            "decision_outcome": None,  # No equivalent in old format
            
            # Progress and metadata
            "progress": {
                str(i): {
                    "status": "completed" if old_data.get(f"step{i}_completed", False) else "not_started",
                    "started_at": None,
                    "completed_at": None,
                    "assigned_to": None,
                    "notes": []
                }
                for i in range(1, 9)
            },
            "stakeholders": [],
            "comments": []
        }
        
        # Handle chosen alternative
        if old_data.get("chosen_alternative"):
            chosen = old_data["chosen_alternative"]
            new_data["chosen_alternative"] = {
                "alternative_id": str(uuid4()),
                "name": chosen["description"],
                "description": chosen["description"],
                "attributes": {},
                "evaluation_scores": {
                    "total_score": chosen.get("score", 0.0)
                },
                "implementation_plan": None,
                "confidence_level": 0.0
            }
        
        return new_data

    def add_information_source(self, source: InformationSource) -> None:
        """Add a new information source to the cycle."""
        self.information_sources.append(source)

    def add_evidence_evaluation(self, criteria_name: str, evaluation: EvidenceEvaluation) -> None:
        """Add an evidence evaluation for a specific criteria."""
        self.evidence_evaluations[criteria_name] = evaluation

    def add_implementation_step(self, step: ImplementationStep) -> None:
        """Add a new implementation step to the plan."""
        self.implementation_steps.append(step)

    def record_alternative_generation(self, generation: AlternativeGeneration) -> None:
        """Record a new alternative generation session."""
        self.alternative_generations.append(generation)

    def get_evidence_strength_for_criteria(self, criteria_name: str) -> Optional[float]:
        """Get the net evidence strength for a specific criteria."""
        if criteria_name in self.evidence_evaluations:
            return self.evidence_evaluations[criteria_name].calculate_net_evidence_strength()
        return None

    def get_blocked_implementation_steps(self) -> List[ImplementationStep]:
        """Get all implementation steps that are currently blocked."""
        return [step for step in self.implementation_steps if step.is_blocked()]

    def add_cognitive_check(self, name: str, description: str, check_type: str, 
                           findings: Optional[List[str]] = None,
                           recommendations: Optional[List[str]] = None,
                           performed_by: Optional[str] = None) -> None:
        """Add a cognitive state check during the decision process."""
        if findings is None:
            findings = []
        if recommendations is None:
            recommendations = []
        
        check = CognitiveCheck(
            check_id=str(uuid4()),
            check_type=check_type,
            description=description,
            findings=findings,
            recommendations=recommendations,
            performed_by=performed_by
        )
        self.cognitive_checks.append(check)
        
        # If stress is high or clarity is low, log a warning
        if check_type == "stress" and findings:
            logging.warning(f"Cognitive overload risk detected: Stress={findings[0]}")
        elif check_type == "clarity" and findings:
            logging.warning(f"Cognitive overload risk detected: Clarity={findings[0]}")

    def record_discussion(self, type: DiscussionType, topic: str, participants: List[str],
                        messages: List[Dict[str, Any]], 
                        tags: Optional[List[str]] = None,
                        created_at: Optional[datetime] = None,
                        status: str = "open") -> None:
        """Record a discussion, debate, or reflection session."""
        if tags is None:
            tags = []
        if created_at is None:
            created_at = datetime.now()
        
        discussion = Discussion(
            discussion_id=str(uuid4()),
            type=type,
            topic=topic,
            participants=participants,
            messages=messages,
            tags=tags,
            created_at=created_at,
            status=status
        )
        self.discussions.append(discussion)

    def get_cognitive_state_summary(self) -> Dict[str, Any]:
        """Get a summary of cognitive states throughout the decision process."""
        if not self.cognitive_checks:
            return {}
            
        return {
            "average_clarity": sum(1 for c in self.cognitive_checks if c.check_type == "clarity" and c.findings) / len(self.cognitive_checks),
            "average_stress": sum(1 for c in self.cognitive_checks if c.check_type == "stress" and c.findings) / len(self.cognitive_checks),
            "state_distribution": Counter(c.check_type for c in self.cognitive_checks),
            "high_stress_incidents": sum(1 for c in self.cognitive_checks if c.check_type == "stress" and c.findings),
            "low_clarity_incidents": sum(1 for c in self.cognitive_checks if c.check_type == "clarity" and c.findings)
        }

    def get_discussion_summary(self) -> Dict[str, Any]:
        """Get a summary of discussions and their outcomes."""
        if not self.discussions:
            return {}
            
        return {
            "total_discussions": len(self.discussions),
            "type_distribution": Counter(d.type for d in self.discussions),
            "total_decisions": sum(len(d.messages) for d in self.discussions),
            "pending_action_items": sum(len(d.tags) for d in self.discussions if d.status == "open"),
            "unique_participants": len(set(p for d in self.discussions for p in d.participants))
        }

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "title": self.title,
            "cycle_id": self.cycle_id,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "problem_statement": self.problem_statement,
            "problem_context": self.problem_context,
            "problem_category": self.problem_category.value if self.problem_category else None,
            "problem_scope": self.problem_scope,
            "criteria": [
                {
                    "name": criterion.name,
                    "description": criterion.description,
                    "weight": criterion.weight,
                    "category": criterion.category.value,
                    "measurement_method": criterion.measurement_method,
                    "threshold": criterion.threshold
                }
                for criterion in self.criteria.values()
            ],
            "alternatives": [
                {
                    "alternative_id": alt.alternative_id,
                    "name": alt.name,
                    "description": alt.description,
                    "attributes": alt.attributes,
                    "evaluation_scores": alt.evaluation_scores,
                    "implementation_plan": alt.implementation_plan,
                    "confidence_level": alt.confidence_level
                }
                for alt in self.alternatives
            ],
            "chosen_alternative": (
                {
                    "alternative_id": self.chosen_alternative.alternative_id,
                    "name": self.chosen_alternative.name,
                    "description": self.chosen_alternative.description,
                    "attributes": self.chosen_alternative.attributes,
                    "evaluation_scores": self.chosen_alternative.evaluation_scores,
                    "implementation_plan": self.chosen_alternative.implementation_plan,
                    "confidence_level": self.chosen_alternative.confidence_level
                }
                if self.chosen_alternative else None
            ),
            "implementation_plan": self.implementation_plan,
            "decision_outcome": (
                {
                    "decision_id": self.decision_outcome.decision_id,
                    "implementation_date": self.decision_outcome.implementation_date.isoformat(),
                    "success_metrics": self.decision_outcome.success_metrics,
                    "actual_outcomes": self.decision_outcome.actual_outcomes,
                    "lessons_learned": self.decision_outcome.lessons_learned,
                    "follow_up_actions": self.decision_outcome.follow_up_actions
                }
                if self.decision_outcome else None
            ),
            "progress": {
                step: {
                    "status": prog.status.value,
                    "started_at": prog.started_at.isoformat() if prog.started_at else None,
                    "completed_at": prog.completed_at.isoformat() if prog.completed_at else None,
                    "assigned_to": prog.assigned_to,
                    "notes": prog.notes
                }
                for step, prog in self.progress.items()
            },
            "stakeholders": self.stakeholders,
            "comments": self.comments,
            "information_sources": [asdict(source) for source in self.information_sources],
            "evidence_evaluations": {
                name: asdict(eval_) for name, eval_ in self.evidence_evaluations.items()
            },
            "implementation_steps": [asdict(step) for step in self.implementation_steps],
            "alternative_generations": [asdict(gen) for gen in self.alternative_generations],
            "cognitive_checks": [asdict(check) for check in self.cognitive_checks],
            "discussions": [asdict(discussion) for discussion in self.discussions],
            "ai_analyses": [asdict(analysis) for analysis in self.ai_analyses],
            "analytics_reports": [asdict(report) for report in self.analytics_reports],
            "collaboration_sessions": [asdict(session) for session in self.collaboration_sessions]
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProblemSolvingCycle':
        cycle = cls(
            title=data["title"],
            created_by=data.get("created_by")
        )
        cycle.cycle_id = data.get("cycle_id", str(uuid4()))
        cycle.created_at = datetime.fromisoformat(data["created_at"])
        cycle.problem_statement = data["problem_statement"]
        cycle.problem_context = data["problem_context"]
        cycle.problem_category = ProblemCategory(data["problem_category"]) if data.get("problem_category") else None
        cycle.problem_scope = data["problem_scope"]
        
        cycle.criteria = {
            criterion["name"]: DecisionCriteria(
                name=criterion["name"],
                description=criterion["description"],
                weight=criterion["weight"],
                category=CriteriaCategory(criterion["category"]),
                measurement_method=criterion["measurement_method"],
                threshold=criterion.get("threshold")
            )
            for criterion in data["criteria"]
        }
        
        cycle.alternatives = [
            Alternative(
                alternative_id=alt["alternative_id"],
                name=alt["name"],
                description=alt["description"],
                attributes=alt["attributes"],
                evaluation_scores=alt["evaluation_scores"],
                implementation_plan=alt.get("implementation_plan"),
                confidence_level=alt.get("confidence_level", 0.0)
            )
            for alt in data["alternatives"]
        ]
        
        if data["chosen_alternative"]:
            alt = data["chosen_alternative"]
            cycle.chosen_alternative = Alternative(
                alternative_id=alt["alternative_id"],
                name=alt["name"],
                description=alt["description"],
                attributes=alt["attributes"],
                evaluation_scores=alt["evaluation_scores"],
                implementation_plan=alt.get("implementation_plan"),
                confidence_level=alt.get("confidence_level", 0.0)
            )
        
        cycle.implementation_plan = data["implementation_plan"]
        
        if data["decision_outcome"]:
            outcome = data["decision_outcome"]
            cycle.decision_outcome = DecisionOutcome(
                decision_id=outcome["decision_id"],
                implementation_date=datetime.fromisoformat(outcome["implementation_date"]),
                success_metrics=outcome["success_metrics"],
                actual_outcomes=outcome["actual_outcomes"],
                lessons_learned=outcome["lessons_learned"],
                follow_up_actions=outcome["follow_up_actions"]
            )
        
        # Load progress data
        for step, prog_data in data["progress"].items():
            step_num = int(step)
            progress = cycle.progress[step_num]
            progress.status = Status(prog_data["status"])
            if prog_data["started_at"]:
                progress.started_at = datetime.fromisoformat(prog_data["started_at"])
            if prog_data["completed_at"]:
                progress.completed_at = datetime.fromisoformat(prog_data["completed_at"])
            progress.assigned_to = prog_data["assigned_to"]
            progress.notes = prog_data["notes"]
            
        cycle.stakeholders = data.get("stakeholders", [])
        cycle.comments = data.get("comments", [])
        
        # Load information sources
        cycle.information_sources = [
            InformationSource(**source_data) for source_data in data.get("information_sources", [])
        ]
        
        # Load evidence evaluations
        cycle.evidence_evaluations = {
            name: EvidenceEvaluation(**eval_data)
            for name, eval_data in data.get("evidence_evaluations", {}).items()
        }
        
        # Load implementation steps
        cycle.implementation_steps = [
            ImplementationStep(**step_data) for step_data in data.get("implementation_steps", [])
        ]
        
        # Load alternative generations
        cycle.alternative_generations = [
            AlternativeGeneration(**gen_data) for gen_data in data.get("alternative_generations", [])
        ]
        
        # Load cognitive checks
        cycle.cognitive_checks = [
            CognitiveCheck(**check_data) for check_data in data.get("cognitive_checks", [])
        ]
        
        # Load discussions
        cycle.discussions = [
            Discussion(**discussion_data) for discussion_data in data.get("discussions", [])
        ]
        
        # Load AI analyses
        cycle.ai_analyses = [
            AIAnalysis(**analysis_data) for analysis_data in data.get("ai_analyses", [])
        ]
        
        # Load analytics reports
        cycle.analytics_reports = [
            AnalyticsReport(**report_data) for report_data in data.get("analytics_reports", [])
        ]
        
        # Load collaboration sessions
        cycle.collaboration_sessions = [
            CollaborationSession(**session_data) for session_data in data.get("collaboration_sessions", [])
        ]
        
        return cycle

    def run_ai_analysis(self, analysis_type: str, input_data: Dict[str, Any], 
                       model: str = "gpt-4") -> AIAnalysis:
        """Run AI analysis on decision components.
        
        Args:
            analysis_type: Type of analysis to perform
            input_data: Data to analyze
            model: AI model to use
            
        Returns:
            AIAnalysis object with results
        """
        # Placeholder for AI integration
        analysis = AIAnalysis(
            analysis_type=analysis_type,
            input_data=input_data,
            model_used=model,
            confidence=0.9,
            recommendations=["AI analysis not yet implemented"]
        )
        self.ai_analyses.append(analysis)
        return analysis
    
    def generate_analytics_report(self) -> AnalyticsReport:
        """Generate analytics report with metrics and predictions."""
        metrics = {
            "decision_quality": self._calculate_decision_quality(),
            "process_efficiency": self._calculate_process_efficiency(),
            "evidence_strength": self._calculate_evidence_strength(),
            "stakeholder_alignment": self._calculate_stakeholder_alignment()
        }
        
        predictions = {
            "expected_outcome_probability": self._predict_outcome_probability(),
            "risk_factors": self._identify_risk_factors(),
            "success_indicators": self._identify_success_indicators()
        }
        
        patterns = self._identify_decision_patterns()
        recommendations = self._generate_recommendations()
        
        report = AnalyticsReport(
            metrics=metrics,
            predictions=predictions,
            patterns=patterns,
            recommendations=recommendations
        )
        self.analytics_reports.append(report)
        return report
    
    def start_collaboration_session(self, participants: List[str]) -> CollaborationSession:
        """Start a new collaboration session.
        
        Args:
            participants: List of participant identifiers
            
        Returns:
            New CollaborationSession object
        """
        session = CollaborationSession(
            participants=participants,
            changes=[],
            comments=[],
            version=len(self.collaboration_sessions) + 1
        )
        self.collaboration_sessions.append(session)
        return session
    
    def _calculate_decision_quality(self) -> float:
        """Calculate overall decision quality score."""
        if not self.chosen_alternative:
            return 0.0
        
        # Calculate individual quality factors
        evidence_quality = self._evidence_quality_score
        criteria_coverage = self._criteria_coverage_score
        stakeholder_alignment = self._stakeholder_alignment_score
        implementation_readiness = self._implementation_readiness_score
        
        # Ensure all factors are within valid range [0.0, 1.0]
        factors = [
            max(0.0, min(1.0, score)) for score in [
                evidence_quality,
                criteria_coverage,
                stakeholder_alignment,
                implementation_readiness
            ]
        ]
        
        # Return average of all factors
        return float(sum(factors) / len(factors)) if factors else 0.0
    
    def _calculate_process_efficiency(self) -> float:
        """Calculate process efficiency score based on completion time and step progress.
        
        Returns:
            float: Efficiency score between 0.0 and 1.0
        """
        total_time: float = 0.0
        completed_steps: int = 0
        
        # Calculate average time per completed step
        for step in self.progress.values():
            if step.completed_at and step.started_at:
                step_duration = (step.completed_at - step.started_at).total_seconds()
                total_time += step_duration
                completed_steps += 1
        
        if not completed_steps:
            return 0.0
            
        # Calculate average time per step (in hours)
        avg_time_per_step = (total_time / completed_steps) / 3600.0
        
        # Define efficiency thresholds (in hours)
        optimal_time = 2.0  # 2 hours per step is considered optimal
        max_time = 8.0     # 8 hours per step is considered inefficient
        
        # Calculate efficiency score
        if avg_time_per_step <= optimal_time:
            efficiency = 1.0
        elif avg_time_per_step >= max_time:
            efficiency = 0.0
        else:
            # Linear interpolation between optimal and max time
            efficiency = 1.0 - ((avg_time_per_step - optimal_time) / (max_time - optimal_time))
        
        return float(max(0.0, min(1.0, efficiency)))
    
    def _calculate_evidence_strength(self) -> float:
        """Calculate overall evidence strength."""
        if not self.evidence_evaluations:
            return 0.0
        
        total_strength = sum(
            eval.calculate_net_evidence_strength()
            for eval in self.evidence_evaluations.values()
        )
        return total_strength / len(self.evidence_evaluations)
    
    def _calculate_stakeholder_alignment(self) -> float:
        """Calculate stakeholder alignment score."""
        # Placeholder for stakeholder alignment calculation
        return 0.8
    
    def _predict_outcome_probability(self) -> float:
        """Predict probability of successful outcome."""
        # Placeholder for outcome prediction
        return 0.75
    
    def _identify_risk_factors(self) -> List[Dict[str, Any]]:
        """Identify potential risk factors."""
        # Placeholder for risk analysis
        return [{"factor": "implementation_complexity", "risk_level": "medium"}]
    
    def _identify_success_indicators(self) -> List[Dict[str, Any]]:
        """Identify key success indicators."""
        # Placeholder for success indicator analysis
        return [{"indicator": "stakeholder_support", "status": "positive"}]
    
    def _identify_decision_patterns(self) -> List[Dict[str, Any]]:
        """Identify patterns in decision making process."""
        # Placeholder for pattern recognition
        return [{"pattern": "evidence_based_decisions", "frequency": "high"}]
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis."""
        # Placeholder for recommendation generation
        return ["Increase stakeholder engagement", "Gather more evidence"]
