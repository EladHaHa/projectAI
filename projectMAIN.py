import streamlit as st
import pandas as pd
import numpy as np
import kagglehub
import os
path = kagglehub.dataset_download("rkiattisak/student-performance-in-mathematics")

print(os.listdir(path))

df = pd.read_csv(os.path.join(path, "exams.csv"))

gender_mapping = {'male': 0, 'female': 1}
df['gender'] = df['gender'].map(gender_mapping)

ethnic_mapping = {'group A': 0, 'group B': 1, 'group C': 2, 'group D': 3, 'group E': 4}
df['race/ethnicity'] = df['race/ethnicity'].map(ethnic_mapping)

parents_mapping = {'some college': 0, 'high school': 1, "associate's degree": 2, 'some high school': 3, "bachelor's degree": 4, "master's degree": 5}
df['parental level of education'] = df['parental level of education'].map(parents_mapping)

lunch_mapping = {'standard': 0, 'free/reduced': 1}
df['lunch'] = df['lunch'].map(lunch_mapping)

test_mapping = {'none': 0, 'completed': 1}
df['test preparation course'] = df['test preparation course'].map(test_mapping)



original_processed_df = df.copy()

from sklearn.model_selection import train_test_split

# X = המידע שניתן למודל
X = df[["gender", "race/ethnicity","parental level of education" ,"lunch","test preparation course"]]

# y = הערך שנרצה לחזות
y = df[["math score","reading score", "writing score"]]

# חלוקה לנתוני אימון ובדיקה
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training samples:", len(X_train))
print("Test samples:", len(X_test))

