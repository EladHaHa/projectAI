import streamlit as st

tab1, tab2, tab3 = st.tabs(["Log In", "Home", "About"])

with tab1:
  st.write("היי")
with tab2:
  st.write("היי")
with tab3:
  st.write("היי")

with st.sidebar:
  st.title("תפריט")
  
  option = st.selectbox("Select Page", ["Log In", "Home"])

