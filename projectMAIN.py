import streamlit as st

tab1, tab2, tab3 = st.tabs(["Log In", "Home", "About"])

with tab1:
  username = st.text_input("Username")
  password = st.text_input("Password", type="password")

  age = st.slider("Enter your age",0,100)

  if st.button("Log In"):
    if username == "" or password == "":
      st.warning("PLease enter a username/password")
    elif age<16:
      st.warning("Age must be over 16")
    else:  
      st.success(f"{username} is logged in")
  
with tab2:
  st.write(f"Welcome, {username}")

with tab3:
  st.write("היי")



