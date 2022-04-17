#IMPORTS
from secrets import choice
import pandas as pd
import numpy as np
from scipy import sparse
import sys
from sklearn.metrics.pairwise import pairwise_distances, cosine_distances, cosine_similarity
import streamlit as st

#DATAFRAMES
all = pd.read_csv('all.csv')
movies = pd.read_csv('movies.csv')

#RECOMMMENDER
pivot = all.pivot_table(index='title', columns='userId', values='rating')
pivot_sparse = sparse.csr_matrix(pivot.fillna(0))
distances = pairwise_distances(pivot_sparse, metric='cosine')
similarity = 1.0 - distances
recommend = pd.DataFrame(similarity, index=pivot.index, columns=pivot.index)

#BECHDEL FUNC
def bechdel(title):
    return (all.loc[all['title'] == title]['bechdel_score']).mode()[0]

#STREAMLIT CODE

#title
st.title("Movie Recommender + Bechdel Score")
#header
st.subheader("Top 5 most similar movies based on user ratings and their corresponding Bechdel Score")

#favorite movie query - text - any format
query = st.text_input("What's your favorite movie?")
# button that sends query
try_it = st.button('Show me movies and Bechdel Scores!')
# button= search for movies with keywords inputted, makes df of options
if try_it:
    # movie_list = []
    # for title in movies.loc[movies['title'].str.contains(query, case=False), 'title']:
    #     movie_list.append(title)
    #     movie_df = pd.DataFrame(movie_list, columns = ['movies'])
    # #st.write(movie_df)    

    
    # option = st.selectbox('Which one of these did you mean?', options=movie_df)
    # st.write('you have selected', option) 
    
    # show_me = st.button('show me movies!')
    # if show_me:
    for title in movies.loc[movies['title'].str.contains(query, case=False), 'title']:
        # movie_list.append(title)
        # movie_df = pd.DataFrame(movie_list, columns = ['movies']) #this allows dropdown in streamlit
        results = recommend[title].sort_values(ascending=False)[1:6]
        results_df = pd.DataFrame(results)
        results_df['bechdel score'] = results_df.index.map(bechdel)
        st.write(results_df)
        print()

# st.write('Great choice! You selected:', choice)
#     #st.write(choice)
    

