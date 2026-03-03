import pandas as pd
import joblib
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from preprocess import preprocess_clean


CONFIG = {
    "enrollment": {
        "folder": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\incoming\enrollment",
        "rf": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\models\e_rf_model.pkl",
        "iso": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\models\e_iso_model.pkl",
        "result": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\results\enrollment.csv"
    },
    "biometric": {
        "folder": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\incoming\biometric",
        "rf": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\models\b_rf_model.pkl",
        "iso": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\models\b_iso_model.pkl",
        "result": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\results\biometric.csv"
    },
    "demographic": {
        "folder": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\incoming\demographic",
        "rf": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\models\d_rf_model.pkl",
        "iso": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\models\d_iso_model.pkl",
        "result": r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\results\demographic.csv"
    }
}


# load models once
MODELS = {}
for key, val in CONFIG.items():
    MODELS[key] = {
        "rf": joblib.load(val["rf"]),
        "iso": joblib.load(val["iso"])
    }


def process(file, dataset):
    try:
        if not os.path.exists(file):
            return

        if os.path.getsize(file) == 0:
            return

        df = pd.read_csv(file)

    except Exception as e:
        print(f"Skipping {file}: {e}")
        return

    # same preprocessing as training
    clean = preprocess_clean(df)

    rf = MODELS[dataset]["rf"]
    iso = MODELS[dataset]["iso"]

    # -------- FEATURE ALIGNMENT FIX --------
    expected_cols = rf.feature_names_in_

    # add missing columns
    for col in expected_cols:
        if col not in clean.columns:
            clean[col] = 0

    # drop extra columns
    clean = clean[expected_cols]

    # ---------------------------------------

    X = clean
    y = clean.iloc[:, -1]

    pred = rf.predict(X)
    anomaly = iso.predict(X)

    out = pd.DataFrame({
        "dataset": dataset,
        "predicted": pred,
        "anomaly": anomaly,
        "actual": y,
        "difference": (y - pred).abs(),
    })

    file = CONFIG[dataset]["result"]

    if os.path.exists(file) and os.path.getsize(file) > 0:
        try:
           old = pd.read_csv(file)
           combined = pd.concat([old, out], ignore_index=True)
        except Exception:
           combined = out
    else:
         combined = out

    combined.to_csv(file, index=False)
    print(f"{dataset.upper()} processed:", file)


class Handler(FileSystemEventHandler):

    def __init__(self, dataset):
        self.dataset = dataset

    def on_created(self, event):
        if event.src_path.endswith(".csv"):
            time.sleep(0.5)
            process(event.src_path, self.dataset)


observer = Observer()

for name, cfg in CONFIG.items():
    if not os.path.exists(cfg["folder"]):
        os.makedirs(cfg["folder"])

for name, cfg in CONFIG.items():
    observer.schedule(Handler(name), cfg["folder"], recursive=False)

observer.start()

print("Monitoring all datasets...")

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()

observer.join()