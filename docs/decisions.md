# Design Decisions

## 2024-05-22: Dashboard Implementation and Filtering
**Context:** The initial "Job Viewer" (`dashboard/jobs_view.py`) was a minimal proof-of-concept for viewing jobs without SQL. Users needed more powerful ways to navigate the data as the volume of ingested jobs grew.

**Decision:**
- Replaced the minimal viewer with a more robust implementation in `dashboard/streamlit_dashboard.py`.
- Added a "Company Filter" at the top of the main area for quick data segmentation.
- Improved the job selection mechanism to only show jobs relevant to the current filter.
- Adopted `psycopg2` and `pandas` as the standard stack for dashboard data fetching.

**Rationale:**
- Placing the filter in the main area (next to the sub-heading) rather than the sidebar keeps the user's focus on the data and feels more integrated for a single-page analytics view.
- Dynamic dropdowns reduce "noise" when looking for a specific job within a large company's listings.
