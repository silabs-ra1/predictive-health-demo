import time
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from simulator import HealthDataSimulator
from analyzer import analyze_state

st.set_page_config(page_title="AI Predictive Health Demo", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #08111f;
    }
    .title-text {
        font-size: 44px;
        font-weight: 800;
        color: white;
        margin-bottom: 8px;
    }
    .subtitle-text {
        font-size: 18px;
        color: #94a3b8;
        margin-bottom: 24px;
    }
    .panel {
        background-color: #111827;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #1f2937;
        box-shadow: 0 4px 18px rgba(0,0,0,0.25);
        margin-bottom: 16px;
    }
    .state-card {
        padding: 22px;
        border-radius: 18px;
        color: white;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-label {
        color: #9ca3af;
        font-size: 14px;
        margin-bottom: 6px;
    }
    .metric-value {
        color: white;
        font-size: 30px;
        font-weight: 800;
    }
    .small-value {
        color: white;
        font-size: 22px;
        font-weight: 700;
    }
    .reason-box {
        background-color: #0f172a;
        border-left: 4px solid #38bdf8;
        padding: 12px;
        border-radius: 10px;
        color: #e5e7eb;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">AI Predictive Health Demo</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle-text">Live AI-assisted health classification for smart embedded systems</div>',
    unsafe_allow_html=True
)

if "simulator" not in st.session_state:
    st.session_state.simulator = HealthDataSimulator()

if "data" not in st.session_state:
    st.session_state.data = []

if "running" not in st.session_state:
    st.session_state.running = False

top1, top2, top3 = st.columns([1, 1, 1])

with top1:
    if st.button("Start Simulation", use_container_width=True):
        st.session_state.running = True

with top2:
    if st.button("Stop Simulation", use_container_width=True):
        st.session_state.running = False

with top3:
    if st.button("Reset Demo", use_container_width=True):
        st.session_state.running = False
        st.session_state.simulator = HealthDataSimulator()
        st.session_state.data = []
        st.rerun()

if st.session_state.running:
    sample = st.session_state.simulator.next_sample()
    st.session_state.data.append(sample)

df = pd.DataFrame(st.session_state.data)

if df.empty:
    st.info("Click Start Simulation to begin the live demo.")
else:
    latest = df.iloc[-1].to_dict()
    result = analyze_state(
        latest,
        df["voltage"].tolist(),
        df["latency"].tolist()
    )

    state_color = result["color"]

    left, right = st.columns([1.2, 2])

    with left:
        st.markdown(
            f"""
            <div class="state-card" style="background: linear-gradient(135deg, {state_color}, #111827);">
                <div style="font-size:14px; opacity:0.9;">CURRENT SYSTEM STATE</div>
                <div style="font-size:34px; margin-top:8px;">{result["state"]}</div>
                <div style="font-size:16px; margin-top:10px;">Severity: {result["badge"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result["risk"],
            title={"text": "Health Risk Score"},
            gauge={
                "axis": {"range": [0, 18]},
                "bar": {"color": state_color},
                "steps": [
                    {"range": [0, 3], "color": "#16351f"},
                    {"range": [4, 8], "color": "#4a3410"},
                    {"range": [9, 18], "color": "#4b1d1d"}
                ],
                "threshold": {
                    "line": {"color": "white", "width": 4},
                    "thickness": 0.75,
                    "value": result["risk"]
                }
            }
        ))
        gauge.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=50, b=10),
            paper_bgcolor="#111827",
            font={"color": "white", "size": 16}
        )
        st.plotly_chart(gauge, use_container_width=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">AI Explanation</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="reason-box">{result["explanation"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="metric-label">Recommended Action</div><div class="small-value">{result["recommendation"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(
            f'<div class="panel"><div class="metric-label">Voltage</div><div class="metric-value">{latest["voltage"]} V</div></div>',
            unsafe_allow_html=True
        )
        m2.markdown(
            f'<div class="panel"><div class="metric-label">Latency</div><div class="metric-value">{latest["latency"]} ms</div></div>',
            unsafe_allow_html=True
        )
        m3.markdown(
            f'<div class="panel"><div class="metric-label">Retry Count</div><div class="metric-value">{latest["retry"]}</div></div>',
            unsafe_allow_html=True
        )
        m4.markdown(
            f'<div class="panel"><div class="metric-label">BOD Count</div><div class="metric-value">{latest["bod"]}</div></div>',
            unsafe_allow_html=True
        )

        fig_v = px.line(df, x="time", y="voltage", title="Voltage Trend")
        fig_v.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="white"),
            height=260
        )
        st.plotly_chart(fig_v, use_container_width=True)

        fig_l = px.line(df, x="time", y="latency", title="Latency Trend")
        fig_l.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="white"),
            height=260
        )
        st.plotly_chart(fig_l, use_container_width=True)

        bottom1, bottom2 = st.columns(2)

        with bottom1:
            fig_r = px.line(df, x="time", y="retry", title="Retry Trend")
            fig_r.update_layout(
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                font=dict(color="white"),
                height=240
            )
            st.plotly_chart(fig_r, use_container_width=True)

        with bottom2:
            fig_b = px.line(df, x="time", y="bod", title="BOD Warning Trend")
            fig_b.update_layout(
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                font=dict(color="white"),
                height=240
            )
            st.plotly_chart(fig_b, use_container_width=True)

        with st.expander("Show latest telemetry table"):
            st.dataframe(df.tail(12), use_container_width=True)

if st.session_state.running:
    time.sleep(1)
    st.rerun()