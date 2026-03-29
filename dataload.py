import oracledb
import csv

#before running dataload.py, make sure to paste create_db.sql into your freesql and run it
#to run paste 'python preprocess.py' in terminal first
#then paste 'python dataload.py'

# --- CONFIGURATION ---
# Path to your extracted Instant Client (Required for FreeSQL/Cloud or older oracle DB versions)
LIB_DIR = r"C:\Users\Matthew\Documents\2026 sophmore\Database1\Oraclestuff\instantclient-basiclite-windows.x64-23.26.1.0.0\instantclient_23_0"

# Your Oracle Credentials
DB_USER = "MILEYFAMM_SCHEMA_D0P3M" # or your FreeSQL username
DB_PASS = "HZI!17TZYVN2SLDV4ZSZ87AH3VWl3Y" # your password for the dbms user
DB_DSN  = "db.freesql.com:1521/23ai_34ui2" # or your FreeSQL DSN

#Initialize Thick Mode (Required for encrypted Cloud/FreeSQL connections)
if LIB_DIR:
    oracledb.init_oracle_client(lib_dir=LIB_DIR)
else: 
    oracledb.enable_thin_mode()

#Establish Connection
# uses the credentials inputted above to connect to freesql
conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
cursor = conn.cursor()
print("Connected to Oracle Database")

#Load Function
# function to load a single csv into freesql oracle
def load_csv_to_oracle(file_path, table_name, insert_sql):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Skip header
            all_data = [row for row in reader]
            
            # Define chunk size (5000 rows at a time)
            chunk_size = 5000
            for i in range(0, len(all_data), chunk_size):
                chunk = all_data[i:i + chunk_size]
                cursor.executemany(insert_sql, chunk)
                conn.commit() # Commit after each chunk
                print(f"Uploaded {i + len(chunk)} / {len(all_data)} rows into {table_name}...")
                
            print(f"DONE: Successfully loaded {table_name}\n")
    except Exception as e:
        print(f"Error loading {table_name}: {e}")

#Define the Loading Tasks (ORDER MATTERS!)
#Movies first (Parent)
load_csv_to_oracle('data/movies.csv', 'movie', "INSERT INTO movie (imdb_title_id, title_name, duration, budget, worldwide_gross_income) VALUES (:1, :2, :3, :4, :5)")

#Directors second (Parent)
load_csv_to_oracle('data/directors.csv', 'director', "INSERT INTO director (director_id, director_name) VALUES (:1, :2)")

#The rest (Children)
load_csv_to_oracle('data/vote_rating.csv', 'vote_rating', "INSERT INTO vote_rating (imdb_title_id, weighted_average_vote, total_votes, mean_vote, median_vote) VALUES (:1, :2, :3, :4, :5)")

load_csv_to_oracle('data/release_country.csv', 'release_country', "INSERT INTO release_country (imdb_title_id, country) VALUES (:1, :2)")

load_csv_to_oracle('data/release_date.csv', 'release_date', "INSERT INTO release_date (imdb_title_id, date_published) VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'))")

load_csv_to_oracle('data/movie_directors.csv', 'movie_director', "INSERT INTO movie_director (imdb_title_id, director_id) VALUES (:1, :2)")

#Closing connection
cursor.close()
conn.close()
print("Oracle connection closed.")