# System Architecture
## Source & Intake Layer
Job postings are discovered manually from high-signal job boards and company career pages. A
local Streamlit application serves as an intake interface, allowing users to paste job descriptions
and minimal metadata (URL, company, title, location, source).
## Parsing & Normalisation Layer
Python parsing logic processes the pasted job descriptions to infer seniority, work mode, role
family, and extract technical and soft skills using a curated skill dictionary and aliases. Raw
descriptions are preserved to allow reprocessing as extraction logic improves.
## Data Layer
PostgreSQL stores raw job data, normalised entities, and analytical outputs. The relational model
supports aggregation, filtering, and trend analysis across roles, locations, and companies.
## Data Layer Implementation
The data layer is implemented using PostgreSQL with a versioned SQL migration approach.

- Core and analytical tables are defined in:
```
db/schema/001_init.sql
```
- Core tables store raw and normalised job data.

- PostgreSQL runs locally via Docker Compose:
  `docker/docker-compose.yml`   

- Schema integrity is validated using a smoke test script that inserts a minimal end-to-end record set (company → job_posting → skill → job_skill):
  `db/schema/010_smoke_test.sql`  

- Analytical tables store persisted insight outputs to ensure reproducibility and performance.

- Raw job descriptions are preserved unchanged to support reprocessing as parsing logic evolves.  

This approach ensures a clear separation between ingestion, processing, and analytics, while keeping the implementation simple and auditable.
## Application & Delivery Layer
A FastAPI service exposes insight-driven endpoints, while a Streamlit dashboard enables
interactive exploration and live demonstrations. Generated reports translate analytical results into
business-facing outputs.
## Observability & Reliability
Basic logging, validation, and data quality checks ensure ingestion reliability and transparency
without introducing unnecessary infrastructure complexity.
## Repository Mapping (Implementation Structure)
Ingestion layer → ingestion/. Parsing & normalisation → processing/. Data layer → db/. Analytics
layer → analytics/. Delivery layer → api/ and dashboard/. Reporting → reports/. Packaging →
docker/. Documentation → docs/.