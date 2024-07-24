import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# Load datasets
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

# Preprocess data
df = preprocessor.preprocess(df, region_df)

# Set up the sidebar title
st.sidebar.title('Olympics Analysis')

#Insert Olympics Symbols
st.sidebar.image('https://cdn.britannica.com/01/23901-050-33507FA4/flag-Olympic-Games.jpg')

# Create a radio button for user menu selection
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete-Wise Analysis')
)

# Medal Tally Section
if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    
    # Fetch years and countries for selection
    years, country = helper.country_year_list(df)
    
    # Dropdowns for selecting year and country
    selected_year = st.sidebar.selectbox('Selected Year', years)
    selected_country = st.sidebar.selectbox('Selected Country', country)
    
    # Fetch the medal tally based on selections
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    
    # Display titles based on the selections
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f'Medal Tally in {selected_year} Olympics')
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f'Overall Medal Tally of {selected_country}')
    else:
        st.title(f'{selected_country} Performance in {selected_year}')
    
    # Display the medal tally table
    st.table(medal_tally)

# Overall Analysis Section
if user_menu == 'Overall Analysis':
    # Calculate top statistics
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    
    # Display top statistics in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Countries")
        st.title(nations)
    
    # Plot participation of nations over time
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participation Nations over the years')
    st.plotly_chart(fig)
    
    # Plot number of events over time
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)
    
    # Plot number of athletes over time
    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title('No. of Athletes over the years')
    st.plotly_chart(fig)
    
    # Heatmap of the number of events over time for each sport
    st.title('No. of Events over time (Every Sport)')
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)
    
    # Display most successful athletes
    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    
    selected_sport = st.selectbox('Select a sport', sport_list)
    st.table(helper.most_successful(df, selected_sport))

# Country-Wise Analysis Section
if user_menu == 'Country-Wise Analysis':
    st.sidebar.title('Country-Wise Analysis')
    
    # Dropdown for selecting country
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    
    # Plot medal tally over the years for the selected country
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(f'{selected_country} Medal Tally over the Years')
    st.plotly_chart(fig)
    
    # Heatmap of sports in which the selected country excels
    st.title(f'{selected_country} excels in the following sports')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)
    
    # Display top 10 athletes of the selected country
    st.title(f'Top 10 athletes of {selected_country}')
    top10df = helper.most_successful_country(df, selected_country)
    st.table(top10df)

# Athlete-Wise Analysis Section
if user_menu == 'Athlete-Wise Analysis':
    st.title('Distribution of Age')
    
    # Drop duplicates and create age distributions
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    
    # Create and plot age distribution plot
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
    
    # Age distribution by sport for gold medalists
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions',
                     'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 
                     'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 
                     'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball',
                     'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics',
                     'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    
    x = []
    name = []
    
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_medalist_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        if not gold_medalist_ages.empty:
            x.append(gold_medalist_ages)
            name.append(sport)
    
    # Create and plot the distribution of ages for different sports
    if x:
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title('Distribution of Age with respect to Sports (Gold Medalists)')
        st.plotly_chart(fig)
    else:
        st.title('Distribution of Age with respect to Sports (Gold Medalists)')
        st.write('No data available for the specified sports and criteria.')
    
    # Scatter plot of height vs weight
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    
    selected_sport = st.selectbox('Select a sport', sport_list)
    
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', data=temp_df, hue='Medal', style='Sex', s=30)
    st.title('Height vs Weight')
    st.pyplot(fig)
    
    # Plot men vs women participation over the years
    st.title('Men vs Women Participation over the Years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)