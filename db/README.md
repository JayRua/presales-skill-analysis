# Database (PostgreSQL)

This project uses PostgreSQL running in Docker for a clean, reproducible local environment.

## Start the database

From repo root:

```bash
docker compose -f docker/docker-compose.yml up -d
```
Check it is running:
```
docker ps
```
## Apply the schema migration
From repo root:
```
docker exec -i presales_db psql -U presales -d presales < db/schema/001_init.sql
```
## Validate schema (quick inspection)
List tables:
```
docker exec -it presales_db psql -U presales -d presales -c "\dt"
```
Describe a table: 
```
docker exec -it presales_db psql -U presales -d presales -c "\d job_posting"
```
## Run smoke test data
From repo root:
```
docker exec -i presales_db psql -U presales -d presales < db/schema/010_smoke_test.sql
```
Verify relationships (example):
```
docker exec -it presales_db psql -U presales -d presales -c "
SELECT
  c.company_name,
  jp.title,
  s.skill_name,
  js.is_required
FROM job_skill js
JOIN job_posting jp ON jp.id = js.job_posting_id
JOIN company c ON c.id = jp.company_id
JOIN skill s ON s.id = js.skill_id
WHERE jp.source_url = 'https://example.com/job/1'
ORDER BY js.is_required DESC, s.skill_name;
"
```
## Stop the database
Stop containers:
```
docker compose -f docker/docker-compose.yml down
```
Warning: the following command deletes the database data volume. Do not try at home :):
```
docker compose -f docker/docker-compose.yml down -v
```
