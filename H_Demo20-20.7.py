import pandas as pd

df = pd.read_csv(r"C:\Users\mishr\Downloads\api_data_aadhar_demographic\api_data_aadhar_demographic\api_data_aadhar_demographic_2000000_2071700.csv")
print("#Head")
print(df.head())
print("#info")
print(df.info())
print("#description")
print(df.describe())
df = df.rename(columns={
    'demo_age_5_17' : 'demo_u17',
    'demo_age_17_': 'demo_o17'
})
df['demo_total'] = df['demo_u17'] + df['demo_o17']
df[['demo_u17','demo_o17','demo_total']].head()
state_demo = df.groupby('state')['demo_total'].sum().sort_values(ascending=False)
print("#State demographic")
print(state_demo.head(10))
age_pattern = df[['demo_u17','demo_o17']].sum()
print("#age pattern")
print(age_pattern)
district_avg = df.groupby('district')['demo_total'].mean()
print("#district avg")
print(district_avg)

mean_val = district_avg.mean()
std_val = district_avg.std()

anomalous_districts = district_avg[district_avg > mean_val + std_val]
print("#anomalous districts")
print(anomalous_districts.head(10))
pincode_hotspots = (
    df.groupby('pincode')['demo_total']
      .mean()
      .sort_values(ascending=False)
      .head(10)
)
print("#pincode hotspots")
print(pincode_hotspots)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

monthly_trend = df.groupby(df['date'].dt.month)['demo_total'].sum()
print("#monthly trend")
print(monthly_trend)
state_median= df.groupby('state')['demo_total'].median()
state_sum= df.groupby('state')['demo_total'].sum()
print("#state sum & median")
print(state_sum)
print(state_median)
percent_share= 100*state_sum/state_sum.sum()
print("#percent share")
print(percent_share.sort_values(ascending=False))
monthly = df.groupby(df['date'].dt.month)['demo_total'].sum()
print("#monthly change")
print(monthly.pct_change()*100)
df['u17_ratio']=df['demo_u17']/df['demo_total']
Age_ratio= df.groupby('state')['u17_ratio'].mean()
print("#u17 ratio")
print(Age_ratio)
district_mean = df.groupby('district')['demo_total'].mean()
z_scores = (district_mean - district_mean.mean()) / district_mean.std()
print("#Z score anamoly")
print(z_scores[z_scores > 2])
Q1 = df['demo_total'].quantile(0.25)
Q3 = df['demo_total'].quantile(0.75)
IQR = Q3 - Q1
print("#inter quartile concentration")
print(df[df['demo_total'] > Q3 + 1.5 * IQR])
state_agg= df.groupby('state').agg({
    'demo_total': ['sum','mean','median','std']
})
print("#state statistics")
print(state_agg)

import matplotlib.pyplot as plt

state_demo.head(10).plot(kind='bar')
plt.title("Top 10 States by Demographic Updates")
plt.ylabel("Total Updates")
plt.show()
