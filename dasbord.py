import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page layout
st.set_page_config(layout="wide")
st.title("Dashboard Analisis Data Kualitas Udara")

# Load datasets
main_url = "https://raw.githubusercontent.com/lupi2804/analisis-data-dicoding/main/Dashbord/dataset_reduced.csv"
station_url = "https://raw.githubusercontent.com/lupi2804/analisis-data-dicoding/main/data/PRSA_Data_Aotizhongxin_20130301-20170228.csv"

df_main = pd.read_csv(main_url)
df_station = pd.read_csv(station_url)

st.sidebar.header("Filter Data")

# Display columns and sample data
st.subheader("Dataset Utama")
st.write("Jumlah baris:", df_main.shape[0])
st.write("Kolom:", df_main.columns.tolist())
st.dataframe(df_main.head())

# Create datetime column by combining year, month, day, and hour columns
if all(col in df_main.columns for col in ['year', 'month', 'day', 'hour']):
    df_main['timestamp'] = pd.to_datetime(df_main[['year', 'month', 'day', 'hour']])
else:
    st.error("Missing necessary columns ('year', 'month', 'day', 'hour') for creating timestamp.")
    st.stop()  # Stop execution if columns are missing

# Extract hour from timestamp for hourly analysis
df_main['hour'] = df_main['timestamp'].dt.hour

# Group by hour and calculate the average concentration of each pollutant
pollutant_hour_df = df_main.groupby(by='hour').agg({
    "PM2.5": 'mean',
    "PM10": 'mean',
    "NO2": 'mean',
    "SO2": 'mean',
    "CO": 'mean',
    "O3": 'mean'
}).reset_index()

# Show a table of pollutant_hour_df in the app
st.subheader("Rata-Rata Konsentrasi Polutan per Jam")
st.dataframe(pollutant_hour_df)

# Plot Barplot and Regplot for each pollutant

# Setup visual style
sns.set(style="whitegrid")
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

# Barplot: Rata-Rata Konsentrasi Polutan per Jam
st.subheader("Barplot: Rata-Rata Konsentrasi Polutan per Jam")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='hour', y='PM2.5', data=pollutant_hour_df, color='skyblue', ax=ax)
ax.set_title("Rata-Rata Konsentrasi PM2.5 per Jam", fontsize=16)
ax.set_xlabel("Jam (0-23)", fontsize=12)
ax.set_ylabel("Konsentrasi PM2.5", fontsize=12)
st.pyplot(fig)

# Regplot: Rata-Rata Konsentrasi Polutan vs Jam
st.subheader("Regplot: Rata-Rata Konsentrasi Polutan vs Jam")
fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(x='hour', y='PM2.5', data=pollutant_hour_df, scatter_kws={'s': 50, 'color': 'blue'}, line_kws={'color': 'red'}, ax=ax)
ax.set_title("Regplot: Konsentrasi PM2.5 vs Jam", fontsize=16)
ax.set_xlabel("Jam (0-23)", fontsize=12)
ax.set_ylabel("Konsentrasi PM2.5", fontsize=12)
st.pyplot(fig)

# Display more pollutant visualizations if necessary (you can repeat similar for other pollutants)
for pollutant in pollutants:
    st.subheader(f" {pollutant}: Rata-Rata Konsentrasi per Jam")
    
    # Barplot for each pollutant
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='hour', y=pollutant, data=pollutant_hour_df, color='skyblue', ax=ax)
    ax.set_title(f"Rata-Rata Konsentrasi {pollutant} per Jam", fontsize=16)
    ax.set_xlabel("Jam (0-23)", fontsize=12)
    ax.set_ylabel(f"Konsentrasi {pollutant}", fontsize=12)
    st.pyplot(fig)

    # Regplot for each pollutant
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='hour', y=pollutant, data=pollutant_hour_df, scatter_kws={'s': 50, 'color': 'blue'}, line_kws={'color': 'red'}, ax=ax)
    ax.set_title(f"Regplot: Konsentrasi {pollutant} vs Jam", fontsize=16)
    ax.set_xlabel("Jam (0-23)", fontsize=12)
    ax.set_ylabel(f"Konsentrasi {pollutant}", fontsize=12)
    st.pyplot(fig)

# Filter Data Section (Optional)
st.sidebar.header("Filter Data")

# Filter based on stasiun (station)
if 'station' in df_main.columns:
    station_options = df_main['station'].unique()
    selected_stations = st.sidebar.multiselect("Pilih Stasiun", options=station_options, default=station_options)
    df_main = df_main[df_main['station'].isin(selected_stations)]

# Display filtered data
st.subheader(" Data Setelah Filter")
st.dataframe(df_main)
