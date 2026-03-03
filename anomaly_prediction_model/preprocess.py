import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_clean(df):

    df = df.copy()

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    df = df.drop_duplicates()

    # Date handling
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day
        df = df.drop(columns=["date"])

    # Missing values
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Remove Invalid Rows
    #Remove negative values 

    df[num_cols] = df[num_cols].clip(lower=0)

    # Drop rows where key columns missing 
    key_cols = ["state","district","pincode"]
    for col in key_cols :
           if col in df.columns : 
                 df = df[df[col].notna()]

    # Encoding
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    # Scaling
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    return df