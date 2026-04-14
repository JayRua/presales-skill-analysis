import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="Job Viewer", layout="wide")

st.title("Job Postings Dashboard")

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="presales",
    user="presales",
    password="presales_pw"
)

# --- 1. Summary table ---
summary_query = """
SELECT
    jp.id,
    jp.title,
    c.company_name,
    jp.location,
    jp.source,
    jp.date_collected
FROM job_posting jp
JOIN company c ON c.id = jp.company_id
ORDER BY jp.id DESC;
"""

df = pd.read_sql(summary_query, conn)

st.subheader("All Jobs")
st.dataframe(df, use_container_width=True)

# --- 2. Select job ---
selected_job_id = st.selectbox(
    "Select a job to view full description",
    df["id"]
)

# --- 3. Fetch details ---
detail_query = """
SELECT
    jp.title,
    c.company_name,
    jp.raw_description,
    jp.source_url
FROM job_posting jp
JOIN company c ON c.id = jp.company_id
WHERE jp.id = %s;
"""

detail_df = pd.read_sql(detail_query, conn, params=(selected_job_id,))

# --- 4. Display description ---
if not detail_df.empty:
    row = detail_df.iloc[0]

    st.subheader(f"{row['title']} at {row['company_name']}")
    st.write(f"Source URL: {row['source_url']}")

    st.text_area(
        "Job Description",
        row["raw_description"],
        height=400
    )

conn.close()
