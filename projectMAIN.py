import streamlit as st

tab1, tab2 = st.tabs(["Log In", "Home"])

with tab1:
  username = st.text_input("Username")
  password = st.text_input("Password", type="password")
  age = st.slider("Enter your age",0,100)
  gender = ""
  gender = st.radio("Gender", ["Male", "Female", "Else"])

  
  test1, test2 = True, True
  if st.button("Log In"):
    if username == "" or password == "":
      st.warning("PLease enter a username/password")
      test1 = False
    if age<16:
      st.warning("Age must be over 16")
      test2 = False
    if gender == "":
      test2 = False
    elif test1 == True and test2 == True:  
      st.success(f"{username} is logged in")
  
with tab2:
  st.subheader(f"Welcome, {username}")




