import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Define the path to the data directory using Path
data_dir = Path(__file__).parent / 'data'

# Function to load CSV file with error handling
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if the file is not found
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on any other error

# Load data
file_2022 = data_dir / '2022.csv'
file_2023 = data_dir / '2023.csv'
file_2024 = data_dir / '2024.csv'

df_2022 = load_data(file_2022)
df_2023 = load_data(file_2023)
df_2024 = load_data(file_2024)

# Check if any dataframes are empty and exit if they are
if df_2022.empty or df_2023.empty or df_2024.empty:
    st.stop()

# Combine dataframes into a single one with a year column
try:
    df_2022['Year'] = 2022
    df_2023['Year'] = 2023
    df_2024['Year'] = 2024

    data = pd.concat([df_2022, df_2023, df_2024])

    # Convert the date column to datetime format
    data['日付'] = pd.to_datetime(data['日付'], format='%Y/%m/%d')

    # Convert non-numeric columns to strings to avoid potential type issues
    for column in ['内容', '保有金融機関', '大項目', '中項目', 'メモ', 'ID']:
        data[column] = data[column].astype(str)
except Exception as e:
    st.error(f"Error processing data: {e}")
    st.stop()

# Set page title
st.title("Finance Data Visualization")

# Select year
year = st.selectbox("Select Year", options=[2022, 2023, 2024])

# Filter data based on the selected year
filtered_data = data[data['Year'] == year]

# Display data table
try:
    st.write(f"Data for the year {year}")
    st.dataframe(filtered_data)
except Exception as e:
    st.error(f"Error displaying data: {e}")
    st.stop()

# Plot total income and expenses
try:
    income_expense = filtered_data.groupby('大項目')['金額（円）'].sum()
    st.write("Total Income and Expenses")
    fig, ax = plt.subplots()
    income_expense.plot(kind='bar', ax=ax)
    ax.set_ylabel('Amount (円)')
    st.pyplot(fig)
except Exception as e:
    st.error(f"Error plotting total income and expenses: {e}")

# Plot monthly income and expenses
try:
    filtered_data['Month'] = filtered_data['日付'].dt.month
    monthly_data = filtered_d
