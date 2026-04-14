import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

#Page Configuration
st.set_page_config(page_title="Atlantic France Dashboard", layout="wide")

#Title of the Dashboard
st.title("🎵 Atlantic France Music Analytics Dashboard")

#Loading the dataset
df = pd.read_csv('Atlantic_France.csv')

#Cleaning the dataset
df['song'] = df['Song'].fillna('Unknown')
df['duration_min'] = df['Duration_ms'] / 60000
df['date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
df['album_type'] = df['Album_type'].str.lower()

#Filters
st.sidebar.header("🔍 Filters")

rank_filter = st.sidebar.selectbox("Select Rank Tier", ["Top 10", "Top 25", "Top 50"])
explicit_filter = st.sidebar.selectbox("Explicit Filter", ["All", "Explicit Only", "Clean Only"])

# Rank filter
if rank_filter == "Top 10":
    df = df[df['Position'] <= 10]
elif rank_filter == "Top 25":
    df = df[df['Position'] <= 25]

# Explicit filter
if explicit_filter == "Explicit Only":
    df = df[df['Is_explicit'] == True]
elif explicit_filter == "Clean Only":
    df = df[df['Is_explicit'] == False]

#KPIs
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

explicit_share = df['Is_explicit'].mean() * 100
clean_ratio = (df['Is_explicit'] == False).sum() / max((df['Is_explicit'] == True).sum(), 1)
avg_duration = df['duration_min'].mean()

# Content Acceptance Score
df['acceptance_score'] = df['Popularity'] / df['Position']
acceptance_score = df['acceptance_score'].mean()

with col1:
    st.metric("Explicit Content %", f"{explicit_share:.2f}%")

with col2:
    st.metric("Clean Dominance Ratio", f"{clean_ratio:.2f}")

with col3:
    st.metric("Avg Duration (min)", f"{avg_duration:.2f}")

with col4:
    st.metric("Content Acceptance Score", f"{acceptance_score:.2f}")

#Charts and Insights
st.subheader("📈 Visual Insights")

col1, col2 = st.columns(2)

# Explicit vs Clean Popularity
with col1:
    fig1, ax1 = plt.subplots()
    pop = df.groupby('Is_explicit')['Popularity'].mean()
    sns.barplot(
        x=['Clean', 'Explicit'],
        y=[pop.get(False, 0), pop.get(True, 0)],
        ax=ax1
    )
    ax1.set_title("Explicit vs Clean Popularity")
    st.pyplot(fig1)

# Album vs Single
with col2:
    fig2, ax2 = plt.subplots()
    sns.countplot(data=df, x='album_type', ax=ax2)
    ax2.set_title("Album vs Single Distribution")
    st.pyplot(fig2)

#Duration Analysis
st.subheader("⏱ Duration Analysis")

fig3, ax3 = plt.subplots()
sns.histplot(df['duration_min'], bins=20, kde=True, ax=ax3)
ax3.set_title("Song Duration Distribution")
st.pyplot(fig3)

#Album Size Impact
st.subheader("📀 Album Size Impact")

fig4, ax4 = plt.subplots()
sns.scatterplot(data=df, x='Total_tracks', y='Popularity', ax=ax4)
ax4.set_title("Album Size vs Popularity")
st.pyplot(fig4)

#Insights
st.subheader("🧠 Key Insights")

if explicit_share < 30:
    st.success("✔ France shows strong preference for clean content")

if pop.get(False, 0) > pop.get(True, 0):
    st.success("✔ Clean songs are more popular than explicit songs")

if avg_duration >= 2.5 and avg_duration <= 4:
    st.success("✔ Medium-length songs perform best")

if df['Total_tracks'].corr(df['Popularity']) < 0:
    st.warning("⚠ Larger albums may dilute track performance")

#Footer 
st.markdown("---")
st.caption("Developed for Atlantic Recording Corporation | France Market Analysis")


