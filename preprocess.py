import csv
import os 

#if a data folder doesn't exist make one, this data folder will hold the cleaned csv data
if not os.path.exists('data'):
    os.makedirs('data')

# Storage for our cleaned data
unique_directors = {}  
director_counter = 1 
movie_director_links = [] 
movies_clean = []
release_countries = []
release_dates = []

# --- NEW: Track the IDs we actually keep ---
kept_movie_ids = set() 

#now that we have some structures to hold data we can begin processing the movies and directors
with open('IMDb movies.csv', mode='r', encoding='utf-8') as f:
    #opens the movies csv in reading mode and keeps it open while the code under the statement runs
    #refers to the movies csv as 'f'
    reader = csv.DictReader(f)
    #csv.DictReader reads the first row of the file (the column headers) and uses those names as
    #keys for every other row in the file so now you can say row['imdb_title_id'] instead of row[0]

    count = 0
    for row in reader:
        if 'English' not in row['language']:
            continue
            
        if count >= 5000:
            break
            
        m_id = row['imdb_title_id']
        kept_movie_ids.add(m_id) # Remember this ID

        #Remove '$' and ',' from budget and income so Oracle sees them as numbers
        raw_budget = row['budget'] or "0"
        clean_budget = "".join(c for c in raw_budget if c.isdigit()) or "0"

        raw_income = row['worlwide_gross_income'] or "0"
        clean_income = "".join(c for c in raw_income if c.isdigit()) or "0"

        #Ensure date is in a standard YYYY-MM-DD format if possible by stripping whitespace
        clean_date = row['date_published'].strip()
        
        # Validation to fix ORA-01840: ensures date strings are long enough for Oracle
        if len(clean_date) == 4:
            clean_date += "-01-01"
        elif len(clean_date) == 7:
            clean_date += "-01"
        elif len(clean_date) < 10:
            clean_date = "1900-01-01"

        #save movie details into the new movies cvs file
        movies_clean.append([m_id, row['title'], row['duration'], clean_budget, clean_income]) #raw has d missing from world for some reason
        
        # Save country info
        release_countries.append([m_id, row['country']])
        # Save date info
        release_dates.append([m_id, clean_date])

        #split directors in each director cell
        raw_directors = row['director'].split(',')
        
        # Track links for this specific movie to avoid ORA-00001 unique constraint errors
        seen_directors_for_this_movie = set()
        
        for d_name in raw_directors:
            name = d_name.strip()
            if not name: continue
            
            if name not in unique_directors:
                unique_directors[name] = director_counter
                director_counter += 1
            
            d_id = unique_directors[name]
            
            #link the current movie to the director's id
            if d_id not in seen_directors_for_this_movie:
                movie_director_links.append([m_id, d_id])
                seen_directors_for_this_movie.add(d_id)
        
        count += 1

# --- UPDATED: Only process ratings for the 5,000 movies we kept ---
vote_ratings = []
with open('IMDb ratings.csv', mode='r', encoding='utf-8') as f:
    r_reader = csv.DictReader(f)
    for r_row in r_reader:
        if r_row['imdb_title_id'] in kept_movie_ids:
            vote_ratings.append([
                r_row['imdb_title_id'], r_row['weighted_average_vote'], 
                r_row['total_votes'], r_row['mean_vote'], r_row['median_vote']
            ])

#Save to new csvs in the created data folder
with open('data/directors.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['director_id','director_name'])
    for name, d_id in unique_directors.items():
        writer.writerow([d_id, name])

with open('data/movie_directors.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['imdb_title_id', 'director_id'])
    writer.writerows(movie_director_links)

with open('data/vote_rating.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['imdb_title_id', 'weighted_average_vote', 'total_votes', 'mean_vote', 'median_vote'])
    writer.writerows(vote_ratings)

with open('data/release_country.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['imdb_title_id', 'country']) 
    writer.writerows(release_countries)

with open('data/release_date.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['imdb_title_id', 'date_published'])
    writer.writerows(release_dates)

with open('data/movies.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['imdb_title_id', 'title_name', 'duration', 'budget', 'worldwide_gross_income'])
    writer.writerows(movies_clean)

#just for my sake print statement declaring that the preprocessor worked
print("Pre-processing done, check /data folder for issues")