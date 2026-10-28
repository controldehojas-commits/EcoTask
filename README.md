# EcoTask - Gestor de Tareas Sostenible

EcoTask is a lightweight task manager designed to help users organize daily activities with a sustainability lens. It stores records in JSON, supports CRUD operations, estimates a simple carbon footprint, and offers multilingual guidance in English and Spanish.

## Features

- CRUD for tasks
- JSON persistence in a portable file
- Impact levels: low, medium, high
- Carbon footprint simulation report
- Simple and accessible console interface
- Multilingual support: Spanish and English
- Sustainable suggestions such as public transport, recycling, and efficient planning
- Unit tests for core behavior

## Run locally

```bash
python main.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

- `ecotask/` - application package
- `tests/` - unit tests
- `data/tasks.json` - persisted task data

## Example task impact values

- low = 1 footprint point
- medium = 3 footprint points
- high = 5 footprint points
