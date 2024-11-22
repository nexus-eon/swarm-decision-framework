=================
Decision Framework
=================

|Python 3.8+| |License: MIT| |Code Style: Black|

.. |Python 3.8+| image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :target: https://www.python.org/downloads/
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
.. |Code Style: Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

:Author: Decision Framework Team
:Version: 1.0
:Purpose: Comprehensive problem-solving system
:AI-Compatibility: Optimized for Cascade/Claude 3.5

.. contents:: Table of Contents
   :depth: 3
   :local:

Overview
========
A comprehensive, flexible problem-solving system that captures complex decision processes through a programmatic and iterative approach. This framework combines cognitive science principles with systematic decision-making methodologies to provide a robust solution for complex problem-solving scenarios.

Key Features
===========

Core Functionality
----------------
* 8-step cyclical problem-solving process
* Evidence-based decision making
* Weighted scoring system for alternatives
* Comprehensive progress monitoring
* Detailed implementation tracking

Advanced Capabilities
-------------------
* Cognitive state tracking and mindfulness integration
* Collaborative decision features with multi-user support
* Historical decision pattern analysis
* Impact assessment metrics
* Validation and constraint checking

Technical Features
----------------
* Type-hinted implementation
* JSON serialization/deserialization
* Migration utilities
* Enum-based state management
* Comprehensive logging

Technical Requirements
====================
* Python 3.8+
* Required packages:

  * dataclasses
  * typing
  * json
  * enum
  * logging

Installation
===========

From Source
----------
.. code-block:: bash

    # Clone the repository
    git clone https://github.com/yourusername/decision-framework.git
    cd decision-framework

    # Install in development mode
    pip install -e .

Using pip
--------
.. code-block:: bash

    pip install decision-framework

Quick Start
==========
Here's a complete example demonstrating the key features of the framework:

.. code-block:: python

    from decision_framework import ProblemSolvingCycle
    from decision_framework.problem_solving_cycle import (
        CognitiveState,
        DiscussionType,
        Alternative,
        DecisionCriteria
    )

    def main():
        # Initialize a new decision cycle with a descriptive name
        cycle = ProblemSolvingCycle("Strategic Product Launch")

        # Step 1: Define the problem and context
        cycle.step1_identify_problem(
            statement="Determine optimal timing and strategy for new product launch",
            context="Competitive market with seasonal demand variations"
        )

        # Step 2: Track cognitive state for better decision quality
        cycle.add_cognitive_check(
            state=CognitiveState.CLEAR,
            clarity=0.8,
            stress=0.3,
            confidence=0.7,
            notes=["Team is well-prepared", "Market research is comprehensive"]
        )

        # Step 3: Define and evaluate alternatives
        cycle.add_alternative(
            Alternative(
                name="Q4 Launch",
                description="Launch product in Q4 2023",
                pros=["Peak seasonal demand", "Market readiness"],
                cons=["Heavy competition", "Higher marketing costs"]
            )
        )

        # Step 4: Set up evaluation criteria with weights
        cycle.add_criteria(
            DecisionCriteria(
                name="Market Timing",
                weight=0.4,
                description="Optimal market conditions for launch"
            )
        )

        # Step 5: Record team discussions and decisions
        cycle.record_discussion(
            type=DiscussionType.BRAINSTORMING,
            participants=["Product Manager", "Marketing Lead", "Sales Director"],
            topic="Launch Timeline Analysis",
            key_points=["Q4 shows highest demand", "Competitor launches in Q3"],
            decisions=["Target Q4 launch", "Begin marketing in Q3"],
            action_items=["Prepare marketing materials", "Set up distribution channels"]
        )

        # Export the decision cycle for documentation
        cycle.export_to_json("product_launch_decision.json")

    if __name__ == "__main__":
        main()

Project Structure
===============

.. code-block:: text

    decision_framework/
    ├── src/
    │   └── decision_framework/
    │       ├── __init__.py         # Package initialization with exports
    │       └── problem_solving_cycle.py  # Core implementation
    ├── docs/
    │   ├── findings-01.md          # Initial design and implementation
    │   ├── findings-02.md          # Decision-making flow improvements
    │   └── findings-03.md          # 7-step process integration
    ├── archive/
    │   ├── findings-01-archive.md  # Implemented features
    │   ├── findings-02-archive.md  # Completed cycle features
    │   └── findings-03-archive.md  # Completed process features
    ├── tests/                      # Test suite
    ├── example_usage.py            # Usage examples
    ├── setup.py                    # Package configuration
    └── LICENSE                     # MIT License

Documentation
============

.. _current-docs:

Current Documentation
-------------------
* ``findings-01.md``: Core design and implementation details
* ``findings-02.md``: Decision-making flow and improvements
* ``findings-03.md``: 8-step process integration

.. _archived-docs:

Archived Documentation
--------------------
* ``findings-01-archive.md``: Initial feature implementations
* ``findings-02-archive.md``: Completed cycle features
* ``findings-03-archive.md``: Completed process implementations

Future Roadmap
============

Advanced Analytics
---------------
* Historical decision pattern analysis
* Success rate tracking
* Impact assessment metrics
* Risk prediction models

Machine Learning Integration
-------------------------
* Decision outcome prediction
* Criteria weight optimization
* Alternative suggestion system

Visualization Tools
----------------
* Decision tree visualization
* Progress tracking charts
* Evidence strength visualization

Contributing
===========
1. Fork the repository
2. Create your feature branch (``git checkout -b feature/amazing-feature``)
3. Commit your changes (``git commit -m 'Add amazing feature'``)
4. Push to the branch (``git push origin feature/amazing-feature``)
5. Open a Pull Request

Development
==========
To set up the development environment:

.. code-block:: bash

    # Create and activate virtual environment
    python -m venv venv
    source venv/bin/activate

    # Install development dependencies
    pip install -r requirements-dev.txt

    # Run tests
    pytest

    # Check code style
    black .
    flake8

License
=======
This project is licensed under the MIT License - see the ``LICENSE`` file for details.
