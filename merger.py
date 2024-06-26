import streamlit as st
import pandas as pd
from typing import List
from io import BytesIO
from tempfile import NamedTemporaryFile

# Function to append files
def append_files(files: List[BytesIO]):
    dfs = []
    file_dimensions = []
    file_names = []
    
    for file in files:
        try:
            if file.name.endswith('.xls') or file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)
            
            # Store dimensions and filename of each file
            file_dimensions.append(df.shape)
            file_names.append(file.name)
            dfs.append(df)
        
        except Exception as e:
            st.error(f"Error reading file {file.name}: {e}")
            return None, [], []
    
    if len(dfs) == 0:
        st.warning("No valid files found to append.")
        return None, [], []
    
    try:
        appended_df = pd.concat(dfs, ignore_index=True)
        appended_dimensions = appended_df.shape
    except Exception as e:
        st.error(f"Error appending files: {e}")
        return None, [], []
    
    return appended_df, file_names, file_dimensions, appended_dimensions

# Streamlit UI
def main():
    st.title(':blue[Append Excel/CSV Files]')
    st.write("")
    uploaded_files = st.file_uploader("Upload your files", accept_multiple_files=True)

    if st.button("Append Files") and uploaded_files:
        st.write("")
        files_data = [file for file in uploaded_files]
        appended_data, file_names, file_dimensions, appended_dimensions = append_files(files_data)
        
        if appended_data is not None:
            st.subheader(":blue[Dimensions of Uploaded Files:]")
            for i, (filename, dim) in enumerate(zip(file_names, file_dimensions), start=1):
                st.write(f"{filename}: {dim[0]} rows, {dim[1]} columns")
            
            st.subheader("\n:blue[Dimensions of Appended Data:]")
            st.write(f"Appended Data: {appended_dimensions[0]} rows, {appended_dimensions[1]} columns")
            st.write("")
            
            st.subheader("\n:blue[Appended Data:]")
            st.write(appended_data)
            
            # Allow user to download the appended file as CSV

            col1, col2 = st.columns([0.5, 1.2])

            with col1:

                with NamedTemporaryFile(delete=False, suffix='.csv') as temp_csv:
                    appended_data.to_csv(temp_csv.name, index=False)
                    st.download_button(label="Download Appended CSV", data=temp_csv.name, file_name='appended_data.csv', mime='text/csv')
            
            with col2:
            # Allow user to download the appended file as Excel (xlsx)
                with NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_xlsx:
                    appended_data.to_excel(temp_xlsx.name, index=False)
                    st.download_button(label="Download Appended Excel", data=temp_xlsx.name, file_name='appended_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        
        else:
            st.warning("Unable to append files. Please check your files and try again.")

if __name__ == '__main__':
    main()
