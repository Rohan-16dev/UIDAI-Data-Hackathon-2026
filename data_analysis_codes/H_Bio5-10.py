import pandas as pd

df = pd.read_csv(r"C:\Users\mishr\Downloads\api_data_aadhar_biometric\api_data_aadhar_biometric\api_data_aadhar_biometric_500000_1000000.csv")
print("#info")
print(df.info())
print("#description")
print(df.describe())
df = df.rename(columns={
    'bio_age_5_17' : 'bio_u17',
    'bio_age_17_': 'bio_o17'
})
df['bio_total'] = df['bio_u17'] + df['bio_o17']
df[['bio_u17','bio_o17','bio_total']].head()
state_bio = df.groupby('state')['bio_total'].sum().sort_values(ascending=False)
print("#State wise biometric")
print(state_bio.head(10))
age_pattern = df[['bio_u17','bio_o17']].sum()
print("#age pattern")
print(age_pattern)
district_avg = df.groupby('district')['bio_total'].mean()
print("#district avg")
print(district_avg)

mean_val = district_avg.mean()
std_val = district_avg.std()

anomalous_districts = district_avg[district_avg > mean_val + std_val]
print("#anomalous districts")
print(anomalous_districts.head(10))
pincode_hotspots = (
    df.groupby('pincode')['bio_total']
      .mean()
      .sort_values(ascending=False)
      .head(10)
)
print("#pincode hotspots")
print(pincode_hotspots)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

monthly_trend = df.groupby(df['date'].dt.month)['bio_total'].sum()
print("#monthly trend")
print(monthly_trend)
state_median= df.groupby('state')['bio_total'].median()
state_sum= df.groupby('state')['bio_total'].sum()
print("#state sum & median")
print(state_sum)
print(state_median)
percent_share= 100*state_sum/state_sum.sum()
print("#percent share")
print(percent_share.sort_values(ascending=False))
monthly = df.groupby(df['date'].dt.month)['bio_total'].sum()
print("#monthly change")
print(monthly.pct_change()*100)
df['u17_ratio']=df['bio_u17']/df['bio_total']
Age_ratio= df.groupby('state')['u17_ratio'].mean()
print("#u17 ratio")
print(Age_ratio)
district_mean = df.groupby('district')['bio_total'].mean()
z_scores = (district_mean - district_mean.mean()) / district_mean.std()
print("#Z score anamoly")
print(z_scores[z_scores > 2])
Q1 = df['bio_total'].quantile(0.25)
Q3 = df['bio_total'].quantile(0.75)
IQR = Q3 - Q1
print("#inter quartile concentration")
print(df[df['bio_total'] > Q3 + 1.5 * IQR])
state_agg= df.groupby('state').agg({
    'bio_total': ['sum','mean','median','std']
})
print("#state statistics")
print(state_agg)

import matplotlib.pyplot as plt

state_bio.head(10).plot(kind='bar')
plt.title("Top 10 States by Biometric Updates")
plt.ylabel("Total Updates")
plt.show()
