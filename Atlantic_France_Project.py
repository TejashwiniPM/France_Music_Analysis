import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Atlantic France Dashboard",
    layout="wide",
    page_icon="🎵"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: #ffffff;
}
[data-testid="stMetric"] {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown(
    "<h1 style='text-align: center; color: #00C853;'>🎵 Atlantic France Music Analytics</h1>",
    unsafe_allow_html=True
)

# -------------------- LOAD DATA --------------------
df = pd.read_csv('Atlantic_France.csv')

# -------------------- DATA CLEANING --------------------
df['song'] = df['Song'].fillna('Unknown')
df['duration_min'] = df['Duration_ms'] / 60000
df['date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
df['album_type'] = df['Album_type'].str.lower()

# -------------------- SIDEBAR --------------------
st.sidebar.header("🔍 Filters")

rank_filter = st.sidebar.selectbox("Rank Tier", ["Top 10", "Top 25", "Top 50"])
explicit_filter = st.sidebar.selectbox("Content Type", ["All", "Explicit", "Clean"])

if rank_filter == "Top 10":
    df = df[df['Position'] <= 10]
elif rank_filter == "Top 25":
    df = df[df['Position'] <= 25]

if explicit_filter == "Explicit":
    df = df[df['Is_explicit'] == True]
elif explicit_filter == "Clean":
    df = df[df['Is_explicit'] == False]

# -------------------- KPIs --------------------
explicit_share = df['Is_explicit'].mean() * 100
clean_ratio = (df['Is_explicit'] == False).sum() / max((df['Is_explicit'] == True).sum(), 1)
avg_duration = df['duration_min'].mean()
df['acceptance_score'] = df['Popularity'] / df['Position']
acceptance_score = df['acceptance_score'].mean()

st.markdown("### 📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎧 Explicit %", f"{explicit_share:.2f}%")
col2.metric("🧼 Clean Ratio", f"{clean_ratio:.2f}")
col3.metric("⏱ Avg Duration", f"{avg_duration:.2f} min")
col4.metric("⭐ Acceptance Score", f"{acceptance_score:.2f}")

st.markdown("---")

# -------------------- TABS --------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Content Analysis",
    "💿 Format Analysis",
    "⏱ Duration",
    "📀 Album Impact"
])

# -------------------- TAB 1 --------------------
with tab1:
    st.subheader("Explicit vs Clean Popularity")

    pop = df.groupby('Is_explicit')['Popularity'].mean()

    fig1, ax1 = plt.subplots()
    sns.barplot(
        x=['Clean', 'Explicit'],
        y=[pop.get(False, 0), pop.get(True, 0)],
        palette=['#00E676', '#FF1744'],
        ax=ax1
    )
    ax1.set_title("Popularity Comparison")
    st.pyplot(fig1)

# -------------------- TAB 2 --------------------
with tab2:
    st.subheader("Album vs Single Distribution")

    fig2, ax2 = plt.subplots()
    sns.countplot(
        data=df,
        x='album_type',
        palette='coolwarm',
        ax=ax2
    )
    st.pyplot(fig2)

# -------------------- TAB 3 --------------------
with tab3:
    st.subheader("Song Duration Distribution")

    fig3, ax3 = plt.subplots()
    sns.histplot(
        df['duration_min'],
        bins=20,
        kde=True,
        color='#00BFFF',
        ax=ax3
    )
    st.pyplot(fig3)

# -------------------- TAB 4 --------------------
with tab4:
    st.subheader("Album Size vs Popularity")

    fig4, ax4 = plt.subplots()
    sns.scatterplot(
        data=df,
        x='Total_tracks',
        y='Popularity',
        hue='Popularity',
        palette='viridis',
        size='Popularity',
        sizes=(20, 200),
        ax=ax4
    )
    st.pyplot(fig4)

# -------------------- INSIGHTS --------------------
st.markdown("---")
st.subheader("🧠 Key Insights")

if explicit_share < 30:
    st.success("✔ French audience prefers clean content")

if avg_duration >= 2.5 and avg_duration <= 4:
    st.info("ℹ Medium-duration songs perform best")

if df['Total_tracks'].corr(df['Popularity']) < 0:
    st.warning("⚠ Larger albums may dilute performance")

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("🚀 Built by Tejashwini | Atlantic France Music Analytics")
