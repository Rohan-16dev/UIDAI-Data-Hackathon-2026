import pandas as pd
import numpy as np
import time
import os
import random

folders = [
    r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\anomaly_prediction_model\incoming\enrollment",
    r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\anomaly_prediction_model\incoming\biometric",
    r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\anomaly_prediction_model\incoming\demographic"
]


for folder in folders:
    if os.path.exists(folder) and not os.path.isdir(folder):
          os.remove(folder)
    os.makedirs(folder, exist_ok=True)


while True:

    state_district_map = {

        "Bihar": [
        "Patna",
        "Gaya",
        "Muzaffarpur",
        "Bhagalpur",
        "Darbhanga"
        ],

        "West Bengal": [
        "Kolkata",
        "Howrah",
        "Durgapur",
        "Asansol",
        "Siliguri"
        ],

        "Maharashtra": [
        "Mumbai",
        "Pune",
        "Nagpur",
        "Nashik",
        "Aurangabad"
        ],

        "Tamil Nadu": [
        "Chennai",
        "Coimbatore",
        "Madurai",
        "Salem",
        "Tiruchirappalli"
        ],

        "Rajasthan": [
        "Jaipur",
        "Jodhpur",
        "Udaipur",
        "Kota",
        "Bikaner"
        ],

        "Uttar Pradesh": [
        "Lucknow",
        "Kanpur",
        "Varanasi",
        "Agra",
        "Prayagraj"
        ],

        "Gujarat": [
        "Ahmedabad",
        "Surat",
        "Vadodara",
        "Rajkot",
        "Bhavnagar"
        ],

        "Karnataka": [
        "Bengaluru",
        "Mysuru",
        "Hubli",
        "Mangaluru",
        "Belagavi"
        ],

        "Madhya Pradesh": [
        "Bhopal",
        "Indore",
        "Gwalior",
        "Jabalpur",
        "Ujjain"
        ],

        "Delhi": [
        "New Delhi",
        "South Delhi",
        "North Delhi",
        "East Delhi",
        "West Delhi"
        ]
     }

    state = random.choice(list(state_district_map.keys()))
    district = random.choice(state_district_map[state])

    pincode_map = {
    "Patna": "800001",
    "Gaya": "823001",
    "Muzaffarpur": "842001",
    "Bhagalpur": "834550",
    "Darbhanga": "822345",
    "Kolkata": "700001",
    "Howrah": "711101",
    "Durgapur": "703201",
    "Asansol": "700345",
    "Siliguri": "787001",
    "Mumbai": "400001",
    "Pune": "411001",
    "Nagpur": "800051",
    "Nashik": "800601",
    "Aurangabad": "845001",
    "Chennai": "600001",
    "Coimbatore": "707001",
    "Madurai": "706201",
    "Salem": "790001",
    "Tiruchirappalli": "702071",
    "Jaipur": "302001",
    "Jodhpur": "402001",
    "Udaipur": "400901",
    "Kota": "3230001",
    "Bikaner": "485001",
    "Lucknow": "403501",
    "Kanpur": "590001",
    "Varanasi":"600081",
    "Agra":"620081",
    "Prayagraj":"600046",
    "Ahmedabad":"600329",
    "Surat":"700081",
    "Vadodara":"606081",
    "Rajkot":"400081",
    "Bhavnagar":"600401",
    "Bengaluru":"602031",
    "Mysuru":"403081",
    "Hubli":"603881",
    "Mangaluru":"590081",
    "Belagavi":"600081",
    "Bhopal":"300081",
    "Indore":"600681",
    "Gwalior":"670081",
    "Jabalpur":"604781",
    "Ujjain":"667081",
    "New Delhi":"600781",
    "South Delhi":"600091",
    "North Delhi":"600921",
    "East Delhi":"600082",
    "West Delhi":"600085"
    
    }

    pincode = pincode_map.get(district)

    folder = random.choice(folders).strip()

    rows = np.random.randint(5,15)
    if folder == r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\anomaly_prediction_model\incoming\enrollment":
      df = pd.DataFrame({
          "year": np.random.randint(2024,2027,rows),
          "month": np.random.randint(1,12,rows),
          "day": np.random.randint(1,31,rows),
          "state": state,
          "district": district,
          "pincode": str(pincode),
          "age_0_5": np.random.randint(0,100,rows),
          "age_5_17": np.random.randint(0,100,rows),
          "age_18_greater": np.random.randint(0,100,rows)
         })
      
      if random.random() < 0.3:

         num_anomalies = np.random.randint(1,5)

         indices = np.random.choice(rows, num_anomalies, replace=False)
         factor = np.random.choice([0.2, 0.3, 0.5, 0.9, 2, 3, 5, 7, 8])
         df.loc[indices, "age_0_5"] *= factor
         df.loc[indices, "age_5_17"] *= factor
         df.loc[indices, "age_18_greater"] *= factor
      
    elif folder == r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\anomaly_prediction_model\incoming\biometric":
      df = pd.DataFrame({
          "year": np.random.randint(2024,2027,rows),
          "month": np.random.randint(1,12,rows),
          "day": np.random.randint(1,31,rows),
          "state": state,
          "district": district,
          "pincode": str(pincode),
          "bio_age_5_17": np.random.randint(0,100,rows),
          "bio_age_17_": np.random.randint(0,100,rows)
     })
      
      if random.random() < 0.3:

         num_anomalies = np.random.randint(1,5)

         indices = np.random.choice(rows, num_anomalies, replace=False)
         factor = np.random.choice([0.2, 0.3, 0.5, 0.9, 2, 3, 5, 7, 8])
         df.loc[indices, "bio_age_5_17"] *= factor
         df.loc[indices, "bio_age_17_"] *= factor
      
    elif folder == r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\anomaly_prediction_model\incoming\demographic":
      df = pd.DataFrame({
          "year": np.random.randint(2024,2027,rows),
          "month": np.random.randint(1,12,rows),
          "day": np.random.randint(1,31,rows),
          "state": state,
          "district": district,
          "pincode": str(pincode),
          "demo_age_5_17": np.random.randint(0,100,rows),
          "demo_age_17_": np.random.randint(0,100,rows)
    })
      
      if random.random() < 0.3:

         num_anomalies = np.random.randint(1,5)

         indices = np.random.choice(rows, num_anomalies, replace=False)
         factor = np.random.choice([0.2, 0.3, 0.5, 0.9, 2, 3, 5, 7, 8])
         df.loc[indices, "demo_age_5_17"] *= factor
         df.loc[indices, "demo_age_17_"] *= factor
      

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