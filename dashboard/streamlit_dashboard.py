import os
import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="Job Market Analytics", layout="wide")

st.title("Job Postings Dashboard")

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "presales"),
        user=os.getenv("DB_USER", "presales"),
        password=os.getenv("DB_PASSWORD", "presales_pw")
    )

try:
    conn = get_connection()

    # --- 1. Fetch Companies for Filter ---
    companies_query = "SELECT DISTINCT company_name FROM company ORDER BY company_name;"
    companies_df = pd.read_sql(companies_query, conn)
    companies = ["All"] + list(companies_df["company_name"])

    # --- 2. Layout Header and Company Filter ---
    # Using vertical_alignment="bottom" to align the subheader text with the selectbox
    col_head, col_filter = st.columns([3, 1], vertical_alignment="bottom")
    
    with col_filter:
        selected_company = st.selectbox("Filter by Company", companies)

    with col_head:
        st.subheader(f"Job Postings ({selected_company})" if selected_company != "All" else "All Job Postings")

    # --- 3. Fetch Filtered Job Postings ---
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
    """
    
    params = []
    if selected_company != "All":
        summary_query += " WHERE c.company_name = %s"
        params.append(selected_company)
        
    summary_query += " ORDER BY jp.id DESC;"
    
    df = pd.read_sql(summary_query, conn, params=params)

    # --- 4. Display Job Table ---
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- 5. Select job to view details ---
    if not df.empty:
        st.divider()
        st.subheader("Job Details")
        
        # Display ID, Title, and Company in the dropdown
        job_options = df.apply(lambda x: f"{x['id']} - {x['title']} ({x['company_name']})", axis=1).tolist()
        job_id_map = dict(zip(job_options, df["id"]))
        
        selected_option = st.selectbox(
            "Select a job to view full description",
            job_options
        )
        selected_job_id = job_id_map[selected_option]

        # --- 6. Fetch details ---
        detail_query = """
        SELECT
            jp.title,
            c.company_name,
            jp.raw_description,
            jp.source_url,
            jp.location,
            jp.date_collected,
            jp.source
        FROM job_posting jp
        JOIN company c ON c.id = jp.company_id
        WHERE jp.id = %s;
        """

        detail_df = pd.read_sql(detail_query, conn, params=(selected_job_id,))

        # --- 7. Display details ---
        if not detail_df.empty:
            row = detail_df.iloc[0]

            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### {row['title']}")
                st.markdown(f"**Company:** {row['company_name']}")
                st.markdown(f"**Location:** {row['location']}")
            with col2:
                st.markdown(f"**Source:** {row['source']}")
                st.markdown(f"**Collected on:** {row['date_collected']}")
                st.markdown(f"[View Original Listing]({row['source_url']})")

            st.text_area(
                "Full Job Description",
                row["raw_description"],
                height=500
            )
    else:
        st.info(f"No job postings found for '{selected_company}'.")

    conn.close()

except Exception as e:
    st.error(f"Error connecting to database or fetching data: {e}")
    st.info("Ensure the database is running and environment variables are set correctly.")
