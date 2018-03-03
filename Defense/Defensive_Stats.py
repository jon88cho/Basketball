
import pandas as pd
from pandas import Series, DataFrame


#Helper function to clean up the player names with a space in front of them
def cleanup (name):
    return name[1:]
def cleanup_index(name):
    for i in range(1,(len(name)-1)):
        name.values[i] = name.values[i][1:]
#Will return 1 dataframe
def player_stats():
    Player_info = DataFrame()
    for i in range (1986,2017):
        url = 'https://www.basketball-reference.com/leagues/NBA_%d_per_game.html' % (i)
        dframe_list = pd.io.html.read_html(url)
        temp_df = dframe_list[0]
        temp_df['Year'] = Series ([i for j in range(len(temp_df.index))])
        Player_info = Player_info.append(temp_df)
    return Player_info
#Will return 4 dataframes
def Defensive_Stats():
    #Defense Tracking
    Defensive_Tracking = DataFrame()
    for i in range (13,18):
        df = pd.read_csv("Player_Csvs/Defense_Tracking/Defense%d.csv" % (i))
        df['Year'] = Series ([2000+i for k in range(len(df.index))])
        Defensive_Tracking = Defensive_Tracking.append(df)
    cleanup_index(Defensive_Tracking.columns)
    Defensive_Tracking = Defensive_Tracking.rename(columns = {'TEAM_ABBREVIATION':'Team','PLAYER_NAME': 'Player'})
    Defensive_Tracking['Player'] = Defensive_Tracking['Player'].apply(cleanup)
    Defensive_Tracking['Year'] = Defensive_Tracking['Year'].astype(float)
    #Defense_General
    Defense_General = DataFrame()
    for i in range (96,100):
        df1 = pd.read_csv("Player_Csvs/Defensive_General/Defense%d.csv" % (i))
        df1['Year'] = Series ([i+1900 for k in range(len(df1.index))])
        Defense_General = Defense_General.append(df1)

    for j in range (18):
        df2 = pd.read_csv("Player_Csvs/Defensive_General/Defense%d.csv" % (j))
        df2['Year'] = Series ([j+2000 for k in range(len(df2.index))])
        Defense_General = Defense_General.append(df2)
    cleanup_index(Defense_General.columns)
    Defense_General = Defense_General.rename(columns = {'TEAM_ABBREVIATION':'Team','PLAYER_NAME': 'Player','AGE':'Age'})
    Defense_General['Player'] = Defense_General['Player'].astype(str).apply(cleanup)
    Defense_General['Team'] = Defense_General['Team'].astype(str).apply(cleanup)
    Defense_General['Year'] = Defense_General['Year'].astype(float)
        
    #Shooting
    Shooting = DataFrame()
    for i in range (96,100):
        df1 = pd.read_csv("Player_Csvs/Opponent_Shooting/Shooting%d.csv" % (i))
        df1['Year'] = Series ([i+1900 for k in range(len(df1.index))])
        Shooting = Shooting.append(df1)
    for j in range (18):
        df2 = pd.read_csv("Player_Csvs/Opponent_Shooting/Shooting%d.csv" % (j))
        df2['Year'] = Series ([j+2000 for k in range(len(df2.index))])
        Shooting = Shooting.append(df2)
    Shooting = Shooting.rename(columns = {' TEAM_ABBREVIATION':'Team',' OPP_FGM': "Less than 5 Ft FGM", ' OPP_FGA' : "Less than 5 Ft FGA",
           ' OPP_FG_PCT' : "Less than 5 Ft FG%",
                   ' OPP_FGM.1': "5-9 Ft GM", ' OPP_FGA.1' : "5-9 Ft FGA",
           ' OPP_FG_PCT.1' : "5-9 Ft FG%",
                   ' OPP_FGM.2': "10-14 Ft FGM", ' OPP_FGA.2' : "10-14 Ft FGA",
           ' OPP_FG_PCT.2' : "10-14 Ft FG%",
                   ' OPP_FGM.3': "15-19 Ft FGM", ' OPP_FGA.3' : "15-19 Ft FGA",
           ' OPP_FG_PCT.3' : "15-19 Ft FG%",
                   ' OPP_FGM.4': "20-24 Ft FGM", ' OPP_FGA.4' : "20-24 Ft FGA",
           ' OPP_FG_PCT.4' : "20-24 Ft FG%",
                   ' OPP_FGM.5': "25-29 Ft FGM", ' OPP_FGA.5' : "25-29 Ft FGA",
           ' OPP_FG_PCT.5' : "25-20 Ft FG%"," PLAYER_NAME":"Player"," AGE":"Age"})
    Shooting['Team'] = Shooting['Team'].astype(str).apply(cleanup)
    Shooting['Player'] = Shooting['Player'].astype(str).apply(cleanup)
    Shooting = Shooting.drop(['PLAYER_ID',' TEAM_ID',' OPP_FGM.6',' OPP_FGA.6',' OPP_FG_PCT.6',' OPP_FGM.7',
                   ' OPP_FGA.7',' OPP_FG_PCT.7',' OPP_FGM.8',' OPP_FG_PCT.8','Age','Team'],axis=1)

    #Hustle Stats
    Hustle = DataFrame()
    for i in range (15,18):
        df = pd.read_csv("Player_Csvs/Hustle/Hustle%d.csv" % (i))
        df['Year'] = Series ([2000+i for k in range(len(df.index))])
        Hustle = Hustle.append(df)
    cleanup_index(Hustle.columns)
    Hustle = Hustle.rename(columns = {'PLAYER_NAME':"Player","TEAM_ABBREVIATION":"Team"})
    Hustle['Player'] = Hustle['Player'].astype(str).apply(cleanup)
    
    return Defensive_Tracking,Defense_General,Shooting,Hustle
