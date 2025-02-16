import sys 
import os 
import numpy as np 
import pandas as pd 
import warnings
import nltk
import secrets
from dataclasses import dataclass, field
from Base_Case_Checker import BaseCase
import time

@dataclass
class Recommender:
    uid: int

    def __post_init__(self):
        pass

    def Connecting(self):
        print("\033[1;32m Connecting to the servers\033[00m")
        base_case: BaseCase = BaseCase(r'E:Internship/')
        status = base_case.base_case()
        return status

    def Main_WorkFlow(self):
        pass 
    
    def Main_Static(self):
        pass 

    def top_n_trending(self, n: int):
        pass 

    def you_might_like(self):
        pass 

    def your_favorite_genre(self):
        pass 

    def if_you_liked_this_movie_might_like_this_one(self):
        pass

    def recommended_movies_in_language(self):
        pass 

    def movies_you_might_like(self):
        pass 

    def try_these_out(self):
        pass 

@dataclass
class factory:

    def collaborative_recommendation(svd, uid,sampling_num=1000, seed=None, n=10):
        sample_data = df2[['id','new title']].sample(n=sampling_num, random_state=seed)
        listin = []
        for id in sample_data['id']:
            sii = svd.predict(uid=uid,iid=id).est
            listin.append(sii)

        sek = pd.Series(listin, index= sample_data['id'],name='predicted_rating')
        sek = sek.reset_index().sort_values('predicted_rating',ascending=False).head(n)
        return sek

    def get_overview_recommendations_lite(df, mid, seed: 'int|None' = None, sample_size: 'int' = 1000, n: int = 10):
        overview1 = df.loc[df['id'] == mid]['overview_cleaned']
        doc1 = nlp(overview1)
        # w1 = set(ss for word in overview1 for ss in wordnet.synsets(word))
        samples = df.sample(sample_size, random_state=seed)
        listin = []
        for i in samples.id:
            overview12 = df.loc[df['id'] == i]['overview_cleaned']
            doc2 = nlp(overview12)
            # w2 = set(ss for word in overview12 for ss in wordnet.synsets(word))
            sim = doc1.similarity(doc2)
            # sim = (wordnet.wup_similarity(s1,s2) for s1,s2, in product(w1,w2))
            listin.append(sim)

        series = pd.Series(listin, index= samples.id, name="similarity")
        series = series.reset_index().sort_values("similarity",ascending=False).head(n)
        return series
    
    def get_overview_recommendations(mid, cosine_sim = cosine_sim):
        sim_scores = list(enumerate(cosine_sim[mid]))
        sim_scores = sorted(sim_scores, key= lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        movie_indices = [i[0] for i in sim_scores]
        scores = [i[1] for i in sim_scores]
        # titles = [i for i in movies['id'].iloc[movie_indices]]
        return pd.DataFrame({'id':movie_indices, 'score':scores})

if __name__ == '__main__':
    pass
