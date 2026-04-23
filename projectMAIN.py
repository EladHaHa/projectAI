import streamlit as st

st.title("AI Project")

st.subheader("description")

name = st.text_input("מה שמך")

st.write(name)

st.button("לחץ עליי")

tab1, tab2, tab3 = st.tabs(["Log In", ["Home"], ["About"])

with tab1:
  st.write("היי")
with tab2:
  st.write("היי")
with tab3:
  st.write("היי")


