#Before running make sure to: 
#1. paste the sql file into freesql and run it
#2. run dataload.py
#3. then you can run you app following the instructions above and below

# to run type in terminal 'streamlit run app.py'
'''
If you are running this code first time, and you don't have streamlit installed, then follow this instruction:
1. open a terminal
2. enter this command
    pip install streamlit
'''

import streamlit as st
import oracledb
import datetime

#If on github codespace input 
#sudo apt-get update
#sudo apt-get install libaio1
#and put /usr/lib/oracle/container/client64/lib into the directory in order to run
# --- CONFIGURATION (Connecting to freesql) ---
LIB_DIR = r"C:\Users\Matthew\Documents\2026 sophmore\Database1\Oraclestuff\instantclient-basiclite-windows.x64-23.26.1.0.0\instantclient_23_0"
DB_USER = "MILEYFAMM_SCHEMA_D0P3M" 
DB_PASS = "OU34VyCQKY11025#I9AFF7X22VI0R4" 
DB_DSN  = "db.freesql.com" + ":" + "1521" + "/" + "23ai_34ui2" 

@st.cache_resource
def init_db():
    if LIB_DIR:
        try:
            oracledb.init_oracle_client(lib_dir=LIB_DIR)
        except Exception as e:
            st.error(f"Error initializing Oracle Client: {e}")

init_db()

def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)

# --- STREAMLIT UI ---
st.title("IMDb Film Industry Analytics Explorer")
    #Title self explanitory, keeps a big text in the middle of the page
st.sidebar.header("Navigation")
    #sidebar.header makes a sidebar on the left side with a name "Navigation"
menu = [
    "1. Movie Title via Duration", 
    "2. Movie Title via Director", 
    "3. Movie Title via Average Vote", 
    "4. Release Date via Movie Title", 
    "5. Release Countries via Movie Title"
]
#Menu is a array which will be but into the selectbox command below
choice = st.sidebar.selectbox("Choose a Query:", menu)
#choice is equal to what we select from the dropdown created by selectbox


# --- Finding Movies Through Their Duration Length ---
if choice == "1. Movie Title via Duration":
    st.subheader("Find Movies Based on Duration")
    #duration_input gets data from a text input that you type in, this case it is the movie name
    duration_input = st.text_input("Enter Movie Duration: ")
    
    #The button is hit
    if st.button("Search"):
        try:
            #connection to fresql is established
            #conn holds the oracledb.Connection value that we get from inputting the right username and password
            conn = get_connection()
            cur = conn.cursor()
            #cur lets you execute SQL commands (select, insert, etc)
            sql = """SELECT DISTINCT title_name 
                FROM movie
                WHERE duration = TO_NUMBER(:dur)
            """
        
            cur.execute(sql, [duration_input])
            data = cur.fetchall()
            
            if data:
                titles = [row[0] for row in data]
                st.write(f"Found {len(titles)} Movies With This Duration Length:")
                st.table(titles)
            else:
                st.info("No Movies Found With This Duration.")
            cur.close()
            #ends the sql execution
            conn.close()
            #closes the sql connection
        except Exception as e:
            #display for the error
            st.error(f"Error: {e}")

# --- Finding Movies Through Their Director ---
elif choice == "2. Movie Title via Director":
    st.subheader("Find Movies Based on Their Director")

    director_input = st.text_input("Enter a Movie Director's Name: ")

    if st.button("Search"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            sql = """SELECT DISTINCT m.title_name
                    FROM movie m
                    JOIN movie_director md ON m.imdb_title_id = md.imdb_title_id
                    JOIN director d ON md.director_id = d.director_id
                    WHERE d.director_name = :dir_name
                 """
            
            cur.execute(sql, [director_input])
            data = cur.fetchall()
            
            if data:
                titles = [row[0] for row in data]
                st.write(f"Found {len(titles)} Movies With This Movie Director:")
                st.table(titles)
            else:
                st.info(f"No Movies Found With This Director.")
                
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

# --- Finding Movies Through Their Average Vote ---
elif choice == "3. Movie Title via Average Vote":
    st.subheader("Find Movies Based on Their Average Vote")
    vote_input = st.text_input("Enter Average Vote of Movie: ")
    
    if st.button("Search"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            sql = """SELECT DISTINCT m.title_name, v.weighted_average_vote 
                     FROM movie m
                     JOIN vote_rating v ON m.imdb_title_id = v.imdb_title_id
                     WHERE v.weighted_average_vote = TO_NUMBER(:wav)
                """
            cur.execute(sql, [vote_input])
            data = cur.fetchall()

            if data:
                titles = [row[0] for row in data]
                st.write(f"Found {len(titles)} Movies With This Vote Rating:")
                st.table(titles)
            else:
                st.info("No Movies Found With This Vote Rating.")
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

# --- Finding Release Date Through Movie Title ---
elif choice == "4. Release Date via Movie Title":
    st.subheader("Find the Release Date of a Movie")
    movie_input = st.text_input("Enter a Movie Title: ")
    
    if st.button("Search"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = """SELECT DISTINCT r.date_published 
                FROM release_date r
                JOIN movie m ON r.imdb_title_id = m.imdb_title_id 
                WHERE m.title_name = :movie_name
            """
            cur.execute(sql, [movie_input])
            data = cur.fetchall()

            if data:
                st.success(f"Release Date Found For **{movie_input}**:")
                for row in data:
                    # row[0] corresponds to r.date_published
                    st.write(f"- {row[0]}")
            else:
                st.info("The Release Date of this Movie is Not Available.")
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

# --- Finding the Release Countries of a Movie Through its Title ---
elif choice == "5. Release Countries via Movie Title":
    st.subheader("Find the Release Countries of a Movie")
    movie_input = st.text_input("Enter a Movie Title: ")
    
    if st.button("Search"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = """SELECT DISTINCT r.country 
                FROM release_country r
                JOIN movie m ON r.imdb_title_id = m.imdb_title_id 
                WHERE m.title_name = :movie_name
            """
            cur.execute(sql, [movie_input])
            data = cur.fetchall()

            if data:
                st.success(f"Release Countries Found For **{movie_input}**:")
                countries = ", ".join([row[0] for row in data])
                st.write(countries)
            else:
                st.info("The Release Countries of this Movie are Not Available.")
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")