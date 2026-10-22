# Customer Accounts Microservice

A Flask REST API for managing customer accounts, with automated tests, CI, security headers, Docker, Kubernetes manifests, and a Tekton pipeline scaffold.

[![CI](https://github.com/Anantjadhav1/github-final-project-/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/Anantjadhav1/github-final-project-/actions/workflows/ci-build.yaml)

## Stack
- Python 3.11, Flask, Flask-SQLAlchemy
- SQLite by default for local development; PostgreSQL can be configured with `DATABASE_URL`
- pytest, coverage, flake8
- Docker, Kubernetes, GitHub Actions, Tekton

## Run locally
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
flask --app service run --debug
```

The service listens on http://127.0.0.1:5000. Check `GET /` and `GET /accounts`.

## Test
```bash
pytest --cov=service --cov-report=term-missing
flake8 service tests
```

## API
- `POST /accounts` create an account
- `GET /accounts` list accounts
- `GET /accounts/<id>` read an account
- `PUT /accounts/<id>` update an account
- `DELETE /accounts/<id>` delete an account

Use the actual output from your own runs for graded evidence. Do not submit sample/fabricated terminal logs as if they were produced by your environment. The GitHub Actions badge turns green only after the workflow runs successfully on GitHub.
