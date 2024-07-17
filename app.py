import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Define the path to the data directory using Path
data_dir = Path(__file__).parent / 'data'

# Load data
file_2022 = data_dir / '収入・支出詳細_2022.csv'
file_2023 = data_dir / '収入・支出詳細_2023.csv'
file_2024 = data_dir / '収入・支出詳細_2024.csv'

df_2022 = pd.read_csv(file_2022)
df_2023 = pd.read_csv(file_2023)
df_2024 = pd.read_csv(file_2024)

# Combine dataframes into a single one with a year column
df_2022['Year'] = 2022
df_2023['Year'] = 2023
df_2024['Year'] = 2024

data = pd.concat([df_2022, df_2023, df_2024])

# Convert the date column to datetime format
data['日付'] = pd.to_datetime(data['日付'], format='%Y/%m/%d')

# Convert non-numeric columns to strings to avoid potential type issues
data['内容'] = data['内容'].astype(str)
data['保有金融機関'] = data['保有金融機関'].astype(str)
data['大項目'] = data['大項目'].astype(str)
data['中項目'] = data['中項目'].astype(str)
data['メモ'] = data['メモ'].astype(str)
data['ID'] = data['ID'].astype(str)

# Set page title
st.title("Finance Data Visualization")

# Select year
year = st.selectbox("Select Year", options=[2022, 2023, 2024])

# Filter data based on the selected year
filtered_data = data[data['Year'] == year]

# Display data table
st.write(f"Data for the year {year}")
st.dataframe(filtered_data)

# Plot total income and expenses
income_expense = filtered_data.groupby('大項目')['金額（円）'].sum()
st.write("Total Income and Expenses")
fig, ax = plt.subplots()
income_expense.plot(kind='bar', ax=ax)
ax.set_ylabel('Amount (円)')
st.pyplot(fig)

# Plot monthly income and expenses
filtered_data['Month'] = filtered_data['日付'].dt.month
monthly_data = filtered_data.groupby(['Month', '大項目'])['金額（円）'].sum().unstack().fillna(0)
st.write("Monthly Income and Expenses")
fig, ax = plt.subplots()
monthly_data.plot(kind='line', ax=ax)
ax.set_ylabel('Amount (円)')
st.pyplot(fig)
