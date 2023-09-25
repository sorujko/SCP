import streamlit as st
import pandas as pd
import numpy as np

st. set_page_config(layout="wide")
df = pd.read_csv('SCP-database.csv')

file_path = "tags.txt"

# Initialize an empty list to store the words
tag_list = []

# Open the file and read its contents line by line
with open(file_path, "r") as file:
    for line in file:
        # Remove leading and trailing whitespace, then append the word to the list
        tag = line.strip()
        tag_list.append(tag)

with st.sidebar:
    st.write('Choose thread level and tags:')
    level_options = df['Level'].unique().tolist()
    levels =st.multiselect(label='Thread levels', options=level_options)
    col1, col2= st.columns(2)
    with col1:
        tags_options = tag_list
        tags =st.multiselect(label='Tags', options=tags_options)
        
    with col2:
        tags_choice = st.radio(label='',options=["AND", "OR"] , key='dsadsaxx')
        
    
    st.write('Choose rating range:')
    col1, col2= st.columns(2)
    with col1:
        min_val=st.number_input('min_value:' , help = 'Remember , that min value shoud by lower than max value',
                                min_value=df['Rating'].min(), value=df['Rating'].min())
    with col2:
        max_val=st.number_input(label='max_value:' ,help = 'Remember , that max value shoud by higher than min value', 
                                max_value=df['Rating'].max(), value=df['Rating'].max())
    st.write('Choose number of rows:')
    rows_limit=st.number_input('Limit number of recieved rows:',help = '0 stands for all rows',
                                min_value=0, max_value=df.shape[0], value=0)
    st.write('Choose order columns:')
        
    col1, col2= st.columns(2)
    with col1:
        level_activated = st.number_input(label='Level',min_value=0 , max_value=2, help= '0 - default , 1 - order by this column, 2 - priority order ')
    with col2:
        level_choice = st.radio(label='',options=["ASC", "DESC"])
    
    col1, col2= st.columns(2)
    with col1:
        tag_activated = st.number_input(label='Tag',min_value=0 , max_value=2, help= '0 - default , 1 - order by this column, 2 - priority order ')
    with col2:
        tag_choice = st.radio(label='',options=["ASC", "DESC"] , key='llplppl')
    
    
    
    if (level_activated == 1 and tag_activated == 1):
        st.warning('Seems like Order by priorities have both same value', icon="⚠️")
        
    elif (level_activated == 2 and tag_activated == 2):
        st.warning('Seems like Order by priorities have both same value', icon="⚠️")
    
    elif (level_activated == 2 and tag_activated == 0):
        st.warning('Seems like there is single 2 in order priority', icon="⚠️")
    
    elif (level_activated == 0 and tag_activated == 2):
        st.warning('Seems like there is single 2 in order priority', icon="⚠️")
    
    
        
    
    #sorted_df = df.sort_values(by=['A', 'B'], ascending=[True, False])
st.title('Diplomovka')


if levels:
    df = df[df['Level'].isin(levels)]

if tags and tags_choice == 'AND':
    df = df[df['Tags'].apply(lambda x: all(tag in x for tag in tags))]
elif tags and tags_choice == 'OR':
    df = df[df['Tags'].apply(lambda x: any(tag in x for tag in tags))]
    

if min_val and max_val:
    df = df[(df['Rating'] >= min_val) & (df['Rating'] <= max_val)]

if rows_limit:
    df = df.head(rows_limit)

if tag_activated == 1 and level_activated ==0:
    if tag_activated =='ASC':
        a = True
    else:
        a = False
    df=df.sort_values(by=['Tags'], ascending=[a])

elif tag_activated == 0 and level_activated ==1:
    if level_choice =='ASC':
        a = True
    else:
        a = False
    df=df.sort_values(by=['Level'], ascending=[a])

elif level_activated == 2 and tag_activated ==1:
    if level_choice =='ASC':
        a = True
    else:
        a = False
    df=df.sort_values(by=['Level','Tags'], ascending=[a,a])

elif level_activated == 1 and tag_activated ==2:
    if level_choice =='ASC':
        a = True
    else:
        a = False
    df=df.sort_values(by=['Tags','Level'], ascending=[a,a])






    
st.dataframe(data=df, hide_index=True,width=1000, height=700)

