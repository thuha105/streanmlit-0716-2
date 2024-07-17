import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Define the path to the data directory using Path
data_dir = Path(__file__).parent / 'data'

# Translation dictionaries
column_translation_dict = {
    '日付': 'Date',
    '内容': 'Description',
    '保有金融機関': 'Financial Institution',
    '大項目': 'Category',
    '中項目': 'Subcategory',
    'メモ': 'Memo',
    'ID': 'ID',
    '金額（円）': 'Amount (Yen)'
}

category_translation_dict = {
    '給料': 'Salary',
    '食費': 'Food',
    '住居費': 'Housing',
    '光熱費': 'Utilities',
    '交通費': 'Transportation',
    '娯楽': 'Entertainment',
    '医療費': 'Medical',
    '教育費': 'Education',
    '通信費': 'Communication',
    'その他': 'Others'
}

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

# Function to translate column names and category values
def translate_dataframe(df, column_dict, category_dict):
    df = df.rename(columns=column_dict)
    if 'Category' in df.columns:
        df['Category'] = df['Category'].map(category_dict).fillna(df['Category'])
    return df

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

    df_2022 = translate_dataframe(df_2022, column_translation_dict, category_translation_dict)
    df_2023 = translate_dataframe(df_2023, column_translation_dict, category_translation_dict)
    df_2024 = translate_dataframe(df_2024, column_translation_dict, category_translation_dict)

    data = pd.concat([df_2022, df_2023, df_2024])

    # Convert the date column to datetime format
    data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d')

    # Convert non-numeric columns to strings to avoid potential type issues
    for column in ['Description', 'Financial Institution', 'Category', 'Subcategory', 'Memo', 'ID']:
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
    income_expense = filtered_data.groupby('Category')['Amount (Yen)'].sum()
    st.write("Total Income and Expenses")
    fig, ax = plt.subplots()
    income_expense.plot(kind='bar', ax=ax)
    ax.set_ylabel('Amount (Yen)')
    ax.set_xlabel('Category')
    for label in ax.get_xticklabels():
        label.set_rotation(45)
    st.pyplot(fig)
except Exception as e:
    st.error(f"Error plotting total income and expenses: {e}")

# Plot monthly income and expenses
try:
    filtered_data['Month'] = filtered_data['Date'].dt.month
    monthly_data = filtered_data.groupby(['Month', 'Category'])['Amount (Yen)'].sum().unstack().fillna(0)
    st.write("Monthly Income and Expenses")
    fig, ax = plt.subplots()
    monthly_data.plot(kind='line', ax=ax)
    ax.set_ylabel('Amount (Yen)')
    ax.set_xlabel('Month')
    for label in ax.get_xticklabels():
        label.set_rotation(45)
    st.pyplot(fig)
except Exception as e:
    st.error(f"Error plotting monthly income and expenses: {e}")
