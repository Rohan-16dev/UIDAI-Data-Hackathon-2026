import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("Predictive Early Warning System")

FILES = {
    "Enrollment":r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\results\enrollment.csv",
    "Biometric":r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\results\biometric.csv",
    "Demographic":r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\Anomaly Prediction Model\results\demographic.csv"
}

THRESHOLD = 0.50   # deviation threshold (50%)

placeholder = st.empty()


def load_all():
    dfs=[]
    for name,path in FILES.items():
        if os.path.exists(path):
           try:
             df=pd.read_csv(path)
             if df.empty:
                 continue
             
             df["dataset"]=name
             dfs.append(df)

           except Exception:
               continue
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sample_path = os.path.join(BASE_DIR, "sample_data.csv")
    # ---- FALLBACK TO STATIC SAMPLE ----
    if os.path.exists(sample_path):
         return pd.read_csv(sample_path)

    return None




data = load_all()

if data is not None:
        st.write("Columns detected:", list(data.columns))
        with placeholder.container():

            st.subheader("Live Monitoring Overview")

            col1,col2,col3 = st.columns(3)

            col1.metric("Total Records", len(data))
            if "anomaly" in data.columns:
                 anomalies = (data["anomaly"] == -1).sum()
            else:
                 anomalies = 0

            col2.metric("Total Anomalies", anomalies)
            if "difference" in data.columns and len(data) > 0:
                 avg_dev = round(data["difference"].mean(), 2)
            else:
                 avg_dev = 0

            col3.metric("Avg Deviation", avg_dev)


            # =====================================================
            # ANOMALY SCORE
            # =====================================================

            data["score"] = data["difference"] / (data["actual"]+1)
            risk_score = data["score"].mean()

            st.subheader("System Risk Score")

            if risk_score > THRESHOLD:
                 st.error(f"🔴 CRITICAL ALERT — Score: {risk_score:.2f}")

            elif risk_score > THRESHOLD * 0.8:
                 st.warning(f"🟠 HIGH RISK — Score: {risk_score:.2f}")

            elif risk_score > THRESHOLD * 0.5:
                 st.info(f"🟡 EARLY WARNING — Score: {risk_score:.2f}")

            else:
                 st.success(f"🟢 SYSTEM NORMAL — Score: {risk_score:.2f}")
            
            dataset_risk = data.groupby("dataset")["score"].mean().sort_values(ascending=False)
            top_dataset = dataset_risk.index[0]
            top_score = dataset_risk.iloc[0]

            st.subheader("Dataset Risk Contribution")

            st.warning(
            f"⚠️ Highest risk coming from **{top_dataset.upper()} dataset** — Score: {top_score:.2f}"
            )
            
            for dataset, score in dataset_risk.items():

               if score > THRESHOLD:
                     st.error(f"🔴 Critical anomaly in {dataset} dataset — Score {score:.2f}")

               elif score > THRESHOLD * 0.6:
                   st.warning(f"🟠 Elevated anomaly in {dataset} dataset — Score {score:.2f}")

            st.subheader("🚨 Dataset & Location Alerts")

            state_map = {
             1: "Bihar",
             2: "Maharashtra",
             3: "West Bengal",
             4: "UP",
             5: "Karnataka",
             6: "Tamil Nadu",
             7: "Delhi",
             8: "Gujarat",
             9: "Rajasthan"
             }

            district_map = {
             1: "Patna",
             2: "Mumbai",
             3: "Kolkata",
             4: "Lucknow",
             5: "Bangalore",
             6: "Chennai",
             7: "Delhi",
             8: "Ahmedabad",
             9: "Jaipur"
             }

            pincode_map = {
             1: "800001",
             2: "400001",
             3: "700001",
             4: "226001",
             5: "560001",
             6: "600001",
             7: "110001",
             8: "380001",
             9: "302001"
             }       

            data["state_name"] = data["state"].map(state_map)
            data["district_name"] = data["district"].map(district_map)
            data["pincode_name"] = data["pincode"].map(pincode_map) 

            data["deviation_percent"] = (
             (data["actual"] - data["predicted"]) / (data["predicted"] + 1)
             ) * 100
 
            def explain_anomaly(row):

                 dataset = row["dataset"]
                 state = row["state_name"]
                 district = row["district_name"]
                 deviation = row["deviation_percent"]

                 if deviation > 0:
                     return f"⚠️ Abnormal {dataset} spike detected in {district}, {state}. Activity is {abs(deviation):.1f}% higher than expected."

                 else:
                     return f"⚠️ Unexpected drop in {dataset} activity detected in {district}, {state}. Activity is {abs(deviation):.1f}% lower than expected."
                 
            alerts = data[data["anomaly"] == 1]

            if alerts.empty:
                 st.success("No anomalies detected across datasets.")
            else:
                 for _, row in alerts.tail(5).iterrows():

                     st.error(
                       f"""
                      🔴 **Anomaly Detected**

                       Dataset: **{row['dataset']}**

                       Location: **{row['district']}, {row['state']}**

                       Pincode: **{row['pincode']}**

                       Actual: **{row['actual']:.2f}**

                       Expected: **{row['predicted']:.2f}**

                       Deviation: **{row['difference']:.2f}**
                       """
                      )
             
            st.subheader("🚨 Intelligent Alerts")

            for _, row in alerts.tail(5).iterrows():

                 message = explain_anomaly(row)

                 st.error(message)        
            

            # =====================================================
            # TREND GRAPH 
            # =====================================================

            st.subheader("Actual vs Predicted Trend")

            fig,ax = plt.subplots()

            ax.plot(data["actual"].values,label="Actual")
            ax.plot(data["predicted"].values,label="Expected",linestyle="--")

            anomalies = data[data["score"]>THRESHOLD]

            ax.scatter(anomalies.index,
                       anomalies["actual"],
                       s=100,
                       label="Anomaly")

            ax.legend()
            st.pyplot(fig)


            # =====================================================
            # HEATMAP CORRELATION
            # =====================================================

            st.subheader("Feature Relationship Heatmap")

            numeric = data.select_dtypes(include=np.number)

            if len(numeric.columns)>1:
                fig2,ax2 = plt.subplots(figsize=(8,4))
                sns.heatmap(numeric.corr(),
                            annot=True,
                            cmap="coolwarm",
                            ax=ax2)
                st.pyplot(fig2)


            # =====================================================
            # DATASET COMPARISON
            # =====================================================

            st.subheader("Anomalies by Dataset")

            st.bar_chart(
                data.groupby("dataset")["anomaly"]
                .apply(lambda x:(x==-1).sum())
            )


           # ==================================
            # ERROR TREND ANIMATION
            # ==================================
            st.subheader("Deviation Trend (Live)")

            st.line_chart(data["difference"])


            # =====================================================
            # RAW DATA TABLE
            # =====================================================

            st.subheader("Processed Data")
            st.dataframe(data)
else:
    st.warning("Waiting for incoming data...")

time.sleep(5)
st.rerun()