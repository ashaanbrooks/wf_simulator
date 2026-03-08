import streamlit as st

pg = st.navigation([st.Page("simulator.py", title = "Simulator"), st.Page("explanation.py", title = "How it works")])
pg.run()

