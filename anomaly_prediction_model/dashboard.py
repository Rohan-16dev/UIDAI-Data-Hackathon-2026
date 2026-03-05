import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

st.set_page_config(layout="wide")
st.title("Predictive Early Warning System")

FILES = {
    "Enrollment":r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\anomaly_prediction_model\results\enrollment.csv",
    "Biometric":r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\anomaly_prediction_model\results\biometric.csv",
    "Demographic":r"C:\Users\mishr\.vscode\Projects\UIDAI Hackathon\anomaly_prediction_model\results\demographic.csv"
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

        data["state_name"] = data["state"].round().clip(1,10).astype(int).map(state_map)
        data["district_name"] = data["district"].round().clip(1,10).astype(int).map(district_map)
        data["pincode_name"] = data["pincode"].round().clip(1,10).astype(int).map(pincode_map) 

        data["deviation_percent"] = (
        (data["actual"] - data["predicted"]) / (data["predicted"] + 1)
        ) * 100
        
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

            def generate_insight(data):

                total_anomalies = data["anomaly"].sum()

                if total_anomalies == 0:
                     return "System operating normally. No anomalies detected across monitored datasets."

                # dataset causing most anomalies
                dataset_risk = data[data["anomaly"] == 1]["dataset"].value_counts()

                if len(dataset_risk) > 0:
                     top_dataset = dataset_risk.index[0]
                else :
                     top_dataset = "Unknown"
                
                # most affected state
                state_risk = data[data["anomaly"] == 1]["state_name"].value_counts()

                if len(state_risk) > 0:
                     top_state = state_risk.index[0]
                else :
                     top_state = "Unknown"

                return (
                  f"Elevated anomaly activity detected. "
                  f"Most anomalies are originating from the **{top_dataset} dataset**. "
                  f"The region most affected is **{top_state}**. "
                  f"Monitoring recommended for unusual activity spikes."
                 )
 
            st.subheader("📊 System Insight Summary")

            insight = generate_insight(data)

            st.info(insight)

            # =====================================================
            # ANOMALY SCORE
            # =====================================================

            data["score"] = data["difference"] / (abs(data["actual"])+1)
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

                       Location: **{row['district_name']}, {row['state_name']}**

                       Pincode: **{row['pincode_name']}**

                       Actual: **{row['actual']:.2f}**

                       Expected: **{row['predicted']:.2f}**

                       Deviation: **{row['difference']:.2f}**
                       """
                      )
             
            st.subheader("🚨 Intelligent Alerts")

            for _, row in alerts.tail(5).iterrows():

                 message = explain_anomaly(row)

                 st.error(message)   

            # =========================================
            # CRITICAL ALERT LOG
            # =========================================

            st.subheader("🚨 Recent Critical Alerts")

            # Define critical threshold
            CRITICAL_THRESHOLD = THRESHOLD

            critical_alerts = data[data["score"] > CRITICAL_THRESHOLD]

            if critical_alerts.empty:
                st.success("No critical alerts recorded.")
            else:

                alert_table = critical_alerts[
                [
                 "dataset",
                 "state_name",
                 "district_name",
                 "pincode_name",
                 "actual",
                 "predicted",
                 "difference",
                 "score"
                ]
                ].sort_values("score", ascending=False).head(10)

                alert_table.columns = [
                 "Dataset",
                 "State",
                 "District",
                 "Pincode",
                 "Actual",
                 "Expected",
                 "Deviation",
                 "Risk Score"
                ]

                st.dataframe(alert_table, use_container_width=True)  

            
            # =====================================
            # TOP RISK LOCATIONS
            # =====================================

            st.subheader("! Top Risk Locations")

            anomaly_data = data[data["anomaly"] == 1]

            if anomaly_data.empty:
                st.success("No risky regions detected.")
            else:
     
                top_locations = (
                anomaly_data.groupby(["state_name","district_name"])
                .size()
                .sort_values(ascending=False)
                .head(5)
                )

                for i, ((state, district), count) in enumerate(top_locations.items(), start=1):
                     st.write(f"{i} **{district}, {state}** — {count} anomalies")
        
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

            state_coords = {
                "Bihar": [25.5941, 85.1376],
                "Maharashtra": [19.7515, 75.7139],
                "West Bengal": [22.9868, 87.8550],
                "UP": [26.8467, 80.9462],
                "Karnataka": [15.3173, 75.7139],
                "Tamil Nadu": [11.1271, 78.6569],
                "Delhi": [28.7041, 77.1025],
                "Gujarat": [22.2587, 71.1924],
                "Rajasthan": [27.0238, 74.2179]
                }



            map_data = data[data["anomaly"] == 1].copy()

            map_data["lat"] = map_data["state_name"].map(lambda x: state_coords.get(x, [None, None])[0])
            map_data["lon"] = map_data["state_name"].map(lambda x: state_coords.get(x, [None, None])[1])

            map_data = map_data.dropna(subset=["lat", "lon"])

            # =========================================
            # ANOMALY HOTSPOT MAP
            # =========================================

            st.subheader("🗺️ India Anomaly Hotspots")

            layer = pdk.Layer(
                "ScatterplotLayer",
                 data=map_data,
                 get_position="[lon, lat]",
                 get_radius="difference * 40000",
                 get_fill_color="[255, 0, 0, 160]",
                 pickable=True,
                )

            view_state = pdk.ViewState(
                latitude=22.9734,
                longitude=78.6569,
                zoom=4,
                pitch=0,
                )

            deck = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"text": "{dataset} anomaly in {state_name}"}
               )

            st.pydeck_chart(deck)   


            # =====================================================
            # RAW DATA TABLE
            # =====================================================

            st.subheader("Processed Data")
            st.dataframe(data)
else:
    st.warning("Waiting for incoming data...")

time.sleep(5)
st.rerun()