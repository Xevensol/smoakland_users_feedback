import streamlit as st
import psycopg2,os
import pandas as pd


DB_PARAMS = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT")
}

def get_feedbacks(good_feedback):
     # SQL query to select data from feedback_info table
    select_query = """
    Select query, response, created_at 
    FROM public.feedback_info 
    WHERE feedback= %s;
    """
    
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                # Select the feedback record from the database
                cur.execute(select_query,(good_feedback,))
                records = cur.fetchall()
                df = pd.DataFrame(records, columns=['Query', 'Response', 'Created At'])
                return df
    except Exception as e:
        print(f"Error in fetching feedbacks: {e}")
        return e
    finally:
        if conn:
            cur.close()
            conn.close()
    

st.title("Smoakland Users Feedback")
# Create two buttons for feedback

col1, col2 = st.columns([500, 500])
feedback_data = None

with col1:

    if st.button("Good Feedback"):
        good_feedback = 'true'
        with st.spinner("Fetching good feedback..."):
            feedback_data = get_feedbacks(good_feedback)

with col2:

    if st.button("Bad Feedback"):
        good_feedback = 'false'
        with st.spinner("Fetching bad feedback..."):
            feedback_data = get_feedbacks(good_feedback)


if feedback_data is not None:
    if not feedback_data.empty:
        st.dataframe(feedback_data, width=800)
    else:
        st.write("No feedback available.")