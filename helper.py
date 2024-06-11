import numpy as np
import pandas as pd

# Function to calculate the medal tally
def medal_tally(df):
    # Remove duplicates based on specific columns to get unique medal entries
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    # Group by 'NOC' (National Olympic Committee) and sum the medal counts
    medal_tally = medal_tally.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False)
    # Calculate the total number of medals
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

# Function to generate lists of years and countries
def country_year_list(df):
    # Get a list of unique years and sort it
    years = df['Year'].unique().tolist()
    years.sort()
    # Insert 'Overall' at the beginning of the list
    years.insert(0, 'Overall')

    # Get a sorted list of unique country names from the 'region' column
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    # Insert 'Overall' at the beginning of the list
    country.insert(0, 'Overall')
    return years, country

# Function to fetch the medal tally based on year and country selection
def fetch_medal_tally(df, year, country):
    flag = 0
    # Remove duplicates to get unique medal entries
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    
    # Filter the dataframe based on the selections
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    
    # Group and sum the medals based on the flag
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    
    # Calculate the total number of medals
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

# Function to create a DataFrame showing data over time
def data_over_time(df, col):
    # Create a DataFrame counting the number of unique entries per year for the given column
    nations_over_time = pd.DataFrame(df.drop_duplicates(['Year', col])['Year'].value_counts().sort_index()).reset_index()
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nations_over_time

# Function to find the most successful athletes in a specific sport or overall
def most_successful(df, sport):
    # Drop rows with missing medals
    temp_df = df.dropna(subset=['Medal'])
    # Filter by sport if a specific sport is selected
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    # Count medals per athlete and merge with the original DataFrame to get additional info
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x

# Function to get the year-wise medal tally for a specific country
def yearwise_medal_tally(df, country):
    # Drop rows with missing medals and remove duplicates
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    # Filter by country
    new_df = temp_df[temp_df['region'] == country]
    # Group by year and count the medals
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

# Function to create a heatmap of country performance in various sports over the years
def country_event_heatmap(df, country):
    # Drop rows with missing medals and remove duplicates
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    # Filter by country
    new_df = temp_df[temp_df['region'] == country]
    # Create a pivot table with sports as rows and years as columns
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

# Function to find the most successful athletes from a specific country
def most_successful_country(df, country):
    # Drop rows with missing medals and filter by country
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    # Count medals per athlete and merge with the original DataFrame to get additional info
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x

# Function to get height vs weight data for a specific sport or overall
def weight_v_height(df, sport):
    # Drop duplicates to get unique athlete entries
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    # Fill missing medals with 'No Medal'
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    # Filter by sport if a specific sport is selected
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

# Function to compare male vs female participation over the years
def men_vs_women(df):
    # Drop duplicates to get unique athlete entries
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    # Group by year and count male and female participants
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    # Merge male and female counts and rename columns
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final