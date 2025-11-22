# Design Patterns Repository

This repository contains implementations of various Design Patterns using Django, organized into three main categories: Creational, Structural, and Behavioral patterns.

## Repository Structure

```
design-patterns-django/
├── creational/              # Creational Patterns Django Project
│   ├── creational_patterns/ # Django project settings
│   ├── factory_pattern/     # Factory Method pattern app
│   ├── abstract_factory/    # Abstract Factory pattern app
│   ├── singleton/           # Singleton pattern app
│   ├── builder/             # Builder pattern app
│   ├── prototype/           # Prototype pattern app
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md
│
├── structural/              # Structural Patterns Django Project
│   ├── structural_patterns/ # Django project settings
│   ├── adapter/             # Adapter pattern app
│   ├── bridge/              # Bridge pattern app
│   ├── composite/           # Composite pattern app
│   ├── decorator/           # Decorator pattern app
│   ├── facade/              # Facade pattern app
│   ├── proxy/               # Proxy pattern app
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md
│
├── behavioral/              # Behavioral Patterns Django Project
│   ├── behavioral_patterns/ # Django project settings
│   ├── observer/            # Observer pattern app
│   ├── strategy/            # Strategy pattern app
│   ├── command/             # Command pattern app
│   ├── template_method/     # Template Method pattern app
│   ├── iterator/            # Iterator pattern app
│   ├── state/               # State pattern app
│   ├── chain_of_responsibility/ # Chain of Responsibility app
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md
│
└── README.md                # Main repository documentation
```

## Getting Started

Each category is a separate Django project. To work on a specific pattern category, navigate to its directory and follow the instructions in its `README.md`.

### Prerequisites

- Python 3.x
- Django 4.2+

### Installation

1.  Clone the repository.
2.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Navigate to the desired project directory (e.g., `creational`).
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Run migrations and start the server.

## Categories

- [Creational Patterns](creational/README.md)
- [Structural Patterns](structural/README.md)
- [Behavioral Patterns](behavioral/README.md)
