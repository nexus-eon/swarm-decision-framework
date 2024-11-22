from datetime import datetime
from src.decision_framework.problem_solving_cycle import (
    ProblemSolvingCycle, Alternative, ProblemCategory,
    DecisionCriteria, CriteriaCategory, AlternativeEvaluation,
    DecisionOutcome
)

def main():
    # Create a new problem-solving cycle
    cycle = ProblemSolvingCycle(title="Office Space Optimization")
    
    # Step 1: Identify Problem
    cycle.step1_identify_problem(
        statement="The current office space is insufficient for our growing team, leading to overcrowding and reduced productivity.",
        context="Our company has grown from 50 to 100 employees in the last year, and our current office space is becoming cramped. This is affecting productivity and employee satisfaction.",
        category=ProblemCategory.OPERATIONAL,
        scope={
            "employees_affected": 100,
            "current_space": "10,000 sq ft",
            "departments": ["Engineering", "Sales", "Marketing", "HR"],
            "impact_areas": ["Productivity", "Employee Satisfaction", "Collaboration"]
        }
    )
    
    # Step 2-3: Establish and Weigh Criteria
    criteria = [
        DecisionCriteria(
            name="space_efficiency",
            description="Ability to accommodate all employees comfortably",
            weight=0.3,
            category=CriteriaCategory.OPERATIONAL,
            measurement_method="Square feet per employee",
            threshold=100.0  # minimum sq ft per employee
        ),
        DecisionCriteria(
            name="cost_effectiveness",
            description="Total cost including implementation and ongoing expenses",
            weight=0.25,
            category=CriteriaCategory.FINANCIAL,
            measurement_method="Total cost over 2 years",
            threshold=1000000.0  # maximum budget
        ),
        DecisionCriteria(
            name="implementation_impact",
            description="Level of disruption to current operations",
            weight=0.2,
            category=CriteriaCategory.OPERATIONAL,
            measurement_method="Estimated hours of disruption",
            threshold=40.0  # maximum hours of disruption
        ),
        DecisionCriteria(
            name="employee_satisfaction",
            description="Expected impact on employee satisfaction",
            weight=0.25,
            category=CriteriaCategory.SOCIAL,
            measurement_method="Projected satisfaction score (1-10)",
            threshold=7.0  # minimum satisfaction score
        )
    ]
    cycle.step2_establish_criteria(criteria)
    
    # Step 4: Generate Alternatives
    alternatives = [
        Alternative(
            name="Relocate",
            description="Relocate to a larger office",
            attributes={
                "cost": 2000000,
                "space": 15000,
                "disruption_hours": 80,
                "satisfaction_score": 8.5
            }
        ),
        Alternative(
            name="Redesign",
            description="Redesign current space",
            attributes={
                "cost": 500000,
                "space": 12000,
                "disruption_hours": 40,
                "satisfaction_score": 7.5
            }
        ),
        Alternative(
            name="Hybrid",
            description="Implement hybrid work model",
            attributes={
                "cost": 200000,
                "space": 10000,
                "disruption_hours": 20,
                "satisfaction_score": 8.0
            }
        )
    ]
    cycle.step4_generate_alternatives(alternatives)
    
    # Step 5: Evaluate Alternatives
    evaluations = [
        AlternativeEvaluation(
            alternative=alt,
            criteria_scores={
                "space_efficiency": alt.attributes["space"] / 100,  # space per employee
                "cost_effectiveness": 1 - (alt.attributes["cost"] / 2000000),  # normalized cost
                "implementation_impact": 1 - (alt.attributes["disruption_hours"] / 80),  # normalized disruption
                "employee_satisfaction": alt.attributes["satisfaction_score"] / 10  # normalized satisfaction
            },
            evaluation_notes=[f"Evaluated {alt.name} option"],
            evaluator="Decision Committee"
        ) for alt in alternatives
    ]
    scores = cycle.step5_evaluate_alternatives(evaluations)
    print("\nAlternative Scores:")
    for desc, score in scores.items():
        print(f"{desc}: {score:.2f}")
    
    # Step 6: Choose Best Alternative
    chosen = cycle.step6_choose_alternative()
    print(f"\nChosen Alternative: {chosen.name}")
    
    # Step 7: Implement Decision
    cycle.step7_implement_decision(
        implementation_plan="""
        Implementation Plan for Hybrid Work Model:
        1. Announce hybrid work policy to all employees
        2. Set up team rotation schedules
        3. Upgrade conference rooms for virtual collaboration
        4. Implement hot-desking system
        5. Provide necessary remote work equipment
        6. Establish communication protocols
        7. Review and adjust after 3 months
        """
    )
    
    # Step 8: Evaluate Decision
    outcome = DecisionOutcome(
        decision_id=cycle.cycle_id,
        implementation_date=datetime.now(),
        success_metrics={
            "employee_satisfaction": 8.5,
            "space_utilization": 0.85,
            "cost_savings": 300000,
            "productivity_index": 1.2
        },
        actual_outcomes={
            "remote_work_adoption": "75%",
            "office_capacity": "Never exceeds 60%",
            "collaboration_score": "8.2/10"
        },
        lessons_learned=[
            "Clear communication is crucial for hybrid model success",
            "Investment in collaboration tools pays off",
            "Regular feedback collection helps quick adjustments"
        ],
        follow_up_actions=[
            "Review space utilization monthly",
            "Survey employee satisfaction quarterly",
            "Assess technology needs ongoing"
        ]
    )
    cycle.step8_evaluate_decision(outcome)
    
    # Generate visualizations
    tree = cycle.visualizer.create_decision_tree(cycle)
    network = cycle.visualizer.create_evidence_network(cycle)
    dashboard = cycle.visualizer.create_progress_dashboard(cycle)
    
    # Save the cycle to a file
    cycle.save_to_file("office_space_decision.json")

if __name__ == "__main__":
    main()
