.RECIPEPREFIX := >
.PHONY: install lint test eval schemas release-plan release-create cli-demo cli-smoke version audit health health smoke docker-build docker-run docker-smoke check run clean status

install:
>python -m pip install --upgrade pip
>python -m pip install -e ".[dev]"

lint:
>python -m ruff check .

test:
>python -m pytest

eval:
>python -m agentic_grant_proposal_builder.evaluation

schemas:
>python scripts/export_schemas.py

release-plan:
>python scripts/create_release.py

release-create:
>python scripts/create_release.py --execute

cli-demo:
>agpb build-scenario education_access

cli-smoke:
>python scripts/cli_smoke.py

version:
>python scripts/check_version.py

audit:
>python scripts/dependency_audit.py

health:
>python scripts/repo_health.py

smoke:
>python scripts/smoke_streamlit.py

docker-build:
>docker build -t agentic-grant-proposal-builder:local .

docker-run:
>docker run --rm -p 8501:8501 agentic-grant-proposal-builder:local

docker-smoke:
>python scripts/docker_smoke.py

check: lint test eval schemas release-plan release-create cli-demo cli-smoke version audit version audit health health health smoke docker-build docker-run docker-smoke

run:
>streamlit run src/agentic_grant_proposal_builder/app.py

clean:
>rm -rf .pytest_cache .ruff_cache reports/*.json reports/*.md reports/schemas
>find . -type d -name "__pycache__" -prune -exec rm -rf {} +

status:
>git status
