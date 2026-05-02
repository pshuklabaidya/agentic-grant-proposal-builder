.RECIPEPREFIX := >
.PHONY: install lint test eval check run clean status

install:
>python -m pip install --upgrade pip
>python -m pip install -e ".[dev]"

lint:
>python -m ruff check .

test:
>python -m pytest

eval:
>python -m agentic_grant_proposal_builder.evaluation

check: lint test eval

run:
>streamlit run src/agentic_grant_proposal_builder/app.py

clean:
>rm -rf .pytest_cache .ruff_cache reports/*.json reports/*.md
>find . -type d -name "__pycache__" -prune -exec rm -rf {} +

status:
>git status
