.RECIPEPREFIX := >
.PHONY: install lint test eval version health health smoke check run clean status

install:
>python -m pip install --upgrade pip
>python -m pip install -e ".[dev]"

lint:
>python -m ruff check .

test:
>python -m pytest

eval:
>python -m agentic_grant_proposal_builder.evaluation

version:
>python scripts/check_version.py

health:
>python scripts/repo_health.py

smoke:
>python scripts/smoke_streamlit.py

check: lint test eval version version health health health smoke

run:
>streamlit run src/agentic_grant_proposal_builder/app.py

clean:
>rm -rf .pytest_cache .ruff_cache reports/*.json reports/*.md
>find . -type d -name "__pycache__" -prune -exec rm -rf {} +

status:
>git status
