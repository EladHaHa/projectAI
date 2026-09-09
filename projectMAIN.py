import streamlit as st
import kagglehub
import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Age at Death Predictor",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 Age at Death Predictor")
st.write(
    "Enter information about a person to estimate their age at death."
)


# =========================================================
# DOWNLOAD DATASET
# =========================================================

@st.cache_data
def load_data():

    path = kagglehub.dataset_download(
        "imoore/age-dataset"
    )

    # Find CSV files
    csv_files = [
        file for file in os.listdir(path)
        if file.endswith(".csv")
    ]

    if len(csv_files) == 0:
        raise FileNotFoundError(
            "No CSV file was found in the downloaded dataset."
        )

    csv_path = os.path.join(path, csv_files[0])

    df = pd.read_csv(csv_path)

    return df


# Load dataset
try:

    df = load_data()

except Exception as e:

    st.error("Could not load the Kaggle dataset.")
    st.exception(e)
    st.stop()


# =========================================================
# SHOW DATASET INFORMATION
# =========================================================

st.subheader("Dataset")

st.write("Number of rows:", len(df))

with st.expander("Show dataset columns"):
    st.write(df.columns.tolist())

with st.expander("Show first rows"):
    st.dataframe(df.head())


# =========================================================
# FIND COLUMNS
# =========================================================

# Change these names if your dataset uses different names.

birth_column = None
death_column = None
gender_column = None
occupation_column = None
country_column = None


# Try to automatically find the columns

for column in df.columns:

    name = column.lower().strip()

    if "birth" in name and "year" in name:
        birth_column = column

    if "death" in name and "year" in name:
        death_column = column

    if "gender" in name or "sex" in name:
        gender_column = column

    if "occupation" in name:
        occupation_column = column

    if "country" in name:
        country_column = column


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

if birth_column is None or death_column is None:

    st.error(
        "I could not automatically find the Birth Year "
        "and Death Year columns."
    )

    st.write("Available columns:")
    st.write(df.columns.tolist())

    st.stop()


# =========================================================
# CREATE AGE AT DEATH
# =========================================================

df[birth_column] = pd.to_numeric(
    df[birth_column],
    errors="coerce"
)

df[death_column] = pd.to_numeric(
    df[death_column],
    errors="coerce"
)

df["AgeAtDeath"] = (
    df[death_column] - df[birth_column]
)


# =========================================================
# CLEAN DATA
# =========================================================

# Remove impossible ages
df = df[
    (df["AgeAtDeath"] >= 0) &
    (df["AgeAtDeath"] <= 120)
]


# =========================================================
# SELECT FEATURES
# =========================================================

feature_columns = []

numeric_features = []

categorical_features = []


# Birth year
feature_columns.append(birth_column)
numeric_features.append(birth_column)


# Gender
if gender_column is not None:

    feature_columns.append(gender_column)
    categorical_features.append(gender_column)


# Occupation
if occupation_column is not None:

    feature_columns.append(occupation_column)
    categorical_features.append(occupation_column)


# Country
if country_column is not None:

    feature_columns.append(country_column)
    categorical_features.append(country_column)


# =========================================================
# CLEAN SELECTED DATA
# =========================================================

model_df = df[
    feature_columns + ["AgeAtDeath"]
].copy()

model_df = model_df.dropna()


# =========================================================
# INPUT DATA
# =========================================================

st.subheader("Person Information")


# Birth year

birth_year = st.number_input(
    "Birth Year",
    min_value=1000,
    max_value=2026,
    value=1950,
    step=1
)


# Gender

if gender_column is not None:

    gender_options = sorted(
        df[gender_column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    gender = st.selectbox(
        "Gender",
        gender_options
    )


# Occupation

if occupation_column is not None:

    occupation_options = sorted(
        df[occupation_column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    occupation = st.selectbox(
        "Occupation",
        occupation_options
    )


# Country

if country_column is not None:

    country_options = sorted(
        df[country_column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    country = st.selectbox(
        "Country",
        country_options
    )


# =========================================================
# PREPARE MODEL
# =========================================================

X = model_df[feature_columns]

y = model_df["AgeAtDeath"]


# Train/test split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =========================================================
# PREPROCESSING
# =========================================================

transformers = []


if len(categorical_features) > 0:

    transformers.append(
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )
    )


if len(numeric_features) > 0:

    transformers.append(
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    )


preprocessor = ColumnTransformer(
    transformers=transformers
)


# =========================================================
# LINEAR REGRESSION MODEL
# =========================================================

model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "regressor",
            LinearRegression()
        )
    ]
)


# Train model

model.fit(
    X_train,
    y_train
)


# =========================================================
# MODEL ACCURACY
# =========================================================

test_predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    test_predictions
)


# =========================================================
# PREDICTION
# =========================================================

if st.button(
    "🔮 Predict Age at Death",
    type="primary"
):

    # Create input dictionary

    person = {
        birth_column: birth_year
    }


    if gender_column is not None:

        person[gender_column] = gender


    if occupation_column is not None:

        person[occupation_column] = occupation


    if country_column is not None:

        person[country_column] = country


    # Convert to DataFrame

    input_data = pd.DataFrame(
        [person]
    )


    # Make prediction

    prediction = model.predict(
        input_data
    )


    predicted_age = round(
        prediction[0],
        1
    )


    # =====================================================
    # OUTPUT
    # =====================================================

    st.success(
        f"Estimated age at death: {predicted_age} years"
    )


    st.info(
        f"Model Mean Absolute Error: {mae:.2f} years"
    )


    st.warning(
        "This is a statistical estimate based on "
        "historical data, not a medical prediction."
    )


# =========================================================
# MODEL INFORMATION
# =========================================================

with st.expander("Model information"):

    st.write(
        "Algorithm: Linear Regression"
    )

    st.write(
        "Target: Age at death"
    )

    st.write(
        "Features used:"
    )

    for column in feature_columns:

        st.write(
            f"- {column}"
        )
