# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'SpotifyProject'))
	print(os.getcwd())
except:
	pass

#%%
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KDTree


#%%
df = pd.read_csv('SpotifyAudioFeaturesApril2019 copy.csv')


#%%
df.head()


#%%
# Now to Make a Function to sum all this up and try different clustering models

def find_nearest_songs(df):
    # remove categoricals
    df_numerics =  df.drop(columns=['track_id', 'track_name', 'artist_name'])
    
    # Scale Data To Cluster More Accurately, and fit clustering model
    df_scaled = StandardScaler().fit_transform(df_numerics)
    df_modeled = KDTree(df_scaled)
    
    # Querying the model for the 15 Nearest Neighbors
    dist, ind = df_modeled.query(df_scaled, k=16)
    
    # Putting the Results into a Dataframe
    dist_df = pd.DataFrame(dist)
    
    # Calculating the Distances
    scores = (1 - ((dist - dist.min()) / (dist.max() - dist.min()))) * 100
    
    # Creating A New Dataframe for the Distances
    columns = ['Searched_Song', 'Nearest_Song1', 'Nearest_Song2', 'Nearest_Song3', 'Nearest_Song4',
               'Nearest_Song5', 'Nearest_Song6', 'Nearest_Song7', 'Nearest_Song8', 'Nearest_Song9',
               'Nearest_Song10', 'Nearest_Song11', 'Nearest_Song12', 'Nearest_Song13', 'Nearest_Song14',
               'Nearest_Song15']
    dist_score = pd.DataFrame(scores.tolist(), columns = columns)
    
    # An Array of all indices of the nearest neighbors
    ind[:16]
    
    # Making an array of the Track IDs
    song_ids = np.array(df.track_id)
    
    # A function that creates list of the each song with its nearest neighbors
    def find_similars(song_ids, ind):
        similars = []
        for row in ind:
            ids = [song_ids[i] for i in row]
            similars.append(ids)

        return similars 
    
    # using the above function
    nearest_neighbors = find_similars(song_ids, ind)
    
    # putting the results into a dataframe
    nearest_neighbors_df = pd.DataFrame(nearest_neighbors, columns=columns)
    
    return nearest_neighbors_df


#%%
# this takes a good two to three minutes to process
find_nearest_songs(df)


#%%
# From here, if we add both the new dataframe and the original into an SQL database, we can easily
# just run JOIN ON queries to match the song Id's with track_name, artist, and any other info we'd want to display


