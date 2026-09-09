import streamlit as st

st.title("Test App")

st.write("Streamlit is working!")

name = st.text_input("Enter your name")

if st.button("Submit"):
    st.success(f"Hello {name}!")
