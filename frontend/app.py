import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import os
from datetime import datetime
import time

# Configure page
st.set_page_config(
    page_title="AI CyberSec SOC Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")

# Custom CSS for modern dark theme
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .metric-card {
        background-color: #1e212b;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #2d3748;
    }
    .metric-title {
        color: #a0aec0;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        color: #e2e8f0;
        font-size: 32px;
        font-weight: bold;
        margin-top: 10px;
    }
    .severity-high { color: #fc8181; }
    .severity-medium { color: #f6e05e; }
    .severity-low { color: #68d391; }
</style>
""", unsafe_allow_html=True)

# Helper functions
def fetch_stats():
    try:
        response = requests.get(f"{API_URL}/stats")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching stats: {e}")
    return {"total_threats_detected": 0, "high_severity_threats": 0, "system_status": "Offline", "threat_distribution": {}}

def fetch_live_threats():
    try:
        response = requests.get(f"{API_URL}/threats/live?limit=10")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching threats: {e}")
    return []

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/cyber-security.png", width=60)
    st.title("SOC Controls")
    
    st.markdown("---")
    
    st.subheader("Capture Engine")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ Start", use_container_width=True):
            requests.post(f"{API_URL}/capture/start")
            st.toast("Capture started")
    with col2:
        if st.button("⏹ Stop", use_container_width=True):
            requests.post(f"{API_URL}/capture/stop")
            st.toast("Capture stopped")
            
    st.markdown("---")
    
    st.subheader("ML Model")
    if st.button("🔄 Retrain Model", use_container_width=True):
        requests.post(f"{API_URL}/model/train")
        st.toast("Model retraining initiated")

# Main Dashboard
st.title("🛡️ Live Security Operations Center")

# Create a placeholder for auto-refreshing content
dashboard_placeholder = st.empty()

def render_dashboard():
    stats = fetch_stats()
    threats = fetch_live_threats()
    
    # Top Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">System Status</div>
            <div class="metric-value" style="color: #68d391;">{stats.get('system_status', 'Unknown')}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Threats</div>
            <div class="metric-value">{stats.get('total_threats_detected', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">High Severity</div>
            <div class="metric-value severity-high">{stats.get('high_severity_threats', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m4:
        capture_status = "Active" if stats.get('capture_active', False) else "Inactive"
        status_color = "#68d391" if capture_status == "Active" else "#fc8181"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Capture Engine</div>
            <div class="metric-value" style="color: {status_color};">{capture_status}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Threat Distribution")
        dist_data = stats.get('threat_distribution', {})
        if dist_data:
            df_dist = pd.DataFrame(list(dist_data.items()), columns=['Attack Type', 'Count'])
            fig_pie = px.pie(df_dist, values='Count', names='Attack Type', hole=0.4,
                             color_discrete_sequence=px.colors.sequential.Plasma)
            fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No threat data available for distribution.")
            
    with c2:
        st.subheader("Risk Score Gauge")
        # Display the most recent threat's risk score
        recent_score = 0.0
        if threats:
            recent_score = threats[0].get('risk_score', 0.0)
            
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = recent_score * 100,
            title = {'text': "Latest Threat Risk Score (%)"},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "red" if recent_score > 0.7 else "yellow" if recent_score > 0.4 else "green"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(104, 211, 145, 0.5)'},
                    {'range': [40, 70], 'color': 'rgba(246, 224, 94, 0.5)'},
                    {'range': [70, 100], 'color': 'rgba(252, 129, 129, 0.5)'}],
            }
        ))
        fig_gauge.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Live Threat Feed
    st.subheader("🔴 Live Threat Feed")
    if threats:
        df_threats = pd.DataFrame(threats)
        # Format the dataframe for display
        df_display = df_threats[['timestamp', 'source_ip', 'destination_ip', 'attack_type', 'severity', 'risk_score']]
        df_display['risk_score'] = df_display['risk_score'].apply(lambda x: f"{x:.2f}")
        
        # Color code severity
        def highlight_severity(s):
            if s == 'High': return 'background-color: #742a2a; color: white'
            elif s == 'Medium': return 'background-color: #744210; color: white'
            return 'background-color: #22543d; color: white'
            
        styled_df = df_display.style.map(highlight_severity, subset=['severity'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.info("No threats detected recently. System is secure.")

# Auto-refresh logic
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True

# We can put this in a while loop if we want continuous refresh, but Streamlit
# handles this better with st_autorefresh component or a button. For MVP, we'll use a simple approach.
render_dashboard()

if st.button("🔄 Refresh Data"):
    st.experimental_rerun()
