import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

#Title of the dashboard
st.title("🎵 Atlantic France Music Dashboard")

#Loading the dataset
df = pd.read_csv('Atlantic_France.csv')

#Data Cleaning and Preprocessing
df['song'] = df['Song'].fillna('Unknown')
df['duration_min'] = df['Duration_ms'] / 60000
df['date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
df['album_type'] = df['Album_type'].str.lower()

#Data Preview
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

#Data Analysis
st.subheader("🎯 Explicit vs Clean Content")

explicit_counts = df['Is_explicit'].value_counts(normalize=True) * 100

col1, col2 = st.columns(2)

with col1:
    st.metric("Explicit %", f"{explicit_counts.get(True, 0):.2f}%")

with col2:
    st.metric("Clean %", f"{explicit_counts.get(False, 0):.2f}%")

# Popularity Comparison
st.subheader("📈 Popularity Comparison")

popularity_comparison = df.groupby('Is_explicit')['Popularity'].mean()

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Explicit:** {popularity_comparison.get(True, 0):.1f}")

with col2:
    st.write(f"**Clean:** {popularity_comparison.get(False, 0):.1f}")

#Data Visualization
st.subheader("📊 Average Popularity Chart")

sns.set_theme(style="whitegrid")

fig, ax = plt.subplots(figsize=(8, 6))

sns.barplot(
    x=['Clean', 'Explicit'],
    y=[
        popularity_comparison.get(False, 0),
        popularity_comparison.get(True, 0)
    ],
    ax=ax
)

ax.set_title('Average Popularity of Explicit vs Clean Tracks')
ax.set_xlabel('Content Type')
ax.set_ylabel('Average Popularity Score')

st.pyplot(fig)

