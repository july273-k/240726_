 import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'path_to_your_file/daily_temp.csv'  # Update this to the correct path
data = pd.read_csv(file_path)

# Clean and preprocess the data
data['날짜'] = data['날짜'].str.strip()  # Remove leading/trailing whitespaces
data['날짜'] = pd.to_datetime(data['날짜'], format='%Y-%m-%d', errors='coerce')
data = data.dropna(subset=['날짜'])
data['연도'] = data['날짜'].dt.year

# Group by year and calculate mean, min, max for each year
yearly_stats = data.groupby('연도').agg({
    '평균기온(℃)': ['mean', 'min', 'max'],
    '최저기온(℃)': ['mean', 'min', 'max'],
    '최고기온(℃)': ['mean', 'min', 'max']
}).reset_index()

# Flatten the MultiIndex columns
yearly_stats.columns = ['연도', '평균기온_mean', '평균기온_min', '평균기온_max', 
                        '최저기온_mean', '최저기온_min', '최저기온_max',
                        '최고기온_mean', '최고기온_min', '최고기온_max']

# Streamlit app
st.title('Temperature Changes from 1907 to 2023')
chart_type = st.radio('Select Chart Type:', ['Line Chart', 'Bar Chart'])

# Plotting
fig, ax = plt.subplots(3, 1, figsize=(14, 18))

if chart_type == 'Line Chart':
    ax[0].plot(yearly_stats['연도'], yearly_stats['평균기온_mean'], label='Average Temp')
    ax[0].plot(yearly_stats['연도'], yearly_stats['평균기온_min'], label='Min Average Temp')
    ax[0].plot(yearly_stats['연도'], yearly_stats['평균기온_max'], label='Max Average Temp')
    ax[0].set_title('Yearly Average Temperature')
    ax[0].legend()

    ax[1].plot(yearly_stats['연도'], yearly_stats['최저기온_mean'], label='Average Min Temp')
    ax[1].plot(yearly_stats['연도'], yearly_stats['최저기온_min'], label='Min Min Temp')
    ax[1].plot(yearly_stats['연도'], yearly_stats['최저기온_max'], label='Max Min Temp')
    ax[1].set_title('Yearly Minimum Temperature')
    ax[1].legend()

    ax[2].plot(yearly_stats['연도'], yearly_stats['최고기온_mean'], label='Average Max Temp')
    ax[2].plot(yearly_stats['연도'], yearly_stats['최고기온_min'], label='Min Max Temp')
    ax[2].plot(yearly_stats['연도'], yearly_stats['최고기온_max'], label='Max Max Temp')
    ax[2].set_title('Yearly Maximum Temperature')
    ax[2].legend()

elif chart_type == 'Bar Chart':
    ax[0].bar(yearly_stats['연도'], yearly_stats['평균기온_mean'], label='Average Temp')
    ax[0].bar(yearly_stats['연도'], yearly_stats['평균기온_min'], label='Min Average Temp', alpha=0.5)
    ax[0].bar(yearly_stats['연도'], yearly_stats['평균기온_max'], label='Max Average Temp', alpha=0.5)
    ax[0].set_title('Yearly Average Temperature')
    ax[0].legend()

    ax[1].bar(yearly_stats['연도'], yearly_stats['최저기온_mean'], label='Average Min Temp')
    ax[1].bar(yearly_stats['연도'], yearly_stats['최저기온_min'], label='Min Min Temp', alpha=0.5)
    ax[1].bar(yearly_stats['연도'], yearly_stats['최저기온_max'], label='Max Min Temp', alpha=0.5)
    ax[1].set_title('Yearly Minimum Temperature')
    ax[1].legend()

    ax[2].bar(yearly_stats['연도'], yearly_stats['최고기온_mean'], label='Average Max Temp')
    ax[2].bar(yearly_stats['연도'], yearly_stats['최고기온_min'], label='Min Max Temp', alpha=0.5)
    ax[2].bar(yearly_stats['연도'], yearly_stats['최고기온_max'], label='Max Max Temp', alpha=0.5)
    ax[2].set_title('Yearly Maximum Temperature')
    ax[2].legend()

for axis in ax:
    axis.set_xlabel('Year')
    axis.set_ylabel('Temperature (℃)')
    axis.grid(True)

st.pyplot(fig)
