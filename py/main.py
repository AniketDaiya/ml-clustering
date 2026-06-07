import asyncio
import sys

# --- THE FIX: Prevents the 'ConnectionResetError' on Windows Python 3.14+ ---
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.datasets import make_blobs

# --- Aesthetic GenZ Setup ---
st.set_page_config(page_title="Ultimate ML Vibe Check", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stSlider > div > div > div > div { background: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧩 The Ultimate Clustering Playground")
st.write("Sorting your squad into groups using **K-Means**, **DBSCAN**, and **Hierarchical** logic.")

# --- 1. Data Generation ---
if 'data' not in st.session_state:
    # Creating 'Hype Level' vs 'Chill Factor' scores
    X, _ = make_blobs(n_samples=500, centers=5, cluster_std=0.8, random_state=42)
    st.session_state.data = pd.DataFrame(X, columns=['Hype_Level', 'Chill_Factor'])

df = st.session_state.data.copy()

# --- 2. Control Center (Sidebar) ---
st.sidebar.header("🕹️ Algorithm Selection")
algo_choice = st.sidebar.selectbox(
    "Which logic are we using?", 
    ["K-Means (The Organizer)", "DBSCAN (The Mosh Pit)", "Hierarchical (The Family Tree)"]
)

# Logic branching for different algorithms
if "K-Means" in algo_choice:
    st.sidebar.markdown("### K-Means Settings")
    k = st.sidebar.slider("Number of Squads (K)", 2, 10, 5)
    model = KMeans(n_clusters=k, n_init=10)
    df['Squad'] = model.fit_predict(df[['Hype_Level', 'Chill_Factor']]).astype(str)
    description = "K-Means divides data into clean, circular groups. It's the standard way to group users."

elif "DBSCAN" in algo_choice:
    st.sidebar.markdown("### DBSCAN Settings")
    eps = st.sidebar.slider("Vibe Radius (Epsilon)", 0.1, 1.5, 0.5)
    min_s = st.sidebar.slider("Min Squad Size", 2, 10, 5)
    model = DBSCAN(eps=eps, min_samples=min_s)
    df['Squad'] = model.fit_predict(df[['Hype_Level', 'Chill_Factor']]).astype(str)
    description = "DBSCAN looks for density. It finds the real 'crowds' and ignores the loners (Noise)."

else:
    st.sidebar.markdown("### Hierarchical Settings")
    k_hier = st.sidebar.slider("Target Squads", 2, 10, 5)
    model = AgglomerativeClustering(n_clusters=k_hier)
    df['Squad'] = model.fit_predict(df[['Hype_Level', 'Chill_Factor']]).astype(str)
    description = "Hierarchical clustering builds a tree by joining the most similar points together."

# --- 3. Dashboard Display ---
col1, col2 = st.columns([3, 1])

with col1:
    fig = px.scatter(
        df, x='Hype_Level', y='Chill_Factor', color='Squad',
        template="plotly_dark", 
        title=f"Visualizing {algo_choice}",
        color_discrete_sequence=px.colors.qualitative.Alphabet
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💡 The Vibe Check")
    st.info(description)
    st.divider()
    st.write("**Real-Life Use Case:**")
    st.success("Targeting ads to specific 'interest squads' on social media.")

st.caption("Pro-tip: Try changing the 'Vibe Radius' in DBSCAN to see how 'Noise' points appear!")