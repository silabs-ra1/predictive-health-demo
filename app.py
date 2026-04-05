import time
import pandas as pd
import streamlit as st
import plotly.express as px

from simulator import HealthDataSimulator
from analyzer import analyze_state

st.set_page_config(page_title="Predictive Health Demo", layout="wide")
st.title("AI Predictive Health Demo")

if "simulator" not in st.session_state:
    st.session_state.simulator = HealthDataSimulator()

if "data" not in st.session_state:
    st.session_state.data = []

if st.button("Start Simulation"):
    st.session_state.running = True

if "running" not in st.session_state:
    st.session_state.running = False

if st.session_state.running:
    sample = st.session_state.simulator.next_sample()
    st.session_state.data.append(sample)

df = pd.DataFrame(st.session_state.data)

if not df.empty:
    latest = df.iloc[-1].to_dict()
    state, risk = analyze_state(
        latest,
        df["voltage"].tolist(),
        df["latency"].tolist()
    )

    st.subheader(f"STATE: {state}")
    st.subheader(f"RISK SCORE: {risk}")

    st.plotly_chart(px.line(df, x="time", y="voltage", title="Voltage"))
    st.plotly_chart(px.line(df, x="time", y="latency", title="Latency"))

    time.sleep(1)
    st.rerun()