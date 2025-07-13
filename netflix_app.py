import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("netflix_titles.csv")
df['listed_in'] = df['listed_in'].str.lower()
df['country'] = df['country'].fillna("Unknown")
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year

st.title(" Netflix Content Explorer")

# Sidebar filters
st.sidebar.header("Filters")

genre = st.sidebar.text_input("Search by Genre (e.g., comedy, drama):").lower()
country = st.sidebar.selectbox("Select Country", sorted(df['country'].dropna().unique()))
# Title Search Input
title_search = st.sidebar.text_input("Search by Title:")

# Filter data
filtered_df = df[df['listed_in'].str.contains(genre, na=False)] if genre else df
filtered_df = filtered_df[filtered_df['country'].str.contains(country, na=False)]

# Show stats
st.subheader(f"Total Results: {len(filtered_df)}")
st.dataframe(filtered_df[['title', 'type', 'listed_in', 'country', 'release_year']])

# Bar plot: Type distribution
st.subheader(" Movie vs TV Show Distribution")
type_counts = filtered_df['type'].value_counts()
fig, ax = plt.subplots()
type_counts.plot(kind='bar', ax=ax, color=['red', 'blue'])
plt.xlabel("Type")
plt.ylabel("Count")
st.pyplot(fig)
filtered_df = df.copy()

# Apply genre filter
if genre:
    filtered_df = filtered_df[filtered_df['listed_in'].str.contains(genre, na=False)]

# Apply country filter
if country:
    filtered_df = filtered_df[filtered_df['country'].str.contains(country, na=False)]

# Apply title search filter
if title_search:
    filtered_df = filtered_df[filtered_df['title'].str.lower().str.contains(title_search.lower())]

# Optional: Year-wise trend
if 'year_added' in filtered_df.columns:
    st.subheader("Content Added Over Years")
    year_trend = filtered_df['year_added'].value_counts().sort_index()
    fig2, ax2 = plt.subplots()
    year_trend.plot(kind='line', ax=ax2)
    plt.xlabel("Year")
    plt.ylabel("No. of Titles")
    st.pyplot(fig2)
