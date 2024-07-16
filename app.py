import streamlit as st

# Title of the app
st.title("Simple Streamlit App")

# Slider widget
value = st.slider("Select a number", 0, 100, 50)

# Display the selected value
st.write("Selected number:", value)

