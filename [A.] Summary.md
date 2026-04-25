Given task: Develop a database of IMDb films covering movies and their cast, crew, ratings, revenue, and awards. 

Project Scope:

    The goal:
        Keeping track of directors and how they have performed through IMDb.

    The features:
        My project will be designed to look at a dataset of IMDb films and keep track of the directors of said films and what they've done over their careers examining the films they released, when they were active(career trajectory analysis), what were the best directors based on their best film decided by gross world income with user ratings (performance indexing), what genre they were primarily directing, and what films directors collaborated on (many to many relationship modeling). 
        Many-to-Many relationship: some films have multiple directors

    The Boundaries:
        The data I have goes from 1894 to 2020, and will be limited by any films not entered into the database, and is only movies. I will also filter out films not in english and with less than 100 user reviews. 

    The Data Plan:
        I have two kaggle datasets, but the "IMDb extensive dataset" one has over 82000 movies which means it'll likely be the data source I will draw heavily from.
        The extensive dataset has two tables linked by the imdb_title_id value one which has data on the ratings and one which details the movies.

    Difficulties:
        The database I'm using is very large and will require filtering out data, in order to work within my chosen search query language application (FreeSQL).
        


Users:
Film Analysts
Film Producers
Movie Reviewers



Data Sources:
https://www.kaggle.com/datasets/simhyunsu/imdbextensivedataset
https://www.kaggle.com/datasets/rajugc/imdb-movies-dataset-based-on-genre/data
