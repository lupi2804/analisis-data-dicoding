import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Set style untuk visualisasi
sns.set(style='dark')

# Fungsi untuk membuat DataFrame rata-rata polutan
def create_pollutant_mean_df(df, pollutant):
    if pollutant not in df.columns:
        st.error(f"Kolom '{pollutant}' tidak ditemukan dalam dataset.")
        return None
    df_mean = df.groupby('station').agg({pollutant: 'mean'}).sort_values(by=pollutant, ascending=False).reset_index()
    return df_mean.rename(columns={'station': 'Kota', pollutant: 'Rata-Rata'})

# Fungsi untuk membuat DataFrame polutan
def create_pollutant_df(df):
    required_columns = ['TEMP', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Kolom berikut tidak ditemukan dalam dataset: {missing_columns}")
        return None
    return df[required_columns].rename(columns={'TEMP': 'Temperatur'})

# Fungsi untuk membuat DataFrame polutan per jam
def create_pollutant_hourly_df(df):
    required_columns = ['hour', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    if not all(col in df.columns for col in required_columns):
        st.error("Dataset tidak memiliki semua kolom yang diperlukan untuk perhitungan per jam.")
        return None
    return df.groupby('hour').mean().reset_index()

# Membaca dataset
df = None
try:
    df = pd.read_csv('dashboard/dataset_reduced.csv', encoding='utf-8')
except FileNotFoundError:
    st.error("Dataset tidak ditemukan. Pastikan file 'dataset.csv' tersedia.")
except pd.errors.EmptyDataError:
    st.error("Dataset kosong. Mohon periksa isinya.")
except pd.errors.ParserError:
    st.error("Terjadi kesalahan saat membaca dataset. Mohon periksa format CSV.")

if df is not None:
    datetime_columns = ['year', 'month', 'day', 'hour']
    if all(col in df.columns for col in datetime_columns):
        df[datetime_columns] = df[datetime_columns].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
        df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']], errors='coerce')
        if df['datetime'].isnull().sum() > 0:
            st.error("Beberapa data datetime tidak valid. Periksa dataset.")
    else:
        st.error("Kolom tahun, bulan, hari, atau jam tidak ditemukan dalam dataset.")

    if 'hour' in df.columns and pd.api.types.is_numeric_dtype(df['hour']):
        df['hour'] = df['hour'].astype(int)
    else:
        st.error("Kolom 'hour' tidak dalam format numerik.")

    # Membuat DataFrame untuk masing-masing polutan
    pollutant_dfs = {p: create_pollutant_mean_df(df, p) for p in ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']}
    pollutant_df = create_pollutant_df(df)
    pollutant_hourly = create_pollutant_hourly_df(df)

    # Dashboard Streamlit
    st.title('Proyek Analisis Data: Air Quality')
    st.caption('Silvi Dian Pramana | silvidianpramana@gmail.com')
    
    st.header('Project')
    st.write('Dataset yang digunakan untuk dashboard ini adalah dataset kualitas udara.')
    st.write(df.head(10))
    
    st.header('Konsentrasi Polusi Paling Tinggi')
    tabs = st.tabs(['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
    colors = ["#408ABF", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    for tab, (polutant, data) in zip(tabs, pollutant_dfs.items()):
        if data is not None:
            with tab:
                st.subheader(f'5 Kota dengan Konsentrasi {polutant} Tertinggi')
                fig, ax = plt.subplots(figsize=(18, 6))
                sns.barplot(x='Rata-Rata', y='Kota', data=data.head(5), palette=colors, ax=ax)
                ax.set_xlabel('Rata-Rata Konsentrasi (µg/m³)', fontsize=15)
                ax.set_ylabel(None)
                ax.tick_params(axis='y', labelsize=15)
                ax.tick_params(axis='x', labelsize=15)
                st.pyplot(fig)
                plt.close(fig)
    
    st.header('Rata-Rata Konsentrasi Polutan per Jam')
    if pollutant_hourly is not None:
        pollutant_hourly_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
        tabs = st.tabs(pollutant_hourly_cols)

        for tab, col in zip(tabs, pollutant_hourly_cols):
            with tab:
                st.subheader(f'Rata-Rata Konsentrasi {col} per Jam')
                fig, ax = plt.subplots(figsize=(18, 6))
                ax.plot(pollutant_hourly['hour'], pollutant_hourly[col], marker='o', linewidth=2)
                ax.set_xlabel('Jam', fontsize=15)
                ax.set_ylabel('Konsentrasi (µg/m³)', fontsize=15)
                ax.tick_params(axis='y', labelsize=15)
                ax.tick_params(axis='x', labelsize=15)
                plt.xticks(pollutant_hourly['hour'])
                st.pyplot(fig)
                plt.close(fig)
