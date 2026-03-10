import streamlit as st

pg = st.navigation([st.Page("simulator.py", title = "Simulator"), st.Page("explanation.py", title = "How it works"), st.Page("questions.py", title = "Questions"), st.Page("answers.py", title = "Answers")])
pg.run()

