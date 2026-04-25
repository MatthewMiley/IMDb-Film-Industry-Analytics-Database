
<img width="2205" height="1661" alt="Screenshot 2026-03-01 170222" src="https://github.com/user-attachments/assets/74aadfe6-b47b-4357-983d-e923c83a6a66" />

To Run this program follow these steps:

First Time Run:
1. paste the sql file into freesql and run it (comment out everything but the first block if there is tables already there then run all the previously uncommented things without the first block)
2. Get instantclient and extract it somewhere safe and copy it's file path into LIB_DIR (see step 4)
3. paste 'python preprocess.py' in terminal first if you have the kaggle dataset (Without the '')
4. Fill out the configuration in dataload.py and app.py with somthing along the lines of:
LIB_DIR = r"C:\Users\Matthew\Documents\2026 sophmore\Database1\Oraclestuff\instantclient-basiclite-windows.x64-23.26.1.0.0\instantclient_23_0"
DB_USER = "MILEYFAMM_SCHEMA_D0P3M" 
DB_PASS = "OU34VyCQKY11025#I9AFF7X22VI0R4" 
DB_DSN  = "db.freesql.com" + ":" + "1521" + "/" + "23ai_34ui2" 
5. then put 'python dataload.py' in the terminal and enter
6. Once dataload is done you can run 'python app.py'