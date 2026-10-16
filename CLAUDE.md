# ollie-cam

Project context for Claude Code.

## Stack
- **Pi** (`pi/`): Python motion detection, posts events to the ingestion API.
- **Mac** (`docker-compose.yml`): Kafka, Postgres, FastAPI ingestion API, Kafka -> Postgres consumer, Airflow, Streamlit.

## Layout
- `pi/` — code that runs on the Raspberry Pi; deployed with `deploy.sh` (rsync).
- `services/<name>/` — one containerized Mac-side app per folder, each with its own `Dockerfile` and `requirements.txt`.
- `airflow/dags/` — `weather_ingest_dag.py`, `daily_summary_dag.py`.
- `sql/init/` — numbered schema scripts run on first Postgres start; `sql/queries/` — reusable analysis SQL.
- `docs/` — notes and diagrams.

## Conventions
- Secrets live in `.env` (gitignored); keep `.env.example` in sync with no real values.
- New SQL init scripts get the next number prefix (`003_...sql`).
