# BizCardX-Extracting-Business-Card-Data-with-OCR

Deployment
To deploy this project run

  pip install easyocr
  
  reader = easyocr.Reader(['en'])
This all, but with Regular Expressions...you will be able to segregate each info's in respective way.

  import regex as re
Once you have the reader object, you can use it to extract the information from the Biz_Card. WHhen the Biz_Card is extracted, you will get the following information:



Creating a user_interface website using Streamlit
This helps user to upload their extracted buissness card information and upload it to SQLite database and it will provide a searchable user interface.



Support
email : suriyakalladai82@gmail.com
