import pandas as pd
import numpy as np
import time
import os
import random

folders = [
    r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\incoming\enrollment",
    r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\incoming\biometric",
    r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\incoming\demographic"
]


for folder in folders:
    if os.path.exists(folder) and not os.path.isdir(folder):
          os.remove(folder)
    os.makedirs(folder, exist_ok=True)


while True:

    folder = random.choice(folders).strip()

    rows = np.random.randint(5,15)
    if folder == r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\incoming\enrollment":
      df = pd.DataFrame({
          "year": np.random.randint(2024,2027,rows),
          "month": np.random.randint(1,12,rows),
          "day": np.random.randint(1,31,rows),
          "state": np.random.randint(1,10,rows),
          "pincode": np.random.randint(1,10,rows),
          "age_0_5": np.random.randint(0,100,rows),
          "age_5_17": np.random.randint(0,100,rows),
          "age_18_greater": np.random.randint(0,100,rows),
          "district": np.random.randint(1,10,rows)
    })
    elif folder == r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\incoming\biometric":
      df = pd.DataFrame({
          "year": np.random.randint(2024,2027,rows),
          "month": np.random.randint(1,12,rows),
          "day": np.random.randint(1,31,rows),
          "state": np.random.randint(1,10,rows),
          "pincode": np.random.randint(1,10,rows),
          "bio_age_5_17": np.random.randint(0,100,rows),
          "bio_age_17_": np.random.randint(0,100,rows),
          "district": np.random.randint(1,10,rows)
    })
    elif folder == r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\incoming\demographic":
      df = pd.DataFrame({
          "year": np.random.randint(2024,2027,rows),
          "month": np.random.randint(1,12,rows),
          "day": np.random.randint(1,31,rows),
          "state": np.random.randint(1,10,rows),
          "pincode": np.random.randint(1,10,rows),
          "demo_age_5_17": np.random.randint(0,100,rows),
          "demo_age_17_": np.random.randint(0,100,rows),
          "district": np.random.randint(1,10,rows)
    })

    # randomly inject anomaly
    if random.random() < 0.3:
        df.loc[0,"district"] *= 5

    print("Saving to:", folder)
    print("Exists?", os.path.exists(folder))
    print("FOLDER =", folder)
    print("ABS PATH =", os.path.abspath(folder))
    print("EXISTS =", os.path.exists(folder))
    print("ISDIR =", os.path.isdir(folder))
    file = os.path.join(folder, f"data_{int(time.time())}.csv")
    df.to_csv(file,index=False)

    print("Generated:", file)

    time.sleep(5)