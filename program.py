import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="Data sweeper", layout="wide")

#custom css
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
         }
         </style>
    """,
    unsafe_allow_html=True
 )

 #title and description
st.title("Datasweeper Sterling Integrator by Hikmat Khan")
st.write("This application is designed to help you clean up your data. You can upload a CSV file and select the columns you want to keep. The app will then return a new CSV file with only the columns you selected.")


#upload file
uploaded_file = st.file_uploader("upload your file (accept CSV or Excel files)", type=["csv", "xlsx"],accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file.ext = os.pt.splitext(file.name)[-1].lower()

        if file.ext == ".csv":
            df = pd.read_csv(file)
        elif file.ext == ".xlsx":
            df = pd.read_excel(file)
        else:
                st.error(f"This file format is not supported: {file.ext}")
                continue
            #file preview
        st.write("Preview the head of the Dataframe:")
        st.write(df.head())


        #Data cleaning options (selectbox)
        st.subheader("Data cleaning options")

        if st.checkbox("Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed")

            with col2:
                if st.button(f"Remove missing values: {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values removed") 
                    

        st.subheader("Select columns to keep")
        columns = st.multiselect(f"Select the columns you want to keep", df.columns, default=df.columns)  
        df = df[columns]

        #Data visualization  
        st.subheader("Data visualization")

        if st.checkbox("Show visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

            #conversion options
            st.subheader("Conversion options")
            conversion_type = st.radio(f"convert {file.name} to", ["CSV", "Excel"], key=file.name)
            if st.button(f"Convert {file.name}"):
                
                buffer = BytesIO()
                if conversion_type == "CSV":
                    file_name = file.name.replace(file.ext, ".")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file.ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                st.download_button(
                    label=f"Click here to download {conversion_type} file",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                )

st.success("Thank you for using this app. If you have any feedback, please let me know!")
                        
                

                    
              
            
