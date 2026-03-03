import pandas as pd
import glob
import joblib
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from preprocess import preprocess_clean
import os

os.makedirs("models", exist_ok=True)

files = glob.glob(r"C:\Enrollment-data\api_data_aadhar_enrolment\**\*.csv", recursive=True) #path to folder
enrollment_df =  pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
edf = preprocess_clean(enrollment_df)

files = glob.glob(r"C:\Biometric-data\api_data_aadhar_biometric\**\*.csv", recursive=True) #path to folder
biometric_df =  pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
bdf = preprocess_clean(biometric_df)

files = glob.glob(r"C:\Demographic-data\api_data_aadhar_demographic\**\*.csv", recursive=True) #path to folder
demographic_df =  pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
ddf = preprocess_clean(demographic_df)

edf = edf.sample(50000, random_state=42)
bdf = bdf.sample(50000, random_state=42)
ddf = ddf.sample(50000, random_state=42)

print("Enrollment shape:", edf.shape)
print("Biometric shape:", bdf.shape)
print("Demographic shape:", ddf.shape)
# Assume last column is target
eX = edf.iloc[:, :-1]
ey = edf.iloc[:, -1]

print("Script started")
# Random Forest → expected value prediction
rf = RandomForestRegressor(n_estimators=20) #Change to 200 later
print("Training Enrollment RF...")
rf.fit(eX, ey)

# Isolation Forest → anomaly detection
iso = IsolationForest(contamination=0.02)
print("Training Enrollment ISO...")
iso.fit(eX)

joblib.dump(rf, "models/e_rf_model.pkl")
joblib.dump(iso, "models/e_iso_model.pkl")

# Assume last column is target
bX = bdf.iloc[:, :-1]
by = bdf.iloc[:, -1]

# Random Forest → expected value prediction
rf = RandomForestRegressor(n_estimators=20) #Change to 200 later
print("Training Biometric RF...")
rf.fit(bX, by)

# Isolation Forest → anomaly detection
iso = IsolationForest(contamination=0.02)
print("Training Biometric ISO...")
iso.fit(bX)

joblib.dump(rf, "models/b_rf_model.pkl")
joblib.dump(iso, "models/b_iso_model.pkl")

# Assume last column is target
dX = ddf.iloc[:, :-1]
dy = ddf.iloc[:, -1]

# Random Forest → expected value prediction
rf = RandomForestRegressor(n_estimators=20) #Change to 200 later
print("Training Demographic RF...")
rf.fit(dX, dy)

# Isolation Forest → anomaly detection
iso = IsolationForest(contamination=0.02)
print("Training Demographic ISO...")
iso.fit(dX)

joblib.dump(rf, "models/d_rf_model.pkl")
joblib.dump(iso, "models/d_iso_model.pkl")

print("\n========== TRAINING COMPLETE ==========")
print("Enrollment rows:", len(edf))
print("Biometric rows:", len(bdf))
print("Demographic rows:", len(ddf))
print("Models saved in /models folder")
print("Models trained and saved.")