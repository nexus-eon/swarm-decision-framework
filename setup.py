"""Setup configuration for the decision framework package."""

from typing import Dict, List
from setuptools import setup, find_packages  # type: ignore

# Read version from a central location
VERSION = "1.1.0"

# Package requirements
INSTALL_REQUIRES: List[str] = [
    "typing>=3.7.4",
    "typing-extensions>=4.0.0",
    "dataclasses>=0.6",
    "networkx>=2.6.0",  # For decision visualization
    "numpy>=1.20.0",    # For numerical computations
    "pydantic>=2.0.0",  # For enhanced data validation
]

# Development requirements
DEV_REQUIRES: List[str] = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
    "black>=22.0.0",
    "isort>=5.0.0",
    "flake8>=4.0.0",
]

# Package metadata
CLASSIFIERS: List[str] = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Typing :: Typed",
]

setup(
    name="decision_framework",
    version=VERSION,
    author="Nexus",
    author_email="nexus@example.com",  # Replace with actual email if desired
    description="A comprehensive problem-solving and decision-making framework with AI capabilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev": DEV_REQUIRES,
    },
    classifiers=CLASSIFIERS,
    keywords="decision-making ai framework problem-solving analytics",
    project_urls={
        "Source": "https://github.com/nexus/decision-framework",  # Replace with actual URL
        "Documentation": "https://decision-framework.readthedocs.io",  # Replace with actual URL
    },
    zip_safe=False,
    include_package_data=True,
)
