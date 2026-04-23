import streamlit as st

tab1, tab2, tab3 = st.tabs(["Log In", "Home", "About"])

with tab1:
  username = st.text_input("Username")
  password = st.text_input("Password", type="password")

  if st.button("Log In"):
    st.success(f"{username} is logged in")
  )
with tab2:
  st.write("היי")
with tab3:
  st.write("היי")



