# Zentask

A simple task lifecycle management application built with Python and Streamlit.

## AVISO
Esse e o codigo completo da atividade para materia de extensao , para usar o programa usa 
```bash 
cd zentask```

``` 
e segue o tutorial abaixo de ultilização normal

## Features

- Create, edit, and delete tasks
- Track task status (To Do, In Progress, Done, Paused)
- Defer tasks to future dates
- Audit trail for all changes
- Keyboard-first design

## Quick Start

1. Set up the virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python run.py
   ```

   Or run directly with Streamlit:
   ```bash
   PYTHONPATH=src streamlit run src/zentask/ui/app.py
   ```

## Development

Run tests:
```bash
pytest
```

## Architecture

- **MVC Pattern**: Models (data), Services (business logic), UI (Streamlit views)
- **In-memory storage** with JSON Lines audit log
- **Immutable audit trail** for all task mutations