import pandas as pd 
from Movies.models import Movies, Genre_Utility

df = pd.read_csv("E:/Internship/data/melted_genres.csv")
values = []
for i in df.index:
    m_id = df.at[i,"id"]
    genre = df.at[i,"genre"]
    values.append(Genre_Utility(movie_id=Movies(id=m_id), genre= genre)) 
    if len(values) >= 1000:
        Genre_Utility.objects.bulk_create(values)
        print("Created {i}")
        values = []
    print("Done {i}", end="\r")
    
if values:
    Genre_Utility.objects.bulk_create(values)
    print("Done {values}")
    


