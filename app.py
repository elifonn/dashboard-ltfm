import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="IST Havalimanı Hava Panosu", layout="wide")

st.title("✈️ İstanbul Havalimanı (LTFM) Hava Panosu")
st.markdown("Açık kaynaklı Open-Meteo API verileriyle anlık ve saatlik hava durumu takibi.")

@st.cache_data(ttl=600)
def load_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 41.275,
        "longitude": 28.751,
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "hourly": ["temperature_2m", "precipitation_probability", "visibility"],
        "timezone": "Europe/Istanbul"
    }
    return requests.get(url, params=params).json()

data = load_data()
current = data["current"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Sıcaklık", f"{current['temperature_2m']} °C")
col2.metric("Rüzgar Hızı", f"{current['wind_speed_10m']} km/s")
col3.metric("Rüzgar Yönü", f"{current['wind_direction_10m']}°")
col4.metric("Yağış", f"{current['precipitation']} mm")

st.divider()

st.subheader("📈 24 Saatlik Sıcaklık Trendi")
hourly_data = data["hourly"]
df = pd.DataFrame({
    "Saat": hourly_data["time"][:24],
    "Sıcaklık": hourly_data["temperature_2m"][:24]
})
df["Saat"] = pd.to_datetime(df["Saat"]).dt.strftime('%H:%M')
df.set_index("Saat", inplace=True)

st.line_chart(df)
