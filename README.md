# ollie-cam

Raspberry Pi motion detection for tracking Ollie the cat, with a Mac-side data stack
(Kafka, Postgres, FastAPI ingestion, Airflow, Streamlit dashboard).

## Architecture

_TODO: diagram_

## Layout

```
ollie-cam/
├── docker-compose.yml   # Mac-side stack: kafka, postgres, api, consumer, airflow, streamlit
├── deploy.sh            # rsync + run on the Pi
├── pi/                  # runs on the Raspberry Pi
├── services/
│   ├── ingestion-api/   # FastAPI + Uvicorn
│   ├── kafka-consumer/  # Kafka -> Postgres
│   └── dashboard/       # Streamlit
├── airflow/             # DAGs: weather ingest, daily summary
├── sql/
│   ├── init/            # runs on first Postgres start
│   └── queries/         # reusable analysis queries
└── docs/
```

## How to run

1. `cp .env.example .env` and fill in values.
2. Mac stack: `docker compose up -d`
3. Pi: `./deploy.sh`

## Screenshots

_TODO_
