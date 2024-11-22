=================================
AI-Enhanced Decision Framework
=================================

:Author: Decision Framework Team
:Version: 1.1
:Purpose: Document project organization and file structure
:AI-Compatibility: Optimized for Cascade/Claude 3.5

Project Layout
============

.. code-block:: text

   expermient-01/
   ├── docs/
   │   ├── archive/
   │   │   ├── findings_archive.rst     # Historical development findings
   │   │   └── findings_v1.1_implemented.rst  # Implemented v1.1 features
   │   ├── markdown_to_rst_roadmap.rst  # Documentation conversion plan
   │   └── swarm_integration_plan.rst   # AI integration strategy
   ├── src/
   │   └── decision_framework/
   │       ├── __init__.py              # Package initialization
   │       └── problem_solving_cycle.py  # Core implementation
   ├── tests/
   │   ├── __init__.py                  # Test package initialization
   │   └── test_problem_solving_cycle.py # Framework test suite
   ├── environment.yml                   # Conda environment specification
   ├── example_usage.py                  # Framework usage examples
   ├── LICENSE                          # MIT License
   ├── office_space_problem.json        # Example problem definition
   ├── README.rst                       # Project documentation
   └── setup.py                         # Package configuration

Directory Contents
================

Source Code (``src/decision_framework/``)
-------------------------------------
* ``problem_solving_cycle.py``: Core implementation with enhanced type safety and AI capabilities
* ``__init__.py``: Package exports and version information

Documentation (``docs/``)
----------------------
* ``archive/``: Historical documentation and implemented features
  - ``findings_archive.rst``: Original development findings
  - ``findings_v1.1_implemented.rst``: Documentation of v1.1 features
* ``markdown_to_rst_roadmap.rst``: Plan for documentation format standardization
* ``swarm_integration_plan.rst``: Strategy for AI/ML integration

Tests (``tests/``)
---------------
* ``test_problem_solving_cycle.py``: Comprehensive test suite including:
  - Unit tests for core functionality
  - Integration tests for AI features
  - Performance benchmarks
  - Type safety verification

Configuration Files
----------------
* ``environment.yml``: Conda environment with all dependencies
* ``setup.py``: Package installation and metadata
* ``LICENSE``: MIT License terms

Example Files
-----------
* ``example_usage.py``: Demonstrates framework usage patterns
* ``office_space_problem.json``: Sample problem definition

Development Tools
--------------
* Mypy for static type checking
* Pytest for testing
* Black for code formatting
* Flake8 for linting
