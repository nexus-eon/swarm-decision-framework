"""
Decision Framework - A comprehensive problem-solving and decision-making framework.

This package provides a structured approach to complex decision-making processes,
incorporating cognitive tracking, evidence-based evaluation, and collaborative features.
"""

from .core.problem import (
    ProblemSolvingCycle,
    Alternative,
    DecisionCriteria,
    Evidence,
    InformationSource,
    EvidenceEvaluation,
    ImplementationStep,
    AlternativeGeneration,
    CognitiveCheck,
    Discussion,
    Status,
    RiskLevel,
    CriteriaCategory,
    SourceType,
    VerificationStatus,
    GenerationTechnique,
    CognitiveState,
    DiscussionType,
)

__version__ = '1.0.0'
__author__ = 'Nexus'
__all__ = [
    'ProblemSolvingCycle',
    'Alternative',
    'DecisionCriteria',
    'Evidence',
    'InformationSource',
    'EvidenceEvaluation',
    'ImplementationStep',
    'AlternativeGeneration',
    'CognitiveCheck',
    'Discussion',
    'Status',
    'RiskLevel',
    'CriteriaCategory',
    'SourceType',
    'VerificationStatus',
    'GenerationTechnique',
    'CognitiveState',
    'DiscussionType',
]
