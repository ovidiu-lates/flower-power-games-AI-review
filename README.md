# Smart Review AI

Smart Review AI analyzes BoardGameGeek review text and transforms unstructured reviews into structured game insights such as:

- Sentiment
- Perceived difficulty
- Common themes/aspects
- Common complaints
- Aggregated insights per game

The project is designed to run independently first and later be integrated with the Flower Power application through a small REST API.

---

## 1. Requirements

Install the following before setting up the project:

- Git
- Python 3.13.15
- `uv`
- Node.js 20.19+ or 22.12+
- npm

You can check Git with:

```bash
git --version
```

You can check Python with:

```bash
python --version
```

The expected Python version is:

```text
Python 3.13.15
```

You can check whether `uv` is installed with:

```bash
uv --version
```

---

## 2. Install `uv`

If `uv` is already installed, skip this step.

### Windows PowerShell

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen PowerShell, then verify:

```powershell
uv --version
```

---

## 3. Clone the repository

Clone the GitHub repository:

```bash
git clone <REPOSITORY_URL>
```

Move into the project directory:

```bash
cd smart-review-ai
```

Replace `<REPOSITORY_URL>` with the actual GitHub repository URL.

---

## 4. Install the required Python version

The project uses:

```text
Python 3.13.15
```

The required version is also stored in:

```text
.python-version
```

To make sure the correct Python version is available, run:

```bash
uv python install 3.13.15
```

Verify it with:

```bash
uv run python --version
```

Expected output:

```text
Python 3.13.15
```

---

## 5. Create and synchronize the virtual environment

Run:

```bash
uv sync
```

This command:

1. Creates `.venv` if it does not already exist.
2. Installs the dependencies from `pyproject.toml`.
3. Uses the exact dependency versions stored in `uv.lock`.

You do **not** need to commit `.venv` to GitHub.

You also do not need to manually activate the environment when using commands through `uv run`.

For example:

```bash
uv run python --version
```

runs Python inside the project environment automatically.

---

## 6. Project structure

The project is organized approximately like this:

```text
smart-review-ai/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── scripts/
│   └── prepare_reviews.py
│
├── src/
│   └── smart_review_ai/
│       ├── __init__.py
│       ├── main.py
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       │
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── sentiment.py
│       │   ├── difficulty.py
│       │   ├── themes.py
│       │   └── complaints.py
│       │
│       ├── aggregation/
│       │   ├── __init__.py
│       │   └── aggregator.py
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── review.py
│       │   ├── review_analysis.py
│       │   └── game_insights.py
│       │
│       └── services/
│           ├── __init__.py
│           └── review_service.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## 7. Download the BoardGameGeek dataset

The project uses the BoardGameGeek Reviews dataset from Kaggle:

```text
https://www.kaggle.com/datasets/jvanelteren/boardgamegeek-reviews
```

Download:

```text
bgg-15m-reviews.csv
games_detailed_info2025.csv
```

Download both files manually from the Kaggle dataset link above and place them
here:

```text
data/raw/bgg-15m-reviews.csv
data/raw/games_detailed_info2025.csv
```

The final location should be:

```text
smart-review-ai/
└── data/
    └── raw/
        ├── bgg-15m-reviews.csv
        └── games_detailed_info2025.csv
```

The raw datasets are intentionally not committed to GitHub because they are
large.

---

## 8. Prepare the review dataset

The raw BoardGameGeek dataset contains rows without written review comments.

The preprocessing script filters the dataset and keeps only rows where `comment` contains text.

Run:

```bash
uv run python scripts/prepare_reviews.py
```

The script reads:

```text
data/raw/bgg-15m-reviews.csv
```

and generates the processed file in:

```text
data/processed/
```

For example:

```text
data/processed/reviews_with_comments.csv
```

The preprocessing script should not modify the original raw dataset.

The intended data flow is:

```text
Kaggle dataset
      ↓
data/raw/bgg-15m-reviews.csv
      ↓
scripts/prepare_reviews.py
      ↓
data/processed/reviews_with_comments.csv
      ↓
Smart Review AI analysis pipeline
```

---

## 9. Configure and start the database

Copy the environment template:

```powershell
Copy-Item .env.example .env
```

Update `.env` with the SQL Server password you want to use. The password in
`DATABASE_URL` must be URL-encoded. For example, `!` becomes `%21`.

Start SQL Server with Docker:

```powershell
docker compose up -d
```

The container listens on `localhost:1434`. The first time you set up the
project, create the `FlowerPowerGames` database on that same SQL Server
instance. You can do this in SSMS by connecting to `localhost,1434` as `sa`
and running:

```sql
CREATE DATABASE FlowerPowerGames;
```

Make sure SSMS uses the same host, port, username, and password as `.env`.
Connecting to another local SQL Server instance will not make the database
available to this project.

Apply all migrations that are already committed to the repository:

```powershell
uv run alembic upgrade head
```

This creates or updates the tables in `FlowerPowerGames`.

### Import the game catalog

The game import CSV must be downloaded manually from the same Kaggle dataset
link in section 7 and saved as:

```text
data/raw/games_detailed_info2025.csv
```

After the database is running and migrations have been applied, run:

```powershell
uv run python scripts/import_games.py
```

The script imports the default CSV file, skips games that already exist, and
prints a summary of inserted, duplicate, and invalid rows. To import a
different CSV file, provide its path:

```powershell
uv run python scripts/import_games.py path\to\games.csv
```

---

## 10. Work with migrations

Run this sequence whenever you start working on the project:

```powershell
docker compose up -d
uv sync
uv run alembic upgrade head
```

When you change a SQLAlchemy model, generate a migration from the model
metadata:

```powershell
uv run alembic revision --autogenerate -m "describe the schema change"
```

Review the generated file in `migrations/versions/`. Autogeneration should be
checked manually, especially for renamed or removed columns. Then apply it:

```powershell
uv run alembic upgrade head
```

Commit the migration file with the model changes. Other developers should
pull the migration and run `uv run alembic upgrade head`; they should not
regenerate the same migration.

Useful migration commands:

```powershell
# Show the current database revision
uv run alembic current

# Show the migration history
uv run alembic history

# Roll back one migration locally
uv run alembic downgrade -1
```

Do not delete or edit an already-applied migration to correct a later change.
Create a new migration instead. If the database is disposable and you need a
clean local database, use `docker compose down -v`, start the container again,
recreate `FlowerPowerGames`, and run `uv run alembic upgrade head`.

---

## 11. Start the FastAPI application

Run:

```bash
uv run uvicorn smart_review_ai.main:app --reload --app-dir src
```

You should see output similar to:

```text
Uvicorn running on http://127.0.0.1:8000
```

Open the application in a browser:

```text
http://localhost:8000
```

### Start the React frontend

The frontend requires Node.js 20.19+ or 22.12+ and npm. After cloning the
repository or pulling frontend changes, open a second terminal and run:

```powershell
cd frontend
npm.cmd ci
Copy-Item .env.example .env
npm.cmd run dev
```

Open the frontend at:

```text
http://localhost:5173
```

The Vite development proxy forwards `/api/*` requests to the FastAPI backend
at `http://localhost:8000`. The minimal connectivity check uses `GET /api/health`
and expects `{"status":"ok"}`. On Windows, use `npm.cmd` if PowerShell blocks
the `npm` command.

For a production build, run these commands from `frontend/`:

```powershell
npm.cmd run typecheck
npm.cmd run build
```

---

## 12. Open the API documentation

FastAPI automatically generates interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

This page allows you to inspect and test the available API endpoints.

Current/planned endpoints include:

```text
GET  /health
```

---

## 13. Check the health endpoint

With the application running, open:

```text
http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## 14. Run the tests

Run all tests with:

```bash
uv run pytest
```

A successful run should finish without test failures.

Whenever possible, run the tests before opening a pull request.

---

## 15. Run the linter

Check the project with Ruff:

```bash
uv run ruff check .
```

To automatically fix issues that Ruff can safely correct:

```bash
uv run ruff check . --fix
```

Format the code with:

```bash
uv run ruff format .
```

Before opening a pull request, it is recommended to run:

```bash
uv run ruff check .
uv run pytest
```

---

## 16. Add a new dependency

Do not install project dependencies with plain `pip install`.

Use `uv add` instead.

For example:

```bash
uv add pandas
```

For a development-only dependency:

```bash
uv add --dev pytest
```

This updates:

```text
pyproject.toml
uv.lock
```

Commit both files when dependency changes are made.

---

## 17. Updating your local environment after pulling changes

When another teammate changes project dependencies, pull the latest changes:

```bash
git pull
```

Then run:

```bash
uv sync
```

This updates your local `.venv` so it matches the versions stored in `uv.lock`.

---

## 18. Environment variables

Local environment variables should be stored in:

```text
.env
```

Do not commit `.env`.

If the application needs a new environment variable, document its name in:

```text
.env.example
```

OpenAI review analysis uses these variables:

```text
OPENAI_API_KEY=replace-with-your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
```

`OPENAI_MODEL` is optional. If it is not set, the application uses `gpt-4o-mini`.

Never place passwords, API keys, tokens, or other secrets directly in Git-tracked files.

---

## 19. Files that should not be committed

The following should stay local:

```text
.venv/
.env
__pycache__/
.pytest_cache/
.ruff_cache/
data/raw/*.csv
data/processed/*.csv
```

The following should be committed:

```text
.python-version
pyproject.toml
uv.lock
README.md
frontend/
src/
scripts/
tests/
.env.example
```

---

## 20. Quick start

For a teammate setting up the project for the first time, the normal sequence is:

```bash
git clone <REPOSITORY_URL>
cd smart-review-ai

uv python install 3.13.15
uv sync
```

Download the BoardGameGeek dataset and place:

```text
bgg-15m-reviews.csv
```

inside:

```text
data/raw/
```

Prepare the data:

```bash
uv run python scripts/prepare_reviews.py
```

Run the tests:

```bash
uv run pytest
```

Start the API:

```bash
uv run uvicorn smart_review_ai.main:app --reload --app-dir src
```

In a second terminal, install and start the frontend:

```powershell
cd frontend
npm.cmd ci
Copy-Item .env.example .env
npm.cmd run dev
```

Then open the frontend:

```text
http://localhost:5173
```

The frontend uses `VITE_API_BASE_URL=http://localhost:8000`. Vite proxies
frontend requests from `/api` to the FastAPI backend, so the connectivity
check calls `/api/health` and expects `{"status":"ok"}`.

The API documentation remains available at:

```text
http://localhost:8000/docs
```

---

## 19. Main development pipeline

The project is intended to evolve toward the following flow:

```text
BoardGameGeek reviews
        ↓
Dataset preparation
        ↓
Sentiment analysis
        ↓
Difficulty classification
        ↓
Theme/aspect extraction
        ↓
Complaint detection
        ↓
Aggregation per game
        ↓
Game insights
        ↓
FastAPI
```

The initial version can work entirely from prepared local review data. Integration with the main Flower Power application can be added later through the API.
