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
                st.error(f"⚠ HIGH RISK ALERT — Score: {risk_score:.2f}")
            elif risk_score > THRESHOLD*0.6:
                st.warning(f"Moderate Risk — Score: {risk_score:.2f}")
            else:
                st.success(f"System Normal — Score: {risk_score:.2f}")


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