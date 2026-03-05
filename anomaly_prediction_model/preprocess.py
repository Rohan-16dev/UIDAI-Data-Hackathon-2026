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

    # Remove constant columns
    df = df.loc[:, df.nunique()>1]

    
    df = df.drop(columns=["state","district","pincode"], errors="ignore")
    
    # Remove Invalid Rows
    #Remove negative values 

    num_cols = [col for col in num_cols if col in df.columns]
    df[num_cols] = df[num_cols].clip(lower=0)
   
    # Scaling
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    return df