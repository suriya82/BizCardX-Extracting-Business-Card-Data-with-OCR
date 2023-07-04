import streamlit as st
import pandas as pd
from PIL import Image
import sqlite3
import time
import json
from streamlit_lottie import st_lottie
import pymysql
from sqlalchemy import create_engine
import mysql.connector as sql

st.set_page_config(layout="wide",page_title="Bizcard_EasyOCR",page_icon=Image.open('media/bizcard.jpg'))

st.sidebar.title("BUSINESS CARD..")
menu = ["Home", "Upload & View","Modify",]
choice = st.sidebar.selectbox("Menu",menu)

def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:

        return json.load(f)
    
mydb = sql.connect(host="localhost",
                   user="root",
                   password="123456",
                   database= "Businesscard"
                  )
    
mycursor=mydb.cursor(buffered=True)

if choice == "Home":
    st.title(":orange[Biz_card Extraction using EasyOCR]")
    col1,col2 = st.columns(2)
    with col1:
        lottie1 = load_lottiefile("media/biz.json")
        st_lottie(lottie1, height=500)
    with col2:
        st.subheader(":green[Business card extraction is the process of digitizing the information on a physical business card and transferring it to a digital format."
                 " This allows the information to be easily stored, organized, and shared electronically.]")
                    
    col1,col2 = st.columns(2)
    with col1:
        st.title(":orange[**EASY_OCR**]")
        st.subheader(":green[Another option is to use a mobile app or software program specifically designed for business card extraction."
                     " These apps use optical character recognition (OCR) technology to scan the business card and extract the relevant information."
                     " Some apps also allow users to add notes, tags, or other details to the digital contact record.]")
    with col2:
        lottie2 = load_lottiefile("media/ocr.json")
        st_lottie(lottie2, height=400)
    col1,col2 = st.columns(2)
    with col1:
        lottie3 = load_lottiefile("media/sql.json")
        st_lottie(lottie3, height=700)
    with col2:
        st.title(":orange[**pymysql**]")
        st.subheader(":green[Once the data has been formatted correctly, it can be inserted into the pymysql database using SQL commands such as INSERT or UPDATE.]")

if choice == "Upload & View":
    # getting csv file from user
    file = st.file_uploader("Upload File", type=["csv", "xlsx", "xls"])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Upload into Database"):
            progress_text = "Operation in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)

            df = pd.read_csv(r'C:\Users\Lenovo\Desktop\Extracted_data.csv')
            cnx = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/Businesscard") 
            df.to_sql('df', cnx, if_exists='replace', index=None)

            
        
            st.success("Data Uploaded Successfully")
    with col2:
        if st.button("View csv file"):
            df = pd.read_csv(r'C:\Users\Lenovo\Desktop\Extracted_data.csv')
            st.dataframe(df)
        






if choice == "Modify":

    
    col1,col2,col3 = st.columns([3,3,2])
    col2.markdown("## Alter or Delete the data here")
    column1,column2 = st.columns(2,gap="large")


    
    with col1:
            mycursor.execute("SELECT Name FROM df")
            result = mycursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a  Name to update", list(business_cards.keys()))
            st.markdown("#### Update or modify any data below")
            mycursor.execute("select Name,Contact,Designation,Domain,Email,Website,Address,District,State,Pincode from df WHERE Name=%s",
                            (selected_card,))
            result = mycursor.fetchone()

            # DISPLAYING ALL THE INFORMATIONS
            Name = st.text_input("Name")
            contact = st.text_input("Contact")
            Designation = st.text_input("Designation")
            Domain = st.text_input("Domain")
            Email = st.text_input("Email")
            Website = st.text_input("Website")
            Address = st.text_input("Address")
            District = st.text_input("District")
            State = st.text_input("State")
            Pincode = st.text_input("PinCode")

            if st.button("Commit changes to DB"):
                # Update the information for the selected business card in the database
                mycursor.execute("""UPDATE df SET Name=%s,Contact=%s,Designation=%s,Domain=%s,Email=%s,Website=%s,Address=%s,District=%s,State=%s,Pincode=%s
                                    WHERE Name=%s""", (Name,contact,Designation,Domain,Email,Website,Address,District,State,Pincode,selected_card))
                mydb.commit()
                st.success("Information updated in database successfully.")

            with column2:
                 mycursor.execute("SELECT Name FROM df")
            result = mycursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a Name to Delete", list(business_cards.keys()))
            st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
            st.write("#### Proceed to delete this card?")

            if st.button("Yes Delete card"):
                mycursor.execute(f"DELETE FROM df WHERE Name='{selected_card}'")
                mydb.commit()
                st.success("card information deleted from database.")


                
    
if st.button("View updated data"):
        mycursor.execute("select Name,contact,Designation,Domain,Email,Website,Address,District,State,Pincode from df")
        updated_df = pd.DataFrame(mycursor.fetchall(),columns=["Name","contact","Designation","Domain","Email","Website","Address","District","State","Pincode"])
        st.write(updated_df)






