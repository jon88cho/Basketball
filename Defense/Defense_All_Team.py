import pandas as pd
from pandas import Series, DataFrame
#This will return 2 DataFrames
def get_all_defense():
    html = 'https://www.basketball-reference.com/awards/all_defense.html' #link for all team defenses
    dframe_list = pd.io.html.read_html(html)
    All_Defense_df = dframe_list[0]
    #formatting
    x = list(range(2,155,3))
    All_Defense_df = All_Defense_df.drop(x)
    #Only 1996-2017 data
    recent_df = All_Defense_df[:44]
    #Transpose the dataframe for formatting purposes
    transposed = recent_df.ix[:,[3,4,5,6,7]].transpose()
    transposed.columns = [''] * len(transposed.columns)
    #Create first team DataFrame
    First_Team = DataFrame(columns = ['Player','Year'])
    year= 2017
    for i in range (0,44,2):
        temp_df = DataFrame(columns = ['Player','Year'])
        temp_df['Player']= transposed.iloc[:,[i]].reset_index().drop(columns = ['index'])
        temp_df['Year']= Series ([year for k in range(len(temp_df['Player'].index))])
        year = year -1
        First_Team = First_Team.append(temp_df)
    First_Team = First_Team.reset_index().drop(columns = ['index'])
    #Create second team DataFrame
    Second_Team = DataFrame(columns = ['Player','Year'])
    year = 2017
    for i in range (1,45,2):
        temp_df = DataFrame(columns = ['Player','Year'])
        temp_df['Player']= transposed.iloc[:,[i]].reset_index().drop(columns = ['index'])
        temp_df['Year']= Series ([year for k in range(len(temp_df['Player'].index))])
        year = year -1
        Second_Team = Second_Team.append(temp_df)
    Second_Team = Second_Team.reset_index().drop(columns = ['index'])
    #Some years have ties, which needs to be resolved
    First_Team.loc[24:25].Player = "Tyson Chandler"
    temp_df1 = DataFrame(columns = ['Player','Year'])
    temp_df1['Player'] = Series(["Joakim Noah"])
    temp_df1['Year'] = Series([2013])
    First_Team = First_Team.append(temp_df1)

    First_Team.loc[59:60].Player = "Kobe Bryant"
    temp_df2 = DataFrame(columns = ['Player','Year'])
    temp_df2['Player'] = Series(["Jason Kidd"])
    temp_df2['Year'] = Series([2006])
    First_Team = First_Team.append(temp_df2)

    Second_Team.loc[64:65].Player = "Dwyane Wade"

    temp_df3 = DataFrame(columns = ['Player','Year'])
    temp_df3['Player'] = Series(["Jason Kidd"])
    temp_df3['Year'] = Series([2005])
    Second_Team = Second_Team.append(temp_df3)

    #Sort the entries back to descending year order
    First_Team = First_Team.sort_values(['Year'], ascending=False)
    Second_Team = Second_Team.sort_values(['Year'], ascending=False)
    First_Team = First_Team.reset_index().drop(columns = ['index'])
    Second_Team = Second_Team.reset_index().drop(columns = ['index'])
    return First_Team,Second_Team

