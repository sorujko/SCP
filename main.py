import streamlit as st
import pandas as pd
import numpy as np
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import random

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
        tags_choice = st.radio(label='',options=["OR", "AND"] , key='dsadsaxx')
        
    
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

if tag_activated == 1 and level_activated == 0:
    # Create a custom sorting key based on the presence of chosen tags
    def custom_tag_sort(tags_list):
        chosen_tags_present = [tag for tag in tags if tag in tags_list]
        return len(chosen_tags_present)

    # Apply the custom sorting key to the DataFrame
    df['TagSortKey'] = df['Tags'].apply(custom_tag_sort)

    # Sort the DataFrame based on the custom sorting key
    if tag_choice == 'ASC':
        df = df.sort_values(by='TagSortKey', ascending=True).drop(columns=['TagSortKey'])
    else:
        df = df.sort_values(by='TagSortKey', ascending=False).drop(columns=['TagSortKey'])

# ... (rest of your code for displaying the DataFrame)


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
    
    # Create a custom sorting key based on the presence of chosen tags
    def custom_tag_sort(tags_list):
        chosen_tags_present = [tag for tag in tags if tag in tags_list]
        return len(chosen_tags_present)

    # Apply the custom sorting key to the DataFrame
    df['TagSortKey'] = df['Tags'].apply(custom_tag_sort)

    # Sort the DataFrame based on the custom sorting key
    if tag_choice == 'ASC':
        b=True
    else:
        b= False
    
    df=df.sort_values(by=['Level','TagSortKey'], ascending=[a,b]).drop(columns=['TagSortKey'])

elif level_activated == 1 and tag_activated ==2:
    if level_choice =='ASC':
        a = True
    else:
        a = False
    
    # Create a custom sorting key based on the presence of chosen tags
    def custom_tag_sort(tags_list):
        chosen_tags_present = [tag for tag in tags if tag in tags_list]
        return len(chosen_tags_present)

    # Apply the custom sorting key to the DataFrame
    df['TagSortKey'] = df['Tags'].apply(custom_tag_sort)

    # Sort the DataFrame based on the custom sorting key
    if tag_choice == 'ASC':
        b=True
    else:
        b= False
    
    df=df.sort_values(by=['TagSortKey','Level'], ascending=[b,a]).drop(columns=['TagSortKey'])






    
tab1, tab2 = st.tabs(["DataFrame", "Graphs"])

with tab1:    
    st.dataframe(data=df, hide_index=True,width=1000, height=700)
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')


    csv = convert_df(df)

    st.download_button(
    "Press to Download",
    csv,
    "SCP_Dataset.csv",
    "text/csv",
    key='download-csv'
    )



with tab2:

    if not levels :
        st.write("Pre zobrazenie grafu Levelov  vyberte nejaké z ponuky")
    else:
        a=df['Level'].value_counts().to_dict()
        a = dict(list(a.items())[:3])
    
        farby=[]
        for item in a.keys():
            farby.append(f'#{random.randrange(256**3):06x}')
        fig = make_subplots(rows=1, cols=2 ,specs=[[{'type': 'xy'},{'type': 'domain'}]] )

        fig.add_trace(
            go.Bar(x=list(a.keys()), y=list(a.values()),marker=dict(color=farby), 
                showlegend=False ,name='',hovertemplate='Level=%{x}, pocet=%{y}') ,
            row=1, col=1
        )

        fig.add_trace(
            go.Pie(labels=list(a.keys()), values=list(a.values()),marker=dict(colors=farby),name='',
                hovertemplate='Level: %{label}<br>pocet: %{value}<br>percento: %{percent}'),
            row=1, col=2
        )

        st.plotly_chart(fig)
    
    if tags and tags_choice == 'OR':
        # Initialize a dictionary to store tag counts
        tag_counts = {}
        
        
        
        # Count the number of rows for each selected tag
        for tag in tags:
            tag_counts[tag] = df[df['Tags'].str.contains(tag)].shape[0]

        farby=[]
        for item in tag_counts.keys():
            farby.append(f'#{random.randrange(256**3):06x}')
        
        # Convert the dictionary to lists for plotting
        tag_labels = list(tag_counts.keys())
        tag_values = list(tag_counts.values())

        
            # Create a subplot with two Pie Charts
        fig = make_subplots(rows=1, cols=2 ,specs=[[{'type': 'xy'},{'type': 'domain'}]] )

        fig.add_trace(
            go.Bar(x=tag_labels, y=tag_values,marker=dict(color=farby), 
                showlegend=False ,name='',hovertemplate='Tag=%{x}, pocet=%{y}') ,
            row=1, col=1
        )

        fig.add_trace(
            go.Pie(labels=tag_labels, values=tag_values,marker=dict(colors=farby),name='',
                hovertemplate='Tag: %{label}<br>pocet: %{value}<br>percento: %{percent}'),
            row=1, col=2
        )

        st.plotly_chart(fig)
    else:
        st.write("Pre zobrazenie grafu Tagov  vyberte nejaké z ponuky (musí byť nastavené OR)")

