# CSCE3444-FitnessAndNutritionTracker

Fitness and Nutrition Tracker for CSCE3444 - Fall 2025

# External Depencies
uv

# Installation
From within the project directory:
`uv venv` to recreate the virtual environment
It with print the command to use to activate the new environment once it's created. ex: 
```
Activate with: source .venv/bin/activate.fish
```

# Prep DB
```
uv run python3
from database import engine
from classes import Base
Base.metadata.create_all(engine)
```

# How to run
From within the project directory:
`uv run flask --app app run --debug` to run application
