import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('averages.csv')
df.columns = ['Date', 'Average']
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')
fig, ax = plt.subplots(figsize=(10,5))
plt.plot(df.index, df['Average'], linewidth=1)
plt.title('Radon levels over time', fontsize=20)
plt.xlabel('Date', fontsize=15)
plt.ylabel('Radon Level (Bq/m^3)', fontsize=15)
# ticks = list(df.index)
# plt.xticks(ticks, rotation=45)
plt.savefig('chart.svg')