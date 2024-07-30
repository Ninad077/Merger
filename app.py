import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# Define the button and title styles
styles = """
<style>
/* Button styles */
div.stButton > button {
    color: #ffffff; /* Text color */
    font-size: 20px;
    background-image: linear-gradient(0deg, #a2c2e1 0%, #003b5c 100%); /* Light blue to deep blue gradient */
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 15px;
    display: inline-block;
    width: 100%; /* Make button fit column width */
}
div.stButton > button:hover {
    background-color: #00ff00; /* Hover background color */
    color: #ff0000; /* Hover text color */
}

/* Title styles */
h1 {
    background-image: linear-gradient(0deg, #a2c2e1 0%, #003b5c 100%); /* Light blue to deep blue gradient */
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 36px;
}
</style>
"""

# Set up the Streamlit app
st.markdown(styles, unsafe_allow_html=True)

# Set up the Streamlit app
st.markdown(styles, unsafe_allow_html=True)

# Custom gradient title
st.markdown("<h1>CSV appender</h1>", unsafe_allow_html=True)
st.write("A website that is used for appending multiple csv files and converting them to excel format")

# File uploader for multiple CSV files
uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)

# Render the button styles
st.markdown(styles, unsafe_allow_html=True)

if uploaded_files:
    # Initialize an empty list to store DataFrames
    df_list = []

    for i, uploaded_file in enumerate(uploaded_files):
        # Read the CSV file into a DataFrame
        if i == 0:
            # For the first file, include the header
            df = pd.read_csv(uploaded_file)
            # Store the columns from the first file
            headers = df.columns
        else:
            # For subsequent files, set the header using the stored headers
            df = pd.read_csv(uploaded_file, names=headers, header=0)
        df_list.append(df)

    # Concatenate all DataFrames, ignoring index to avoid duplication
    merged_df = pd.concat(df_list, ignore_index=True)

    # Display the merged DataFrame
    st.markdown("<h1>Appended data</h1>", unsafe_allow_html=True)
    st.dataframe(merged_df)

    # Create a layout with 3 columns for buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        # Provide a download button for the merged CSV file
        if st.button("Append CSV"):
          csv_output = BytesIO()
          merged_df.to_csv(csv_output, index=False)
          csv_output.seek(0)
          csv_base64 = base64.b64encode(csv_output.getvalue()).decode()
        

    with col2:
        # Provide an option to convert to Excel
        if st.button("Convert to Excel"):
            excel_output = BytesIO()
            with pd.ExcelWriter(excel_output, engine='xlsxwriter') as writer:
                merged_df.to_excel(writer, index=False)
            excel_output.seek(0)

            # Store the Excel output in session state for later download
            excel_base64 = base64.b64encode(excel_output.getvalue()).decode()
            st.session_state.excel_data = excel_base64
            st.session_state.excel_ready = True

    with col3:
        # Provide a download button for the Excel file if it has been converted
        if st.button("Download excel"):
          if st.session_state.get("excel_ready", False):
              st.markdown(f"""
              <a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{st.session_state.excel_data}" download="merged_data.xlsx" class="stButton">
                  <button>Download excel</button>
              </a>
              """, unsafe_allow_html=True)

else:
    st.write("")
