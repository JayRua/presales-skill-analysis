import os
from datetime import date

import psycopg
import streamlit as st


def get_db_conn():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "presales"),
        user=os.getenv("DB_USER", "presales"),
        password=os.getenv("DB_PASSWORD", "presales_pw"),
    )


def upsert_company(cur, company_name: str, company_type: str | None, industry: str | None) -> int:
    cur.execute("SELECT id FROM company WHERE company_name = %s;", (company_name,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        """
        INSERT INTO company (company_name, company_type, industry)
        VALUES (%s, %s, %s)
        RETURNING id;
        """,
        (company_name, company_type, industry),
    )
    return cur.fetchone()[0]


def insert_job_posting(cur, company_id: int, data: dict) -> int:
    cur.execute(
        """
        INSERT INTO job_posting (
            company_id, title, raw_description, source, source_url,
            location, date_posted, date_collected
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (
            company_id,
            data["title"],
            data["raw_description"],
            data["source"],
            data["source_url"],
            data["location"],
            data["date_posted"],
            data["date_collected"],
        ),
    )
    return cur.fetchone()[0]


st.set_page_config(page_title="Job Intake", layout="centered")
st.title("Manual Job Intake")

with st.form("job_intake_form", clear_on_submit=True):
    st.subheader("Company")
    company_name = st.text_input("Company name *")
    company_type = st.selectbox("Company type (optional)", ["", "startup", "enterprise", "consultancy", "scale-up"])
    industry = st.text_input("Industry (optional)")

    st.subheader("Job posting")
    title = st.text_input("Job title *")
    source = st.selectbox("Source *", ["LinkedIn", "Indeed", "Company site", "Wellfound", "Other"])
    source_url = st.text_input("Job URL *")
    location = st.text_input("Location", value="Dublin")
    date_posted = st.date_input("Date posted (optional)", value=None)
    date_collected = st.date_input("Date collected *", value=date.today())
    raw_description = st.text_area("Full job description * (paste here)", height=250)

    submitted = st.form_submit_button("Save")

if submitted:
    errors = []
    if not company_name.strip():
        errors.append("Company name is required.")
    if not title.strip():
        errors.append("Job title is required.")
    if not source_url.strip():
        errors.append("Job URL is required.")
    if not raw_description.strip() or len(raw_description.strip()) < 200:
        errors.append("Job description is required (minimum 200 characters).")

    if errors:
        for e in errors:
            st.error(e)
        st.stop()

    try:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                company_id = upsert_company(
                    cur,
                    company_name.strip(),
                    company_type.strip() if company_type else None,
                    industry.strip() if industry else None,
                )

                job_id = insert_job_posting(
                    cur,
                    company_id,
                    {
                        "title": title.strip(),
                        "raw_description": raw_description.strip(),
                        "source": source,
                        "source_url": source_url.strip(),
                        "location": location.strip() if location else None,
                        "date_posted": date_posted,
                        "date_collected": date_collected,
                    },
                )

            conn.commit()

        st.success(f"Saved job posting. job_posting.id = {job_id}")
    except Exception as ex:
        st.error(f"Database error: {ex}")
