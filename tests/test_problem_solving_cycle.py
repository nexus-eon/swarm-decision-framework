import unittest
from src.decision_framework.problem_solving_cycle import (
    ProblemSolvingCycle,
    Alternative,
    DecisionCriteria,
    AlternativeEvaluation,
    DecisionOutcome,
    CognitiveCheck
)

class TestProblemSolvingCycle(unittest.TestCase):
    def setUp(self):
        self.cycle = ProblemSolvingCycle(title="Test Decision Process")
    
    def test_initialization(self):
        """Test basic initialization of ProblemSolvingCycle"""
        self.assertIsNotNone(self.cycle)
        self.assertEqual(self.cycle.title, "Test Decision Process")
        # Add more initialization tests

    def test_alternative_creation(self):
        """Test creating and managing alternatives"""
        # Add alternative creation tests
        pass

    def test_criteria_evaluation(self):
        """Test criteria creation and evaluation"""
        # Add criteria evaluation tests
        pass

    def test_cognitive_checks(self):
        """Test cognitive state tracking"""
        # Add cognitive check tests
        pass

    def test_decision_outcome(self):
        """Test decision outcome tracking"""
        # Add outcome tracking tests
        pass

    def test_alternative_evaluation(self):
        """Test AlternativeEvaluation initialization and score calculation"""
        alt = Alternative(
            name="Option A",
            description="Test option",
            attributes={"cost": 100, "quality": 8}
        )
        
        eval = AlternativeEvaluation(
            alternative=alt,
            criteria_scores={"cost": 0.8, "quality": 0.9},
            evaluation_notes=["Test evaluation"],
            evaluator="Test Team"
        )
        
        # Check automatic calculation of scores
        self.assertEqual(eval.weighted_scores, {"cost": 0.8, "quality": 0.9})
        self.assertAlmostEqual(eval.total_score, 1.7)
        
        # Test recalculation with criteria weights
        criteria = {
            "cost": DecisionCriteria(
                name="cost",
                description="Cost factor",
                weight=0.6,
                category="financial",
                measurement_method="direct_score"
            ),
            "quality": DecisionCriteria(
                name="quality",
                description="Quality factor",
                weight=0.4,
                category="performance",
                measurement_method="direct_score"
            )
        }
        
        eval.recalculate_scores(criteria)
        self.assertEqual(eval.weighted_scores["cost"], 0.8 * 0.6)
        self.assertEqual(eval.weighted_scores["quality"], 0.9 * 0.4)
        self.assertAlmostEqual(eval.total_score, (0.8 * 0.6) + (0.9 * 0.4))

if __name__ == '__main__':
    unittest.main()
