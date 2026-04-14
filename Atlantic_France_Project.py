import pandas  as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
st.title("Hello, Streamlit!")

#Loading the dataset  
df  = pd.read_csv('Atlantic_France.csv')

#Analytics 1: Handling the misssing values.
df['song'] = df['song'].fillna('Unknown')

#Analytics 2:  Convert time.
df['duration_min'] = df['duration_ms'] / 60000

#Analytics 3:  Date Parsing
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

#Analytics 4:  Standardize Labels
df['album_type'] = df['album_type'].str.lower()

#Calculating the % of Explicit vs Clean tracks
explicit_counts = df['is_explicit'].value_counts(normalize=True) * 100
print("Explicit Content Share:")
print(f"Explicit: {explicit_counts[True]:.2f}%")
print(f"Clean: {explicit_counts[False]:.2f}%")

#Compare average popularity scores
popularity_comparison = df.groupby('is_explicit')['popularity'].mean()
print("\nAverage Popularity Comparison:")
print(f"Average Popularity (Explicit): {popularity_comparison[True]:.1f}")
print(f"Average Popularity (): {popularity_comparison[False]:.1f}")

#Setting the style
sns.set_theme(style="whitegrid")

#Plot creation
plt.figure(figsize=(8, 6))
sns.barplot(x=popularity_comparison.index, y=popularity_comparison.values, palette=['#A1C9F4', '#FFB482'])

#Labels and titles
plt.title('Average Popularity of Explicit vs Clean Tracks', fontsize=14)
plt.xlabel('Is Explicit?', fontsize=12)
plt.ylabel('Average Popularity Score', fontsize=12)
plt.xticks([0, 1], ['Clean', 'Explicit'])

plt.show()

