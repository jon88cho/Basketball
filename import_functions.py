from pandas import read_html
import pandas as pd
from pandas import Series, DataFrame
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import urllib.request  #remove later
import os

def get_html(url, dirname = 'HTML', start_year = 1986, end_year = 2017):
    if not os.path.isdir('./' + dirname):
        os.mkdir(dirname)
    if '%d' not in url:
        print("Invalid string, needed '%d' place holder for year")
        return
    for year in range(start_year, end_year + 1):
        url = url % year
        s = url.split('/')
        name = "%s/%s_%s" % (dirname, s[-2], s[-1])
        urlretrieve(url, name)

#Pulling regular season team ratings from 1986 to 2017
def team_ratings (keep_html = True, dirname = 'HTML'):
    reg_team_rating_dframe = DataFrame()
    #download and save html
    if keep_html:
        os.mkdir(dirname)
        for year in range(1986,2018): #appends the rest of the dataframes
            url = 'https://www.basketball-reference.com/leagues/NBA_%d_ratings.html' % year
            name = '%s/leagues_NBA_%d_ratings.html' % (dirname, year)
            doc = urllib.request.URLopener()
            doc.retrieve(url, name)
    
    #process html from local into dataframe
    for year in range(1986,2017): #appends the rest of the dataframes
        name = '%s/leagues_NBA_%d_ratings.html' % (dirname, year)
        dframe_list = pd.io.html.read_html(name)
        df = dframe_list[0]
        df.columns = df.columns.droplevel() #drops the unnecessary hierachy
        df['Year'] = Series ([year for i in range(len(df.index))])
        reg_team_rating_dframe = reg_team_rating_dframe.append(df)


    #2017 season doesnt have the hierachy like the rest of the seasons, append separately
    url1 = '%s/leagues_NBA_2017_ratings.html' % dirname
    dframe_list1 = pd.io.html.read_html(url1)
    dframe17 = dframe_list1[0]
    dframe17['Year'] = Series ([2017 for i in range(len(dframe17.index))]) #year column
    reg_team_rating_dframe = reg_team_rating_dframe.append(dframe17)
    
    reg_team_rating_dframe = reg_team_rating_dframe.rename({"Rk":"Rank"},axis='columns')    #Feature Transformation
    reg_team_rating_dframe.to_csv("reg_team_rating_dframe.csv",index=False)
    return reg_team_rating_dframe

#Find the champion of each season
def Champion(keep_html = True, dirname = 'HTML'):
    Champions_df = DataFrame(columns = ['Year','Team'])
    if keep_html:
        for year in range (1986, 2018):
            champion_url = 'https://www.basketball-reference.com/playoffs/NBA_%d.html' %year
            name = '%s/playoffs_NBA_%d.html' % (dirname, year)
            doc = urllib.request.URLopener()
            doc.retrieve(champion_url, name)
        
    for year in range (1986,2018):
        name = '%s/playoffs_NBA_%d.html' % (dirname, year)
        r = open(name)
        soup = BeautifulSoup(r,'lxml')
        list1=[]
        for text in soup.find_all('p'):
            list1.append(text)
        element = list1[2]
        index = str(element).find(".html\">") 
        index = index + 7 #the starting index of the team
        Team = str(element)[index:str(element).find("</a><")] #substring "Team" is the team name
        series = Series (data = [year,Team],index = ['Year','Team'])
        Champions_df = Champions_df.append(series,ignore_index=True)
        Champions_df.to_csv('Champions_df.csv', index = False)
    return Champions_df

#Dataframe that details which round the team got eliminated
# 1 = Champion
# 2 = Runner's up
# 3 = Lost in the 3rd Round
# 4 = Lost in the 2nd Round
# 5 = Lost in the 1st Round
def playoff_elim (keep_html = True, dirname = 'HTML'):
    playoff_elim_df = DataFrame()
    if keep_html:
        for year in range(1986,2018):
            url1 = 'https://www.basketball-reference.com/playoffs/NBA_%d.html' % year
            name = '%s/playoffs_NBA_%d.html' % (dirname, year)
            doc = urllib.request.URLopener()
            doc.retrieve(url1, name)
        
    for x in range (1986,2018):
        name = '%s/playoffs_NBA_%d.html' % (dirname, x)
        dframe_list = pd.io.html.read_html(name)
        raw_dframe = dframe_list[16]
        teams_not_in_finals = raw_dframe['Team'][2:16]
        finalists = raw_dframe['Team'][0:2]
        df = DataFrame()
        positions = Series([0,1,2,3,3,4,4,4,4,5,5,5,5,5,5,5,5])
        df['Position'] = positions
        championsindex = int(x-1986)
        championteam = Champion_df.iloc[championsindex]['Team']
        teams = Champion_df.iloc[championsindex]
        finalists = finalists.loc[finalists != championteam]
        teams = teams.append(finalists,ignore_index=True)
        teams = teams.append(teams_not_in_finals,ignore_index=True)
        teams = teams.drop(index = [0])
        df['Teams'] = teams
        df['Year'] = Series(x,teams.index)
        df = df.drop(index= [0])
        playoff_elim_df = playoff_elim_df.append(df,ignore_index=True)
        playoff_elim_df.to_csv("playoff_elim_df.csv", index = False)
    return playoff_elim_df

def get_leagues_html(keep_html = True, dirname = 'HTML'):
    #download html into specified directory
    per_game_all = pd.DataFrame()
    per_poss_all = pd.DataFrame()
    if keep_html:
        for year in range(1986, 2018):
            url = "https://www.basketball-reference.com/leagues/NBA_%d.html" % year
            name = dirname + "/leagues_NBA_%d.html" % year
            doc = urllib.request.URLopener()
            doc.retrieve(url, name)            
    for year in range(1986, 2018):
        name = dirname + "/leagues_NBA_%d.html" % year
        #read saved file and write relevant parts to new html
        code = open(name).read()
        start = code.find('<div id="all_team-stats-per_game" class="table_wrapper setup_commented commented">')
        end = code.find('<!-- fs_btf_2 -->')
        code = code[start:end]
        code = code.replace('<!--', '') #the tables are commented out orginally
        code = code.replace('-->', '')  #this clears that so pandas can read them
        
        cleaned_name = name[:len(name) - 5] + '_cleaned.html'
        cleaned_html = open(cleaned_name, 'w')
        cleaned_html.write(code)
        cleaned_html.close()
        #read in the tables from cleaned html
        #order is: team per game, opponent per game, team-stats-base, opponent-stats-base, team-stats-per poss, opponent-per-poss
        df_list = pd.io.html.read_html(cleaned_name)
        #drop league averages
        for i in range(len(df_list)):
            df_list[i] = df_list[i].drop(len(df_list[i])-1)
        #drop NaN rows and columns (resulting from whitespace in html)
        df_list = [df.T.dropna().T for df in df_list]
        
        column_names = {0: "_game", 1: "_opp_game", 4: "_poss", 5: "_opp_poss"} #see comment on order of dfs above
        for i in range(len(df_list)):
            if i ==2 or i == 3:
                continue
            else:
                #set index to team name (for concatenation later)
                df_list[i].index = df_list[i]['Team']
                #change name to more easily identify df
                new_clmns = {clmn: clmn + column_names[i] for clmn in df_list[i]}
                df_list[i] = df_list[i].rename(index = str, columns = new_clmns)
        
        #concatenate team and opponent stats
        per_game = pd.concat([df_list[0], df_list[1]], axis = 1)
        per_poss = pd.concat([df_list[4], df_list[5]], axis=1)
        per_game['Year'] = pd.Series([year for i in range(len(per_game.index))], index=per_game.index)
        per_poss['Year'] = pd.Series([year for i in range(len(per_poss.index))], index=per_poss.index)
        per_game_all = per_game_all.append(per_game)
        per_poss_all = per_poss_all.append(per_poss)
    
    per_game_all.to_csv("per_game_all.csv", index=False)
    per_poss_all.to_csv("per_poss_all.csv", index=False)
    return per_game_all, per_poss_all


