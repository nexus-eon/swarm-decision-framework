# Swarm Decision Framework

[![CI](https://github.com/nexus-eon/swarm-decision-framework/actions/workflows/main.yml/badge.svg)](https://github.com/nexus-eon/swarm-decision-framework/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/nexus-eon/swarm-decision-framework/branch/main/graph/badge.svg)](https://codecov.io/gh/nexus-eon/swarm-decision-framework)

A powerful multi-agent AI system for intelligent decision-making using OpenAI's Swarm library.

## Features

- Multi-agent decision-making framework
- Integration with OpenAI's Swarm library
- Flexible and extensible architecture
- Strong focus on type safety and code quality

## Installation

```bash
pip install -r requirements.txt
```

## Development

This project uses Python 3.12 and follows strict type checking and code quality standards.

### Setup Development Environment

#### 1. Clone the repository

```bash
git clone git@github.com:nexus-eon/swarm-decision-framework.git
cd swarm-decision-framework
```

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Install development dependencies

```bash
pip install pytest pytest-cov mypy black flake8
```

### Running Tests

Run tests with coverage:

```bash
pytest --cov=src/decision_framework
```

### Code Quality

Run code formatters and linters:

```bash
black .
flake8 .
mypy src/decision_framework
```

## Project Structure

```text
src/decision_framework/
├── core/          # Core framework components
├── swarm/         # OpenAI Swarm integration
└── utils/         # Utility functions
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
