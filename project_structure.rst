=================================
AI-Enhanced Decision Framework
=================================

:Author: Decision Framework Team
:Version: 2.0
:Purpose: Document project organization and file structure
:AI-Compatibility: Optimized for OpenAI Swarm

Project Layout
============

.. code-block:: text

   expermient-01/
   ├── docs/
   │   ├── api/
   │   │   ├── swarm_api.rst           # OpenAI Swarm API documentation
   │   │   └── integration.rst         # Integration guidelines
   │   ├── architecture/
   │   │   ├── swarm_design.rst       # Swarm architecture design
   │   │   └── system_overview.rst     # System architecture overview
   │   └── examples/
   │       └── swarm_examples.rst      # Swarm usage examples
   ├── src/
   │   └── decision_framework/
   │       ├── __init__.py             # Package initialization
   │       ├── swarm/
   │       │   ├── __init__.py         # Swarm package initialization
   │       │   ├── agents.py           # Swarm agent definitions
   │       │   ├── coordinator.py      # Swarm coordination logic
   │       │   └── policies.py         # Swarm behavior policies
   │       ├── core/
   │       │   ├── __init__.py         # Core package initialization
   │       │   ├── problem.py          # Problem definition
   │       │   └── solution.py         # Solution processing
   │       └── utils/
   │           ├── __init__.py         # Utils package initialization
   │           ├── config.py           # Configuration management
   │           └── logging.py          # Logging utilities
   ├── tests/
   │   ├── __init__.py                # Test package initialization
   │   ├── test_swarm/                # Swarm-related tests
   │   │   ├── __init__.py
   │   │   ├── test_agents.py
   │   │   └── test_coordinator.py
   │   └── test_core/                 # Core functionality tests
   │       ├── __init__.py
   │       ├── test_problem.py
   │       └── test_solution.py
   ├── examples/
   │   ├── basic_usage.py             # Basic framework usage
   │   └── swarm_examples/            # Swarm-specific examples
   │       ├── collaborative_solving.py
   │       └── multi_agent_decision.py
   ├── environment.yml                # Conda environment specification
   ├── pyproject.toml                 # Project configuration (replaces setup.py)
   ├── LICENSE                        # MIT License
   └── README.rst                     # Project documentation

Directory Contents
================

Source Code (``src/decision_framework/``)
-------------------------------------
* ``swarm/``: OpenAI Swarm Integration
  - ``agents.py``: Individual swarm agent implementations
  - ``coordinator.py``: Swarm coordination and orchestration
  - ``policies.py``: Swarm behavior and decision policies

* ``core/``: Core Framework Components
  - ``problem.py``: Problem definition and analysis
  - ``solution.py``: Solution generation and evaluation

* ``utils/``: Utility Functions
  - ``config.py``: Configuration management
  - ``logging.py``: Logging and monitoring

Documentation (``docs/``)
----------------------
* ``api/``: API Documentation
  - ``swarm_api.rst``: OpenAI Swarm API reference
  - ``integration.rst``: Integration guidelines

* ``architecture/``: System Design
  - ``swarm_design.rst``: Detailed swarm architecture
  - ``system_overview.rst``: High-level system design

* ``examples/``: Usage Examples
  - ``swarm_examples.rst``: Swarm implementation examples

Tests (``tests/``)
---------------
* ``test_swarm/``: Swarm functionality tests
* ``test_core/``: Core framework tests

Examples (``examples/``)
--------------------
* ``basic_usage.py``: Basic framework usage examples
* ``swarm_examples/``: Advanced swarm-specific examples
