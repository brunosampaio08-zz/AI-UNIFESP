import pandas as pd
import sklearn
import numpy as np
import time

from ast import literal_eval
from sklearn import neighbors, tree, svm, neural_network
from sklearn import preprocessing

if __name__ == "__main__":
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_columns', None)

    start_time = time.time()
    col_df = pd.read_csv("INPUT/_columns.csv")
    raw_df = pd.read_csv("INPUT/LeagueofLegends.csv")

    #Just delete the columns that doesn't matter
    del raw_df['Address']
    del raw_df['Season']
    del raw_df['League']
    del raw_df['Year']
    del raw_df['Type']
    del raw_df['blueTeamTag']
    del raw_df['redTeamTag']
    #Blue and red gold don't matter because we'll use golddiff
    del raw_df['goldblue']
    del raw_df['goldred']
    del raw_df['blueBans']
    del raw_df['redBans']

    # print(raw_df.columns)

    #Some columns are not really lists, they are strings that look like lists
    #So we should convert them to actual lists
    raw_df['golddiff'] = raw_df['golddiff'].apply(literal_eval)

    raw_df['bKills'] = raw_df['bKills'].apply(literal_eval)
    raw_df['bTowers'] = raw_df['bTowers'].apply(literal_eval)
    raw_df['bInhibs'] = raw_df['bInhibs'].apply(literal_eval)
    raw_df['bDragons'] = raw_df['bDragons'].apply(literal_eval)
    raw_df['bBarons'] = raw_df['bBarons'].apply(literal_eval)
    raw_df['bHeralds'] = raw_df['bHeralds'].apply(literal_eval)
    
    raw_df['goldblueTop'] = raw_df['goldblueTop'].apply(literal_eval)
    raw_df['goldblueJungle'] = raw_df['goldblueJungle'].apply(literal_eval)
    raw_df['goldblueMiddle'] = raw_df['goldblueMiddle'].apply(literal_eval)
    raw_df['goldblueADC'] = raw_df['goldblueADC'].apply(literal_eval)
    raw_df['goldblueSupport'] = raw_df['goldblueSupport'].apply(literal_eval)
    
    raw_df['rKills'] = raw_df['rKills'].apply(literal_eval)
    raw_df['rTowers'] = raw_df['rTowers'].apply(literal_eval)
    raw_df['rInhibs'] = raw_df['rInhibs'].apply(literal_eval)
    raw_df['rDragons'] = raw_df['rDragons'].apply(literal_eval)
    raw_df['rBarons'] = raw_df['rBarons'].apply(literal_eval)
    raw_df['rHeralds'] = raw_df['rHeralds'].apply(literal_eval)
    
    raw_df['goldredTop'] = raw_df['goldredTop'].apply(literal_eval)
    raw_df['goldredJungle'] = raw_df['goldredJungle'].apply(literal_eval)
    raw_df['goldredMiddle'] = raw_df['goldredMiddle'].apply(literal_eval)
    raw_df['goldredADC'] = raw_df['goldredADC'].apply(literal_eval)
    raw_df['goldredSupport'] = raw_df['goldredSupport'].apply(literal_eval)

    # print((raw_df['golddiff']))
    # print(type(raw_df['golddiff'][0][0]))

    backup_df = raw_df.copy()

    #Since these features are lists, turn them into separate columns

    #We'll have 5 gold diff columns:
    #   gold 0-9min; gold  10-19min; gold 20-29min; gold 30-39min; gold 40+ min
    #If the match ended before 40 min, copy the last gold to the remaining columns
    #So that they don't remain empty

    gold_columns = [[], [], [], [], []]
    
    curr_gold_avg = 0
    for gold_list in raw_df['golddiff']:
        time_count = 0
        list_count = 0

        for item in gold_list:
            curr_gold_avg += item
            time_count += 1

            if time_count%10 == 0 and time_count != 0 and time_count < 41:
                curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))
                gold_columns[list_count].append(curr_gold_avg)
                curr_gold_avg = 0
                list_count += 1
        

        #Get the avg for time > 40
        if time_count-(list_count*10) != 0:
            curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))

        #While list_count < 5, append the last avg to the lists
        while list_count < 5:
            if curr_gold_avg != 0:
                gold_columns[list_count].append(curr_gold_avg)
            else:
                gold_columns[list_count].append(gold_columns[list_count-1][-1])
            list_count += 1

    raw_df['gold_0_9'] = gold_columns[0]
    raw_df['gold_10_19'] = gold_columns[1]
    raw_df['gold_20_29'] = gold_columns[2]
    raw_df['gold_30_39'] = gold_columns[3]
    raw_df['gold_40'] = gold_columns[4]

    # for k in range(len(gold_columns[0])):
    #     print([gold_columns[j][k] for j in range(5)])

    #For kills, we'll have only one column, containing the number of kills
    #The champion that killed could matter, but we'll address that later

    kills = []

    for kill_list in raw_df['bKills']:
        kills.append(len(kill_list))

    raw_df['bKills'] = kills

    kills = []

    for kill_list in raw_df['rKills']:
        kills.append(len(kill_list))

    raw_df['rKills'] = kills

    #Same goes for towers, inhibs, dragons, barons and heralds

    #Towers
    Towers = []

    for Tower_list in raw_df['bTowers']:
        Towers.append(len(Tower_list))

    raw_df['bTowers'] = Towers

    Towers = []

    for Tower_list in raw_df['rTowers']:
        Towers.append(len(Tower_list))

    raw_df['rTowers'] = Towers

    #Inhibitors
    Inhibs = []

    for Inhib_list in raw_df['bInhibs']:
        Inhibs.append(len(Inhib_list))

    raw_df['bInhibs'] = Inhibs

    Inhibs = []

    for Inhib_list in raw_df['rInhibs']:
        Inhibs.append(len(Inhib_list))

    raw_df['rInhibs'] = Inhibs

    #Dragons
    #Note that since dragons changed from gold drake to elemental drakes in May 2016
    #They might generate bias or error, might remove later
    Dragons = []

    for Dragon_list in raw_df['bDragons']:
        Dragons.append(len(Dragon_list))

    raw_df['bDragons'] = Dragons

    Dragons = []

    for Dragon_list in raw_df['rDragons']:
        Dragons.append(len(Dragon_list))

    raw_df['rDragons'] = Dragons

    #Barons
    Barons = []

    for Baron_list in raw_df['bBarons']:
        Barons.append(len(Baron_list))

    raw_df['bBarons'] = Barons

    Barons = []

    for Baron_list in raw_df['rBarons']:
        Barons.append(len(Baron_list))

    raw_df['rBarons'] = Barons

    #Heralds
    #Note that since heralds were added to the game in Nov. 2015, they might
    #Generate a bias or error, might remove later
    Heralds = []

    for Herald_list in raw_df['bHeralds']:
        Heralds.append(len(Herald_list))

    raw_df['bHeralds'] = Heralds

    Heralds = []

    for Herald_list in raw_df['rHeralds']:
        Heralds.append(len(Herald_list))

    raw_df['rHeralds'] = Heralds

    #Here we'll mitigate the effect of only counting kills and not champion that killed
    #Since most gold comes from killing, it's actually kinda equivalent
    #Similar to golddiff, create 5 columns for each player's gold value
    #Using avg_gold every 10 minutes

    #Blue team
    #Blue toplaner
    gold_columns = [[], [], [], [], []]
    
    curr_gold_avg = 0
    for gold_list in raw_df['goldblueTop']:
        time_count = 0
        list_count = 0

        for item in gold_list:
            curr_gold_avg += item
            time_count += 1

            if time_count%10 == 0 and time_count != 0 and time_count < 41:
                curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))
                gold_columns[list_count].append(curr_gold_avg)
                curr_gold_avg = 0
                list_count += 1
        

        #Get the avg for time > 40
        if time_count-(list_count*10) != 0:
            curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))

        #While list_count < 5, append the last avg to the lists
        while list_count < 5:
            if curr_gold_avg != 0:
                gold_columns[list_count].append(curr_gold_avg)
            else:
                gold_columns[list_count].append(gold_columns[list_count-1][-1])
            list_count += 1

    raw_df['bTop_gold_0_9'] = gold_columns[0]
    raw_df['bTop_gold_10_19'] = gold_columns[1]
    raw_df['bTop_gold_20_29'] = gold_columns[2]
    raw_df['bTop_gold_30_39'] = gold_columns[3]
    raw_df['bTop_gold_40'] = gold_columns[4]

    #Blue jungler
    gold_columns = [[], [], [], [], []]
    
    curr_gold_avg = 0
    for gold_list in raw_df['goldblueJungle']:
        time_count = 0
        list_count = 0

        for item in gold_list:
            curr_gold_avg += item
            time_count += 1

            if time_count%10 == 0 and time_count != 0 and time_count < 41:
                curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))
                gold_columns[list_count].append(curr_gold_avg)
                curr_gold_avg = 0
                list_count += 1
        

        #Get the avg for time > 40
        if time_count-(list_count*10) != 0:
            curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))

        #While list_count < 5, append the last avg to the lists
        while list_count < 5:
            if curr_gold_avg != 0:
                gold_columns[list_count].append(curr_gold_avg)
            else:
                gold_columns[list_count].append(gold_columns[list_count-1][-1])
            list_count += 1

    raw_df['bJungle_gold_0_9'] = gold_columns[0]
    raw_df['bJungle_gold_10_19'] = gold_columns[1]
    raw_df['bJungle_gold_20_29'] = gold_columns[2]
    raw_df['bJungle_gold_30_39'] = gold_columns[3]
    raw_df['bJungle_gold_40'] = gold_columns[4]

    #Blue midlaner
    gold_columns = [[], [], [], [], []]
    
    curr_gold_avg = 0
    for gold_list in raw_df['goldblueMiddle']:
        time_count = 0
        list_count = 0

        for item in gold_list:
            curr_gold_avg += item
            time_count += 1

            if time_count%10 == 0 and time_count != 0 and time_count < 41:
                curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))
                gold_columns[list_count].append(curr_gold_avg)
                curr_gold_avg = 0
                list_count += 1
        

        #Get the avg for time > 40
        if time_count-(list_count*10) != 0:
            curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))

        #While list_count < 5, append the last avg to the lists
        while list_count < 5:
            if curr_gold_avg != 0:
                gold_columns[list_count].append(curr_gold_avg)
            else:
                gold_columns[list_count].append(gold_columns[list_count-1][-1])
            list_count += 1

    raw_df['bMid_gold_0_9'] = gold_columns[0]
    raw_df['bMid_gold_10_19'] = gold_columns[1]
    raw_df['bMid_gold_20_29'] = gold_columns[2]
    raw_df['bMid_gold_30_39'] = gold_columns[3]
    raw_df['bMid_gold_40'] = gold_columns[4]

    #Blue adc
    gold_columns = [[], [], [], [], []]
    
    curr_gold_avg = 0
    for gold_list in raw_df['goldblueADC']:
        time_count = 0
        list_count = 0

        for item in gold_list:
            curr_gold_avg += item
            time_count += 1

            if time_count%10 == 0 and time_count != 0 and time_count < 41:
                curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))
                gold_columns[list_count].append(curr_gold_avg)
                curr_gold_avg = 0
                list_count += 1
        

        #Get the avg for time > 40
        if time_count-(list_count*10) != 0:
            curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))

        #While list_count < 5, append the last avg to the lists
        while list_count < 5:
            if curr_gold_avg != 0:
                gold_columns[list_count].append(curr_gold_avg)
            else:
                gold_columns[list_count].append(gold_columns[list_count-1][-1])
            list_count += 1

    raw_df['bADC_gold_0_9'] = gold_columns[0]
    raw_df['bADC_gold_10_19'] = gold_columns[1]
    raw_df['bADC_gold_20_29'] = gold_columns[2]
    raw_df['bADC_gold_30_39'] = gold_columns[3]
    raw_df['bADC_gold_40'] = gold_columns[4]

    #Blue support
    gold_columns = [[], [], [], [], []]
    
    curr_gold_avg = 0
    for gold_list in raw_df['goldblueSupport']:
        time_count = 0
        list_count = 0

        for item in gold_list:
            curr_gold_avg += item
            time_count += 1

            if time_count%10 == 0 and time_count != 0 and time_count < 41:
                curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))
                gold_columns[list_count].append(curr_gold_avg)
                curr_gold_avg = 0
                list_count += 1
        

        #Get the avg for time > 40
        if time_count-(list_count*10) != 0:
            curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))

        #While list_count < 5, append the last avg to the lists
        while list_count < 5:
            if curr_gold_avg != 0:
                gold_columns[list_count].append(curr_gold_avg)
            else:
                gold_columns[list_count].append(gold_columns[list_count-1][-1])
            list_count += 1

    raw_df['bSupp_gold_0_9'] = gold_columns[0]
    raw_df['bSupp_gold_10_19'] = gold_columns[1]
    raw_df['bSupp_gold_20_29'] = gold_columns[2]
    raw_df['bSupp_gold_30_39'] = gold_columns[3]
    raw_df['bSupp_gold_40'] = gold_columns[4]

    #red team
    #red toplaner
    gold_columns = [[], [], [], [], []]
    
    curr_gold_avg = 0
    for gold_list in raw_df['goldredTop']:
        time_count = 0
        list_count = 0

        for item in gold_list:
            curr_gold_avg += item
            time_count += 1

            if time_count%10 == 0 and time_count != 0 and time_count < 41:
                curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))
                gold_columns[list_count].append(curr_gold_avg)
                curr_gold_avg = 0
                list_count += 1
        

        #Get the avg for time > 40
        if time_count-(list_count*10) != 0:
            curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))

        #While list_count < 5, append the last avg to the lists
        while list_count < 5:
            if curr_gold_avg != 0:
                gold_columns[list_count].append(curr_gold_avg)
            else:
                gold_columns[list_count].append(gold_columns[list_count-1][-1])
            list_count += 1

    raw_df['rTop_gold_0_9'] = gold_columns[0]
    raw_df['rTop_gold_10_19'] = gold_columns[1]
    raw_df['rTop_gold_20_29'] = gold_columns[2]
    raw_df['rTop_gold_30_39'] = gold_columns[3]
    raw_df['rTop_gold_40'] = gold_columns[4]

    #red jungler
    gold_columns = [[], [], [], [], []]
    
    curr_gold_avg = 0
    for gold_list in raw_df['goldredJungle']:
        time_count = 0
        list_count = 0

        for item in gold_list:
            curr_gold_avg += item
            time_count += 1

            if time_count%10 == 0 and time_count != 0 and time_count < 41:
                curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))
                gold_columns[list_count].append(curr_gold_avg)
                curr_gold_avg = 0
                list_count += 1
        

        #Get the avg for time > 40
        if time_count-(list_count*10) != 0:
            curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))

        #While list_count < 5, append the last avg to the lists
        while list_count < 5:
            if curr_gold_avg != 0:
                gold_columns[list_count].append(curr_gold_avg)
            else:
                gold_columns[list_count].append(gold_columns[list_count-1][-1])
            list_count += 1

    raw_df['rJungle_gold_0_9'] = gold_columns[0]
    raw_df['rJungle_gold_10_19'] = gold_columns[1]
    raw_df['rJungle_gold_20_29'] = gold_columns[2]
    raw_df['rJungle_gold_30_39'] = gold_columns[3]
    raw_df['rJungle_gold_40'] = gold_columns[4]

    #red midlaner
    gold_columns = [[], [], [], [], []]
    
    curr_gold_avg = 0
    for gold_list in raw_df['goldredMiddle']:
        time_count = 0
        list_count = 0

        for item in gold_list:
            curr_gold_avg += item
            time_count += 1

            if time_count%10 == 0 and time_count != 0 and time_count < 41:
                curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))
                gold_columns[list_count].append(curr_gold_avg)
                curr_gold_avg = 0
                list_count += 1
        

        #Get the avg for time > 40
        if time_count-(list_count*10) != 0:
            curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))

        #While list_count < 5, append the last avg to the lists
        while list_count < 5:
            if curr_gold_avg != 0:
                gold_columns[list_count].append(curr_gold_avg)
            else:
                gold_columns[list_count].append(gold_columns[list_count-1][-1])
            list_count += 1

    raw_df['rMid_gold_0_9'] = gold_columns[0]
    raw_df['rMid_gold_10_19'] = gold_columns[1]
    raw_df['rMid_gold_20_29'] = gold_columns[2]
    raw_df['rMid_gold_30_39'] = gold_columns[3]
    raw_df['rMid_gold_40'] = gold_columns[4]

    #red adc
    gold_columns = [[], [], [], [], []]
    
    curr_gold_avg = 0
    for gold_list in raw_df['goldredADC']:
        time_count = 0
        list_count = 0

        for item in gold_list:
            curr_gold_avg += item
            time_count += 1

            if time_count%10 == 0 and time_count != 0 and time_count < 41:
                curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))
                gold_columns[list_count].append(curr_gold_avg)
                curr_gold_avg = 0
                list_count += 1
        

        #Get the avg for time > 40
        if time_count-(list_count*10) != 0:
            curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))

        #While list_count < 5, append the last avg to the lists
        while list_count < 5:
            if curr_gold_avg != 0:
                gold_columns[list_count].append(curr_gold_avg)
            else:
                gold_columns[list_count].append(gold_columns[list_count-1][-1])
            list_count += 1

    raw_df['rADC_gold_0_9'] = gold_columns[0]
    raw_df['rADC_gold_10_19'] = gold_columns[1]
    raw_df['rADC_gold_20_29'] = gold_columns[2]
    raw_df['rADC_gold_30_39'] = gold_columns[3]
    raw_df['rADC_gold_40'] = gold_columns[4]

    #red support
    gold_columns = [[], [], [], [], []]
    
    curr_gold_avg = 0
    for gold_list in raw_df['goldredSupport']:
        time_count = 0
        list_count = 0

        for item in gold_list:
            curr_gold_avg += item
            time_count += 1

            if time_count%10 == 0 and time_count != 0 and time_count < 41:
                curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))
                gold_columns[list_count].append(curr_gold_avg)
                curr_gold_avg = 0
                list_count += 1
        
            

        #Get the avg for time > 40
        if time_count-(list_count*10) != 0:
            curr_gold_avg = curr_gold_avg/(time_count-(list_count*10))

        #While list_count < 5, append the last avg to the lists
        while list_count < 5:
            if curr_gold_avg != 0:
                gold_columns[list_count].append(curr_gold_avg)
            else:
                gold_columns[list_count].append(gold_columns[list_count-1][-1])
            list_count += 1

    raw_df['rSupp_gold_0_9'] = gold_columns[0]
    raw_df['rSupp_gold_10_19'] = gold_columns[1]
    raw_df['rSupp_gold_20_29'] = gold_columns[2]
    raw_df['rSupp_gold_30_39'] = gold_columns[3]
    raw_df['rSupp_gold_40'] = gold_columns[4]

    #Now we delete all rows that are lists
    #golddiff
    del raw_df['golddiff']
    #Blue team champion gold
    del raw_df['goldblueTop']
    del raw_df['goldblueJungle']
    del raw_df['goldblueMiddle']
    del raw_df['goldblueADC']
    del raw_df['goldblueSupport']
    #Red team champion gold
    del raw_df['goldredTop']
    del raw_df['goldredJungle']
    del raw_df['goldredMiddle']
    del raw_df['goldredADC']
    del raw_df['goldredSupport']

    #We'll encode strings as binarys
    lb = preprocessing.LabelBinarizer()

    #Encoding heroes
    blue_heroes_list = np.concatenate([raw_df['blueTopChamp'].unique(), \
        raw_df['blueJungleChamp'].unique(), raw_df['blueMiddleChamp'].unique(), \
            raw_df['blueADCChamp'].unique(), raw_df['blueSupportChamp'].unique()], axis=0)

    red_heroes_list = np.concatenate([raw_df['redTopChamp'].unique(), \
        raw_df['redJungleChamp'].unique(), raw_df['redMiddleChamp'].unique(), \
            raw_df['redADCChamp'].unique(), raw_df['redSupportChamp'].unique()], axis=0)

    heroes_list = np.concatenate([blue_heroes_list, red_heroes_list], axis=0)

    #Fit the encoder for heroes
    lb.fit(heroes_list)

    transformed_b_Top = lb.transform(raw_df['blueTopChamp'].tolist())
    transformed_b_Jungle = lb.transform(raw_df['blueJungleChamp'].tolist())
    transformed_b_Middle = lb.transform(raw_df['blueMiddleChamp'].tolist())
    transformed_b_ADC = lb.transform(raw_df['blueADCChamp'].tolist())
    transformed_b_Support = lb.transform(raw_df['blueSupportChamp'].tolist())

    transformed_r_Top = lb.transform(raw_df['redTopChamp'].tolist())
    transformed_r_Jungle = lb.transform(raw_df['redJungleChamp'].tolist())
    transformed_r_Middle = lb.transform(raw_df['redMiddleChamp'].tolist())
    transformed_r_ADC = lb.transform(raw_df['redADCChamp'].tolist())
    transformed_r_Support = lb.transform(raw_df['redSupportChamp'].tolist())
    
    #Put Top heroes
    heroes_df = pd.DataFrame(transformed_b_Top, columns=lb.classes_)
    
    #Put Jungle heroes
    row_count = 0
    for item in transformed_b_Jungle:
        column_count = 0
        for field in item:
            if field == 1:
                heroes_df[heroes_df.columns[column_count]][row_count] = 1
            column_count += 1
        row_count += 1

    #Put Middle heroes
    row_count = 0
    for item in transformed_b_Middle:
        column_count = 0
        for field in item:
            if field == 1:
                heroes_df[heroes_df.columns[column_count]][row_count] = 1
            column_count += 1
        row_count += 1

    #Put ADC heroes
    row_count = 0
    for item in transformed_b_ADC:
        column_count = 0
        for field in item:
            if field == 1:
                heroes_df[heroes_df.columns[column_count]][row_count] = 1
            column_count += 1
        row_count += 1

    #Put Support heroes
    row_count = 0
    for item in transformed_b_Support:
        column_count = 0
        for field in item:
            if field == 1:
                heroes_df[heroes_df.columns[column_count]][row_count] = 1
            column_count += 1
        row_count += 1

    #Append to raw_df

    raw_df = pd.concat([raw_df, heroes_df], axis=1)

    #Encode players
    blue_players_list = np.concatenate([raw_df['blueTop'].unique(), \
        raw_df['blueJungle'].unique(), raw_df['blueMiddle'].unique(), \
            raw_df['blueADC'].unique(), raw_df['blueSupport'].unique()], axis=0)

    red_players_list = np.concatenate([raw_df['redTop'].unique(), \
        raw_df['redJungle'].unique(), raw_df['redMiddle'].unique(), \
            raw_df['redADC'].unique(), raw_df['redSupport'].unique()], axis=0)

    players_list = np.concatenate([blue_players_list, red_players_list], axis=0)

    #Fit the encoder for players
    lb.fit([str(k) for k in players_list])

    transformed_b_Top = lb.transform(raw_df['blueTop'].tolist())
    transformed_b_Jungle = lb.transform(raw_df['blueJungle'].tolist())
    transformed_b_Middle = lb.transform(raw_df['blueMiddle'].tolist())
    transformed_b_ADC = lb.transform(raw_df['blueADC'].tolist())
    transformed_b_Support = lb.transform(raw_df['blueSupport'].tolist())

    transformed_r_Top = lb.transform(raw_df['redTop'].tolist())
    transformed_r_Jungle = lb.transform(raw_df['redJungle'].tolist())
    transformed_r_Middle = lb.transform(raw_df['redMiddle'].tolist())
    transformed_r_ADC = lb.transform(raw_df['redADC'].tolist())
    transformed_r_Support = lb.transform(raw_df['redSupport'].tolist())
    
    #Put Top players
    players_df = pd.DataFrame(transformed_b_Top, columns=lb.classes_)
    
    #Put Jungle players
    row_count = 0
    for item in transformed_b_Jungle:
        column_count = 0
        for field in item:
            if field == 1:
                players_df[players_df.columns[column_count]][row_count] = 1
            column_count += 1
        row_count += 1

    #Put Middle players
    row_count = 0
    for item in transformed_b_Middle:
        column_count = 0
        for field in item:
            if field == 1:
                players_df[players_df.columns[column_count]][row_count] = 1
            column_count += 1
        row_count += 1

    #Put ADC players
    row_count = 0
    for item in transformed_b_ADC:
        column_count = 0
        for field in item:
            if field == 1:
                players_df[players_df.columns[column_count]][row_count] = 1
            column_count += 1
        row_count += 1

    #Put Support players
    row_count = 0
    for item in transformed_b_Support:
        column_count = 0
        for field in item:
            if field == 1:
                players_df[players_df.columns[column_count]][row_count] = 1
            column_count += 1
        row_count += 1

    raw_df = pd.concat([raw_df, players_df], axis=1)

    #Note that we have two columns: bResult and rResult
    #Change that for a result column: 'blue' if bResult == 1, else 'red'

    result_list = []
    for item in raw_df['bResult']:
        if item == 1:
            result_list.append('blue')
        else:
            result_list.append('red')

    raw_df['result'] = result_list
    
    #Remove bResult and rResult
    del raw_df['bResult']
    del raw_df['rResult']

    raw_df.drop(raw_df.columns[(range(13,33))], axis=1, inplace=True)

    #df is now ready to be used for training and testing

    #We'll use 70% of the dataset to train
    training_df = raw_df.sample(frac=0.7)

    #The rest will be tested
    testing_df = raw_df.drop(index=training_df.index)

    #Extract the classes from training dataset
    training_classes = [item for item in training_df.iloc[:,len(training_df.columns)-1]]

    #Drop class column from training df
    training_df.drop(labels=training_df.columns[len(training_df.columns)-1], axis=1, inplace=True)
    
    #Extract training list values
    training_list = [list(row) for index,row in training_df.iterrows()]

    #Extract classes from testing dataset
    testing_classes = [item for item in testing_df.iloc[:,len(testing_df.columns)-1]]

    #Drop class column for testing df
    testing_df.drop(labels=testing_df.columns[len(testing_df.columns)-1], axis=1, inplace=True)

    #Extract testing values
    testing_list = [list(row) for index,row in testing_df.iterrows()]
    end_time = time.time()

    print(f"Preprocessing Elapsed Time: {(end_time-start_time):.2f}\n")

    #Instantiate the classifiers

    knn = neighbors.KNeighborsClassifier()
    decision_tree = tree.DecisionTreeClassifier()
    sup_vect_mac = svm.SVC()
    mlp = neural_network.MLPClassifier()

    start_time = time.time()
    #KNN
    knn.fit(training_list, training_classes)
    knn_predictions = knn.predict(testing_list)

    #KNN
    knn_confusion_matrix = sklearn.metrics.confusion_matrix(testing_classes, knn_predictions)

    #Accuracy is the sum of the main diagonal divided by the total sum of the confusion matrix 
    accuracy = sum([knn_confusion_matrix[i][j] for i in range(len(knn_confusion_matrix[0]))\
        for j in range(len(knn_confusion_matrix[0])) if i == j])\
            /sum(sum(knn_confusion_matrix))
    end_time = time.time()

    print(f"KNN Elapsed Time:{(end_time-start_time):.2f}")
    print("KNN Accuracy:", accuracy)
    print("KNN Confusion Matrix:\n", knn_confusion_matrix)

    start_time = time.time()
    #Decision tree
    decision_tree.fit(training_list, training_classes)
    decision_tree_predictions = decision_tree.predict(testing_list)

    #Decision Tree
    dec_tree_confusion_matrix = sklearn.metrics.confusion_matrix(testing_classes, decision_tree_predictions)

    #Accuracy is the sum of the main diagonal divided by the total sum of the confusion matrix 
    accuracy = sum([dec_tree_confusion_matrix[i][j] for i in range(len(dec_tree_confusion_matrix[0]))\
        for j in range(len(dec_tree_confusion_matrix[0])) if i == j])\
            /sum(sum(dec_tree_confusion_matrix))
    end_time = time.time()

    print(f"\nDecision Tree Elapsed Time:{(end_time-start_time):.2f}")
    print("Decision Tree Accuracy:", accuracy)
    print("Decision Tree Confusion Matrix:\n", dec_tree_confusion_matrix)

    start_time = time.time()
    #SVM
    sup_vect_mac.fit(training_list, training_classes)
    sup_vect_mac_predictions = sup_vect_mac.predict(testing_list)

    #SVM
    svm_confusion_matrix = sklearn.metrics.confusion_matrix(testing_classes, sup_vect_mac_predictions)

    #Accuracy is the sum of the main diagonal divided by the total sum of the confusion matrix 
    accuracy = sum([svm_confusion_matrix[i][j] for i in range(len(svm_confusion_matrix[0]))\
        for j in range(len(svm_confusion_matrix[0])) if i == j])\
            /sum(sum(svm_confusion_matrix))
    end_time = time.time()

    print(f"\nSVM Elapsed Time:{(end_time-start_time):.2f}")
    print("SVM Accuracy:", accuracy)
    print("SVM Confusion Matrix:\n", svm_confusion_matrix)

    start_time = time.time()
    #MLP
    mlp.fit(training_list, training_classes)
    mlp_predictions = mlp.predict(testing_list)

    #MLP
    mlp_confusion_matrix = sklearn.metrics.confusion_matrix(testing_classes, mlp_predictions)

    #Accuracy is the sum of the main diagonal divided by the total sum of the confusion matrix 
    accuracy = sum([mlp_confusion_matrix[i][j] for i in range(len(mlp_confusion_matrix[0]))\
        for j in range(len(mlp_confusion_matrix[0])) if i == j])\
            /sum(sum(mlp_confusion_matrix))
    end_time = time.time()

    print(f"\nMLP Elapsed Time:{(end_time-start_time):.2f}")
    print("MLP Accuracy:", accuracy)
    print("MLP Confusion Matrix:\n", mlp_confusion_matrix)