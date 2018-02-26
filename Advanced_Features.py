import scipy
import pandas as pd
import numpy as np
from pandas import DataFrame,Series
#make sure to specify the year this distribution is run
def Correlated_Gaussian_Winning_Percentage(df,year):
    df = df[df['Year']==year] #gives the entire dataframe
    Allowed_series = df['Points_Allowed']
    Scored_series = df['Points_Scored']
    list_of_percentages = DataFrame(columns = ['Team','Percentage'])
    for team in range(len(df.index)):
        percent = scipy.norm.cdf(team['Points_Scored']-team['Points Allowed'])/((Allowed_series-Scored_series).std())
        series = Series ([team,percent],index = ['Team','Percentage'])
        list_of_percentages = list_of_percentages.append(series,ignore_index=True)

    list_of_percentages['Year']=Series ([year for i in range(len(list_of_percentages.index))])
    return list_of_percentages
#Correlated_Gaussian_Winning_Percentage(df,year)
#Assist Ratio is the percentage of a team’s possessions that ends in an assist.
#This stat is probably a good predictor because a team that has "good ball movement" tend to win (might be wrong obv)
def assist_ratio (Team):
    Assists,FGA,FTA,TO = Team
    return (((Assists)*100)/ ((FGA)+(FTA*0.44)+(Assists)+(TO)))
#df['assist_ratio'] = df[['Assists','FGA','FTA','TO']].apply(assist_ratio,axis=1)
#The method that gives an expected winning percentage using the ratio of a team’s wins and losses
#is related to the number of points scored and allowed.
def Pythagorean_Winning_Percentage(team):
    Points_Scored,Points_Allowed = team
    return (np.power(Points_Scored,16.5)/(np.power(Points_Scored,16.5)+np.power(Points_Allowed,16.5)))
#df['pythag_win_percentage'] = df[['Points_Scored','Points_Allowed']].apply(Pythagorean_Winning_Percentage,axis=1)
#The numerical gap between a team’s offensive efficiency and defensive efficiency.
#The differential represents what each team did for the entire season
#and a team’s efficiency differential is a better predictor of future success.
def Efficiency_Differential(team):
    Offensive_Efficiency,Defensive_Efficiency = team
    return ((Offensive_Efficiency)-(Defensive_Efficiency))
#df['efficiency_diff'] = df[['Off_eff'],['Def_eff']].apply(Efficiency_Differential,axis=1)
def transition_defense(team):
    Opponent_Fast_Break_Points, Opponent_Steals = team
    return ((Opponent_Fast_Break_Points)/(Opponent_Steals))
    #I don't think this formula is particularly accurate
    #because transition offense can be initiated in other ways
def transition_offense(team):
    Fast_Break_Points,Steals = team
    return ((Fast_Break_Points)/(Steals))
#I don't think this formula is particularly accurate
#because transition offense can be initiated in other ways
#this stat might be a good indicator if a team is a "rough and tough" team as opposed to a finesse team
#or it might indicate that the team has a dominant big man.
def Defensive_Rebouding_Percentage(team):
    Defensive_Rebounds,Opponent_Offensive_Rebounds = team
    return((Defensive_Rebounds)/((Defensive_Rebounds)+(Opponent_Offensive_Rebounds)))
#this stat might be a good indicator if a team is a "rough and tough" team as opposed to a finesse team
#or it might indicate that the team has a dominant big man.
def Offensive_Rebounding_Percentage(team):
    Offensive_Rebounds,Opponent_Defensive_Rebounds = team
    return ((Offensive_Rebounds)/((Offensive_Rebounds)+(Opponent_Defensive_Rebounds)))
#number of possessions a team has
def possessions (team):
    FGA,Turnovers,FTA,Offensive_Rebounds= team
    return 0.96*((FGA)+(Turnovers)+0.44*(FTA)-(Offensive_Rebounds))
#shows how fast a team plays
def pace (team):
    Team_Minutes,Possession_Team,Possession_Opponent = team
    return ((240/(Team_Minutes))*((Possession_Team+Possession_Opponent)/2))
#The metric that indicates the percentage of the time a team will score if not sent to the free throw line.
def play_percentage(team):
    FGM,FGA,Offensive_Rebounds,Turnovers = team
    return (FGM/(FGA-Offensive_Rebounds+Turnovers))
#Turnover Ratio is the percentage of a team’s possessions that end in a turnover.
#this is likely to be a pretty good indicator as teams which take care of the ball are better (might be wrong)
def Turnover_Ratio(team):
    Turnovers,FGA,FTA,Assists,Turnovers = team
    return ((Turnovers*100)/ ((FGA)+(FTA*0.44)+(Assists)+(Turnovers)))