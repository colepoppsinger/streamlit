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
st.subheader("Top 5 most common movies based on user ratings and their corresponding Bechdel Score")

#favorite movie query - text - any format
query = st.text_input("What's your favorite movie?")
# button that sends query
show_options = st.button('Show me my options')

# button= search for movies with keywords inputted, makes df of options
if try_it:

    # movie_list = []
    # for title in movies.loc[movies['title'].str.contains(query, case=False), 'title']:
    #     movie_list.append(title)
    #     movie_df = pd.DataFrame(movie_list, columns = ['movies'])
    #st.write(movie_df)    

    
    # option = st.selectbox('Which one of these did you mean?', options=movie_df['movies'])
    # st.write(f'you have selected {option}') 

# show_me = st.button('show me movies!')
# if show_me:
    movie_list = []
    def get_list(movie_word):
        for title in movies.loc[movies['title'].str.contains(query, case=False), 'title']:
            movie_list.append(title)
            movie_df = pd.DataFrame(movie_list, columns = ['movies']) #this allows dropdown in streamlit
        return movie_df
    
option = st.selectbox('Which one of these did you mean?', options=movie_df['movies'])
st.write(f'you have selected {option}') 

        
        results = recommend[title].sort_values(ascending=False)[1:6]
        results_df = pd.DataFrame(results)
        results_df['bechdel score'] = results_df.index.map(bechdel)
        try:
            st.write(results_df)
        except:
            pass


# st.write('Great choice! You selected:', choice)
#     #st.write(choice)
    
#   mulitline form with single button
# with st.form("my_form"):
#     st.write("Inside the form")
#     slider_val = st.slider("Form slider")
#     checkbox_val = st.checkbox("Form checkbox")

#     # Every form must have a submit button.
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         st.write("slider", slider_val, "checkbox", checkbox_val)

# st.write("Outside the form")