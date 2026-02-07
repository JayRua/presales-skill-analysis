# Job Market Analytics for Junior Solutions Engineers

## Overview
This project is a market intelligence and analytics platform designed to identify the key technical, cloud, and customer-facing skills companies hire for **junior and entry-level pre-sales / solutions engineering roles in Ireland**. It is intentionally framed as a **Solutions Engineer-style engagement**, covering discovery, solution design, implementation, and value delivery.

The scope and data sources are informed by real career guidance and reflect how junior SE roles are actually advertised in the Irish tech market.

## Problem Statement
Junior Solutions Engineers face fragmented and noisy signals across job boards, role titles, and company career pages. Hiring managers and candidates alike lack a consolidated, data-driven view of which skills, tools, and competencies truly matter at entry level.

## Target Role Titles
The system explicitly tracks and normalises the following role titles:

- Junior Solutions Engineer  
- Associate Solutions Engineer  
- Junior Pre-Sales Engineer  
- Pre-Sales Engineer (entry-level)  
- Sales Engineer (junior / technical)  
- Presales Consultant  
- Solutions Consultant (entry-level)  
- Technical Sales Engineer (junior)  
- Pre-Sales Solutions Consultant  
- Solution Consultant  
- Technical Consultant (pre-sales focus)  

## Job Boards & Data Sources
Job postings are sourced from high-signal platforms used by tech and SaaS companies in Ireland:

- LinkedIn Jobs  
- Indeed Ireland  
- IrishJobs.ie  
- Glassdoor.ie  
- Jobs.ie  
- BuiltInDublin.ie  
- Wellfound (AngelList Talent)  
- CareerJet.ie  
- Jobgether  
- PreSales Collective  
- Direct company career pages (e.g. Salesforce, Google, Intercom, Stripe, Okta, Gong)

## Solution
The platform ingests job postings, normalises skills and requirements, and exposes insights through structured SQL queries, APIs, dashboards, and generated reports.

## Architecture
Job postings are ingested via Python ETL pipelines, normalised and stored in a PostgreSQL relational database, queried through a FastAPI layer, and surfaced via an interactive Streamlit dashboard and generated reports.

## Tech Stack
- PostgreSQL
- Python
- SQL
- FastAPI
- Streamlit
- Docker

---
This project mirrors how Solutions Engineers approach real customer problems: discover, design, deliver, and explain value.

## Quickstart (Database)

Start PostgreSQL:

```bash
docker compose -f docker/docker-compose.yml up -d
```
Apply schema:
```
docker exec -i presales_db psql -U presales -d presales < db/schema/001_init.sql
```
Run smoke test:
```
docker exec -i presales_db psql -U presales -d presales < db/schema/010_smoke_test.sql
```
## Run ingestion (Streamlit)
Activate venv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Export DB env vars (example):
```
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=presales
export DB_USER=presales
export DB_PASSWORD=presales_pw
```
Run the intake app:
```
streamlit run ingestion/streamlit_intake.py
```
## Verify ingestion wrote to the database

After submitting a job via the Streamlit intake form, you can verify the record was persisted in PostgreSQL.

Run the following from the repo root:

```bash
docker exec -it presales_db psql -U presales -d presales -c "
SELECT
  jp.id,
  jp.title,
  c.company_name,
  jp.source,
  jp.source_url,
  jp.date_collected
FROM job_posting jp
JOIN company c ON c.id = jp.company_id
ORDER BY jp.id DESC
LIMIT 5;
"
```