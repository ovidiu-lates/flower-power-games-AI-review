# Flower Power Games - AI Review

Flower Power Games - AI Review helps people choose board games using insights
extracted from real player reviews. The application turns unstructured review
text into useful signals such as sentiment, perceived difficulty, liked
aspects, common complaints, average rating, and review counts.

The project is built as a React frontend backed by a FastAPI REST API. It is
currently designed to run locally and can later be integrated into the wider
Flower Power Games application.

## Application preview

The application contains the following main screens:

### Login and account creation

Users can log in or create an account. Registration validates the password and
the login form stores the returned access token for authenticated API requests.

<img width="1874" height="901" alt="image" src="https://github.com/user-attachments/assets/d0fa3e7e-8f34-4cf2-ba70-4ad46c4bf5bd" />

<img width="1621" height="906" alt="image" src="https://github.com/user-attachments/assets/d1cce971-443c-47e9-b2c8-40506dcbf1b4" />


### Discover games

The Discover page presents the game catalogue and its latest review insights.
Users can search by name, filter by player count, maximum play time, and
difficulty, and sort the results by rating or name.

<img width="1801" height="907" alt="image" src="https://github.com/user-attachments/assets/85fc2e76-59c6-42f1-aeae-d637a14f1bb4" />


### Game details and insights

Selecting a game opens its details page. The page shows game facts, the
community rating, the number of analyzed reviews, AI-generated insight panels,
and paginated player reviews.

<img width="1822" height="901" alt="image" src="https://github.com/user-attachments/assets/4686c435-37ee-458f-9da6-184c36cf5410" />

<img width="1630" height="913" alt="image" src="https://github.com/user-attachments/assets/45125e6d-95c0-4add-b02c-9cc282f72b27" />


### Write a review

The **Write a review** and **Add yours** buttons open a modal where an
authenticated user can choose a rating from 1 to 10, write a review, and
publish it.

<img width="1624" height="902" alt="image" src="https://github.com/user-attachments/assets/6a96b205-fa40-4bff-a157-d39606ea1786" />


### My reviews

The **My Reviews** navigation item shows the reviews published by the signed-in
user.

<img width="1673" height="911" alt="image" src="https://github.com/user-attachments/assets/f93256f7-2c16-4a91-85cf-ba951b94a4ce" />


---

## What users can do

- Create an account and sign in securely.
- Browse the available board-game catalogue.
- Search games by name from the navigation bar.
- Filter games by number of players, play time, and perceived difficulty.
- Sort games by community rating or name.
- Open a game to view its description, player limits, play time, rating, and
  review count.
- Read AI-generated insights about sentiment, difficulty, liked aspects, and
  common complaints.
- Read community reviews with pagination.
- Write and publish a personal review with a 1-10 rating.
- Review previously published feedback from the **My Reviews** page.
- Sign out from the profile menu.

## How the application works

1. A user signs in or creates an account from the frontend.
2. The React application sends authenticated requests to the FastAPI API.
3. Games and reviews are stored in SQL Server through SQLAlchemy.
4. Review analysis transforms text into structured sentiment, difficulty,
   themes, and complaint data.
5. Game-level insights aggregate the analyzed reviews and are displayed on the
   Discover and Game Details pages.
6. A new review refreshes the game's review list and available insights.

The frontend does not contain the analysis logic. It calls the API and renders
the responses, keeping the presentation and backend responsibilities separate.

## Technology stack

### Backend

- Python 3.13.15
- FastAPI and Uvicorn
- SQLAlchemy and Alembic
- Microsoft SQL Server (Docker)
- pandas for dataset preparation and import
- scikit-learn and OpenAI integrations for review analysis
- JWT authentication with Argon2 password hashing

### Frontend

- React 19
- TypeScript
- Vite
- React Router
- lucide-react icons

## Project structure

Only the most important areas are shown below:

```text
flower-power-games-AI-review/
├── src/smart_review_ai/
│   ├── main.py                 # FastAPI app, CORS, and API registration
│   ├── api/                    # Authentication, games, reviews, and health routes
│   ├── analysis/               # Review analysis and insight generation
│   ├── services/               # Application/business logic
│   ├── repositories/           # Database access
│   ├── models/                 # SQLAlchemy database models
│   ├── schemas/                # Request and response schemas
│   ├── core/                   # Configuration, security, and exceptions
│   └── db/                     # Database engine and session setup
├── frontend/
│   ├── src/pages/              # Login, Discover, Game Details, My Reviews
│   ├── src/components/         # Cards, insights, navigation, and review modal
│   ├── src/lib/                # API clients
│   ├── src/services/           # Authentication/session helpers
│   └── package.json
├── data/
│   ├── raw/                    # Downloaded Kaggle CSV files
│   └── processed/              # Prepared reviews
├── scripts/
│   ├── prepare_reviews.py      # Removes rows without review text
│   └── import_games.py         # Imports game data into SQL Server
├── migrations/                 # Alembic migration history
├── compose.yml                 # Local SQL Server container
├── pyproject.toml              # Python dependencies and project metadata
├── uv.lock                     # Locked Python dependency versions
└── README.md
```

## Requirements

Install the following before setting up the project:

- Git
- Python 3.13.15
- `uv`
- Node.js 20.19+ or 22.12+
- npm
- Docker Desktop (for SQL Server)

Check the installed tools:

```powershell
git --version
python --version
uv --version
node --version
npm.cmd --version
docker --version
```

## Installation and local setup

The commands below are written for Windows PowerShell. `npm.cmd` is used
explicitly because it works on Windows systems where the PowerShell execution
policy prevents the `npm` shim from running.

### 1. Clone the repository

```powershell
git clone <REPOSITORY_URL>
cd flower-power-games-AI-review
```

### 2. Install Python and synchronize the environment

```powershell
uv python install 3.13.15
uv sync
```

`uv sync` creates `.venv` and installs the versions recorded in `uv.lock`.
There is no need to activate the virtual environment when using `uv run`.

### 3. Configure environment variables

Copy the backend template:

```powershell
Copy-Item .env.example .env
```

Update `.env` with a strong SQL Server password and your OpenAI settings. The password in `DATABASE_URL` must be URL-encoded (`!` becomes `%21`, for example).
Never commit `.env` or API keys.

The frontend already has a template as well:

```powershell
Copy-Item frontend\.env.example frontend\.env
```

The default value is:

```text
VITE_API_BASE_URL=http://localhost:8000
```

### 4. Download the source datasets

Download the BoardGameGeek Reviews dataset from
[Kaggle](https://www.kaggle.com/datasets/jvanelteren/boardgamegeek-reviews).
Place these files in `data/raw/`:

```text
data/raw/bgg-15m-reviews.csv
data/raw/games_detailed_info2025.csv
```

The raw files are large and are intentionally not committed to the repository.

### 5. Prepare the review data

The preparation script keeps rows containing written review comments and
normalizes their text:

```powershell
uv run python scripts\prepare_reviews.py
```

It creates:

```text
data/processed/reviews_with_comments.csv
```

### 6. Start SQL Server and create the database

Start the local SQL Server container:

```powershell
docker compose up -d
```

The container is available at `localhost,1434`. Create a database named
`FlowerPowerGames` by connecting as `sa` from SQL Server Management Studio (or
another SQL client) and running:

```sql
CREATE DATABASE FlowerPowerGames;
```

Apply the migrations:

```powershell
uv run alembic upgrade head
```

Import the game catalogue:

```powershell
uv run python scripts\import_games.py
```

To import another CSV file:

```powershell
uv run python scripts\import_games.py path\to\games.csv
```

### 7. Install and start the backend

From the repository root:

```powershell
uv run uvicorn smart_review_ai.main:app --reload
```

The API is available at `http://localhost:8000`. Useful checks include:

- OpenAPI documentation: `http://localhost:8000/docs`
- Health endpoint: `http://localhost:8000/api/health`

### 8. Install and start the frontend

Open a second PowerShell window:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

The frontend is available at `http://localhost:5173`. Keep both the backend and
frontend terminals running while using the application.

## API overview

The backend mounts its routes under `/api`:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Check that the API is running |
| `POST` | `/api/auth/register` | Create a user account |
| `POST` | `/api/auth/login` | Log in and receive an access token |
| `GET` | `/api/auth/me` | Get the current authenticated user |
| `GET` | `/api/games` | Search, filter, sort, and paginate games |
| `GET` | `/api/games/{game_id}` | Get one game's details |
| `GET` | `/api/games/{game_id}/insight` | Get aggregated game insights |
| `GET` | `/api/games/{game_id}/reviews` | List reviews for a game |
| `POST` | `/api/games/{game_id}/reviews` | Publish a review |
| `GET` | `/api/reviews/mine` | List the current user's reviews |

For the complete request and response schemas, use the interactive Swagger UI
at `http://localhost:8000/docs`.

## Development commands

Run frontend type checking and the production build:

```powershell
cd frontend
npm.cmd run typecheck
npm.cmd run build
```

Run backend tests:

```powershell
uv run pytest
```

Format and lint Python code with Ruff:

```powershell
uv run ruff check .
```

## Database migrations

When a SQLAlchemy model changes, generate a migration and review it manually:

```powershell
uv run alembic revision --autogenerate -m "describe the schema change"
uv run alembic upgrade head
```

Commit migration files together with the model changes. Other developers only
need to pull the migration and run `uv run alembic upgrade head`.

## Stopping local services

Stop the SQL Server container without removing its data:

```powershell
docker compose down
```

To remove the container and its persisted volume as well, use this only when
you intentionally want to reset the local database:

```powershell
docker compose down -v
```

## Future improvements

- Add automated insight regeneration when new reviews are imported.
- Add review editing and deletion.
- Add richer game recommendations and personalized discovery.
- Add automated frontend and API integration tests.
- Add Docker services for the complete application.
