import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

from ast import literal_eval

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

#Function radar_factory available at: https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html
def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

if __name__ == "__main__":
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
    
    del raw_df['blueBans']
    del raw_df['redBans']

    # print(raw_df.columns)

    #Some columns are not really lists, they are strings that look like lists
    #So we should convert them to actual lists
    raw_df['golddiff'] = raw_df['golddiff'].apply(literal_eval)
    raw_df['goldblue'] = raw_df['goldblue'].apply(literal_eval)
    raw_df['goldred'] = raw_df['goldred'].apply(literal_eval)

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

    #Let's print a scatter from the gold to see the relation between gold and win

    #Note that we have two columns: bResult and rResult
    #Change that for a result column: 'blue' if bResult == 1, else 'red'
    #Let's also count the wins so we can plot a pie chart just for fun

    result_list = []
    red_wins = 0
    blue_wins = 0
    for item in raw_df['bResult']:
        if item == 1:
            result_list.append('blue')
            blue_wins += 1
        else:
            result_list.append('red')
            red_wins += 1

    raw_df['result'] = result_list

    plt.pie([blue_wins/(red_wins+blue_wins), red_wins/(red_wins+blue_wins)], labels=['Blue', 'Red'], colors=['blue','red'],\
        shadow=True, autopct='%1.1f%%')
    
    plt.savefig("IMAGES/"+"wins-pie.png")
    
    #Then let's get gold and time columns
    game_time = 0
    game = 0
    gold_time = []
    for game_gold in raw_df['golddiff']:
        gold_time.append([[game_gold[game_time], game_time, raw_df['result'][game]] for game_time in range(len(game_gold))])
        game += 1

    #Flatten the list
    flat_gold_time = []
    for k in range(len(gold_time)):
        for i in gold_time[k]:
            flat_gold_time.append(i)

    #Plot the scatter and save it
    plt.scatter([k[1] for k in flat_gold_time], [k[0] for k in flat_gold_time], \
        c=[k[2] for k in flat_gold_time])

    plt.savefig("IMAGES/"+"gold-x-time-scatter.png")

    #Let's do the same for championgold so that we see how gold on each role impacts the game

    #Let's get gold and time columns
    #It's better if we get golddiff for each role, so we'll use raw_df['goldblueXXX'][X]-raw_df['goldredXXX'][X]

    #Toplaner
    game_time_Top = 0
    game_Top = 0
    gold_time_Top = []
    for game_gold_position in range(len(raw_df['goldblueTop'])):
        gold_time_Top.append([[(raw_df['goldblueTop'][game_Top][game_time_Top]-raw_df['goldredTop'][game_Top][game_time_Top]),\
             game_time_Top, raw_df['result'][game_Top]] for game_time_Top in range(len(raw_df['goldblueTop'][game_Top]))])
        game_Top += 1

    #Flatten the list
    flat_gold_time_Top = []
    for k in range(len(gold_time_Top)):
        for i in gold_time_Top[k]:
            flat_gold_time_Top.append(i)

    plt.clf()

    #Plot the scatter and save it
    plt.scatter([k[1] for k in flat_gold_time_Top], [k[0] for k in flat_gold_time_Top], \
        c=[k[2] for k in flat_gold_time_Top])

    plt.savefig("IMAGES/"+"gold-x-time-Top-scatter.png")

    #Jungler
    game_time_Jungle = 0
    game_Jungle = 0
    gold_time_Jungle = []
    for game_gold_position in range(len(raw_df['goldblueJungle'])):
        gold_time_Jungle.append([[(raw_df['goldblueJungle'][game_Jungle][game_time_Jungle]-raw_df['goldredJungle'][game_Jungle][game_time_Jungle]),\
             game_time_Jungle, raw_df['result'][game_Jungle]] for game_time_Jungle in range(len(raw_df['goldblueJungle'][game_Jungle]))])
        game_Jungle += 1

    #Flatten the list
    flat_gold_time_Jungle = []
    for k in range(len(gold_time_Jungle)):
        for i in gold_time_Jungle[k]:
            flat_gold_time_Jungle.append(i)

    plt.clf()

    #Plot the scatter and save it
    plt.scatter([k[1] for k in flat_gold_time_Jungle], [k[0] for k in flat_gold_time_Jungle], \
        c=[k[2] for k in flat_gold_time_Jungle])

    plt.savefig("IMAGES/"+"gold-x-time-Jungle-scatter.png")

    #Mid laner
    game_time_Middle = 0
    game_Middle = 0
    gold_time_Middle = []
    for game_gold_position in range(len(raw_df['goldblueMiddle'])):
        gold_time_Middle.append([[(raw_df['goldblueMiddle'][game_Middle][game_time_Middle]-raw_df['goldredMiddle'][game_Middle][game_time_Middle]),\
             game_time_Middle, raw_df['result'][game_Middle]] for game_time_Middle in range(len(raw_df['goldblueMiddle'][game_Middle]))])
        game_Middle += 1

    #Flatten the list
    flat_gold_time_Middle = []
    for k in range(len(gold_time_Middle)):
        for i in gold_time_Middle[k]:
            flat_gold_time_Middle.append(i)

    plt.clf()

    #Plot the scatter and save it
    plt.scatter([k[1] for k in flat_gold_time_Middle], [k[0] for k in flat_gold_time_Middle], \
        c=[k[2] for k in flat_gold_time_Middle])

    plt.savefig("IMAGES/"+"gold-x-time-Middle-scatter.png")

    #ADC
    game_time_ADC = 0
    game_ADC = 0
    gold_time_ADC = []
    for game_gold_position in range(len(raw_df['goldblueADC'])):
        gold_time_ADC.append([[(raw_df['goldblueADC'][game_ADC][game_time_ADC]-raw_df['goldredADC'][game_ADC][game_time_ADC]),\
             game_time_ADC, raw_df['result'][game_ADC]] for game_time_ADC in range(len(raw_df['goldblueADC'][game_ADC]))])
        game_ADC += 1

    #Flatten the list
    flat_gold_time_ADC = []
    for k in range(len(gold_time_ADC)):
        for i in gold_time_ADC[k]:
            flat_gold_time_ADC.append(i)

    plt.clf()

    #Plot the scatter and save it
    plt.scatter([k[1] for k in flat_gold_time_ADC], [k[0] for k in flat_gold_time_ADC], \
        c=[k[2] for k in flat_gold_time_ADC])

    plt.savefig("IMAGES/"+"gold-x-time-ADC-scatter.png")

    #Support
    game_time_Support = 0
    game_Support = 0
    gold_time_Support = []
    for game_gold_position in range(len(raw_df['goldblueSupport'])):
        gold_time_Support.append([[(raw_df['goldblueSupport'][game_Support][game_time_Support]-raw_df['goldredSupport'][game_Support][game_time_Support]),\
             game_time_Support, raw_df['result'][game_Support]] for game_time_Support in range(len(raw_df['goldblueSupport'][game_Support]))])
        game_Support += 1

    #Flatten the list
    flat_gold_time_Support = []
    for k in range(len(gold_time_Support)):
        for i in gold_time_Support[k]:
            flat_gold_time_Support.append(i)

    plt.clf()

    #Plot the scatter and save it
    plt.scatter([k[1] for k in flat_gold_time_Support], [k[0] for k in flat_gold_time_Support], \
        c=[k[2] for k in flat_gold_time_Support])

    plt.savefig("IMAGES/"+"gold-x-time-Support-scatter.png")

    #Wanna see if the gold distribution among roles influences the wins, so let's plot a radar chart for that
    
    #For each role get the gold that the champion ended the match
    
    #Top
    blue_Top_gold_win = 0
    blue_Top_gold_lose = 0
    red_Top_gold_win = 0
    red_Top_gold_lose = 0
    blue_win_count = 0

    for gold_list in range(len(raw_df['goldblueTop'])):
        #If blue team won
        if raw_df['result'][gold_list] == 'blue':
            #Get the last gold reg
            blue_Top_gold_win += raw_df['goldblueTop'][gold_list][-1]
            red_Top_gold_lose += raw_df['goldredTop'][gold_list][-1]
            blue_win_count += 1
        else:
            blue_Top_gold_lose += raw_df['goldblueTop'][gold_list][-1]
            red_Top_gold_win += raw_df['goldredTop'][gold_list][-1]

    #Get the avg
    blue_Top_gold_win = blue_Top_gold_win/blue_win_count
    blue_Top_gold_lose = blue_Top_gold_lose/(len(raw_df['goldblueTop'])-blue_win_count)
    red_Top_gold_win = red_Top_gold_win/(len(raw_df['goldblueTop'])-blue_win_count)
    red_Top_gold_lose = red_Top_gold_lose/blue_win_count

    #Jungle
    blue_Jungle_gold_win = 0
    blue_Jungle_gold_lose = 0
    red_Jungle_gold_win = 0
    red_Jungle_gold_lose = 0
    blue_win_count = 0
    
    for gold_list in range(len(raw_df['goldblueJungle'])):
        #If blue team won
        if raw_df['result'][gold_list] == 'blue':
            #Get the last gold reg
            blue_Jungle_gold_win += raw_df['goldblueJungle'][gold_list][-1]
            red_Jungle_gold_lose += raw_df['goldredJungle'][gold_list][-1]
            blue_win_count += 1
        else:
            blue_Jungle_gold_lose += raw_df['goldblueJungle'][gold_list][-1]
            red_Jungle_gold_win += raw_df['goldredJungle'][gold_list][-1]

    #Get the avg
    blue_Jungle_gold_win = blue_Jungle_gold_win/blue_win_count
    blue_Jungle_gold_lose = blue_Jungle_gold_lose/(len(raw_df['goldblueTop'])-blue_win_count)
    red_Jungle_gold_win = red_Jungle_gold_win/(len(raw_df['goldblueTop'])-blue_win_count)
    red_Jungle_gold_lose = red_Jungle_gold_lose/blue_win_count

    #Middle
    blue_Middle_gold_win = 0
    blue_Middle_gold_lose = 0
    red_Middle_gold_win = 0
    red_Middle_gold_lose = 0
    blue_win_count = 0

    for gold_list in range(len(raw_df['goldblueMiddle'])):
        #If blue team won
        if raw_df['result'][gold_list] == 'blue':
            #Get the last gold reg
            blue_Middle_gold_win += raw_df['goldblueMiddle'][gold_list][-1]
            red_Middle_gold_lose += raw_df['goldredMiddle'][gold_list][-1]
            blue_win_count += 1

        else:
            blue_Middle_gold_lose += raw_df['goldblueMiddle'][gold_list][-1]
            red_Middle_gold_win += raw_df['goldredMiddle'][gold_list][-1]

    #Get the avg
    blue_Middle_gold_win = blue_Middle_gold_win/blue_win_count
    blue_Middle_gold_lose = blue_Middle_gold_lose/(len(raw_df['goldblueTop'])-blue_win_count)
    red_Middle_gold_win = red_Middle_gold_win/(len(raw_df['goldblueTop'])-blue_win_count)
    red_Middle_gold_lose = red_Middle_gold_lose/blue_win_count

    #ADC
    blue_ADC_gold_win = 0
    blue_ADC_gold_lose = 0
    red_ADC_gold_win = 0
    red_ADC_gold_lose = 0
    blue_win_count = 0

    for gold_list in range(len(raw_df['goldblueADC'])):
        #If blue team won
        if raw_df['result'][gold_list] == 'blue':
            #Get the last gold reg
            blue_ADC_gold_win += raw_df['goldblueADC'][gold_list][-1]
            red_ADC_gold_lose += raw_df['goldredADC'][gold_list][-1]
            blue_win_count += 1

        else:
            blue_ADC_gold_lose += raw_df['goldblueADC'][gold_list][-1]
            red_ADC_gold_win += raw_df['goldredADC'][gold_list][-1]

    #Get the avg
    blue_ADC_gold_win = blue_ADC_gold_win/blue_win_count
    blue_ADC_gold_lose = blue_ADC_gold_lose/(len(raw_df['goldblueTop'])-blue_win_count)
    red_ADC_gold_win = red_ADC_gold_win/(len(raw_df['goldblueTop'])-blue_win_count)
    red_ADC_gold_lose = red_ADC_gold_lose/blue_win_count

    #Support
    blue_Support_gold_win = 0
    blue_Support_gold_lose = 0
    red_Support_gold_win = 0
    red_Support_gold_lose = 0
    blue_win_count = 0

    for gold_list in range(len(raw_df['goldblueSupport'])):
        #If blue team won
        if raw_df['result'][gold_list] == 'blue':
            #Get the last gold reg
            blue_Support_gold_win += raw_df['goldblueSupport'][gold_list][-1]
            red_Support_gold_lose += raw_df['goldredSupport'][gold_list][-1]
            blue_win_count += 1

        else:
            blue_Support_gold_lose += raw_df['goldblueSupport'][gold_list][-1]
            red_Support_gold_win += raw_df['goldredSupport'][gold_list][-1]

    #Get the avg
    blue_Support_gold_win = blue_Support_gold_win/blue_win_count
    blue_Support_gold_lose = blue_Support_gold_lose/(len(raw_df['goldblueTop'])-blue_win_count)
    red_Support_gold_win = red_Support_gold_win/(len(raw_df['goldblueTop'])-blue_win_count)
    red_Support_gold_lose = red_Support_gold_lose/blue_win_count

    #Now get the % of the team gold that each role's gold represents
    blue_total_gold_win = blue_Top_gold_win + blue_Jungle_gold_win + blue_Middle_gold_win + blue_ADC_gold_win + blue_Support_gold_win
    blue_total_gold_lose = blue_Top_gold_lose + blue_Jungle_gold_lose + blue_Middle_gold_lose + blue_ADC_gold_lose + blue_Support_gold_lose

    red_total_gold_win = red_Top_gold_win + red_Jungle_gold_win + red_Middle_gold_win + red_ADC_gold_win + red_Support_gold_win
    red_total_gold_lose = red_Top_gold_lose + red_Jungle_gold_lose + red_Middle_gold_lose + red_ADC_gold_lose + red_Support_gold_lose
   
    #blue win %
    blue_Top_gold_win_pct = blue_Top_gold_win/blue_total_gold_win
    blue_Jungle_gold_win_pct = blue_Jungle_gold_win/blue_total_gold_win
    blue_Middle_gold_win_pct = blue_Middle_gold_win/blue_total_gold_win
    blue_ADC_gold_win_pct = blue_ADC_gold_win/blue_total_gold_win
    blue_Support_gold_win_pct = blue_Support_gold_win/blue_total_gold_win

    #blue lose %
    blue_Top_gold_lose_pct = blue_Top_gold_lose/blue_total_gold_lose
    blue_Jungle_gold_lose_pct = blue_Jungle_gold_lose/blue_total_gold_lose
    blue_Middle_gold_lose_pct = blue_Middle_gold_lose/blue_total_gold_lose
    blue_ADC_gold_lose_pct = blue_ADC_gold_lose/blue_total_gold_lose
    blue_Support_gold_lose_pct = blue_Support_gold_lose/blue_total_gold_lose

    #red win %
    red_Top_gold_win_pct = red_Top_gold_win/red_total_gold_win
    red_Jungle_gold_win_pct = red_Jungle_gold_win/red_total_gold_win
    red_Middle_gold_win_pct = red_Middle_gold_win/red_total_gold_win
    red_ADC_gold_win_pct = red_ADC_gold_win/red_total_gold_win
    red_Support_gold_win_pct = red_Support_gold_win/red_total_gold_win

    #red lose %
    red_Top_gold_lose_pct = red_Top_gold_lose/red_total_gold_lose
    red_Jungle_gold_lose_pct = red_Jungle_gold_lose/red_total_gold_lose
    red_Middle_gold_lose_pct = red_Middle_gold_lose/red_total_gold_lose
    red_ADC_gold_lose_pct = red_ADC_gold_lose/red_total_gold_lose
    red_Support_gold_lose_pct = red_Support_gold_lose/red_total_gold_lose

    #Now plot
    data = [('Blue Team Gold Div', [[blue_Top_gold_win_pct, blue_Jungle_gold_win_pct, blue_Middle_gold_win_pct, blue_ADC_gold_win_pct, blue_Support_gold_win_pct],\
        [blue_Top_gold_lose_pct, blue_Jungle_gold_lose_pct, blue_Middle_gold_lose_pct, blue_ADC_gold_lose_pct, blue_Support_gold_lose_pct]]),\
            ('Red Team Gold Div', [[red_Top_gold_win_pct, red_Jungle_gold_win_pct, red_Middle_gold_win_pct, red_ADC_gold_win_pct, red_Support_gold_win_pct],\
        [red_Top_gold_lose_pct, red_Jungle_gold_lose_pct, red_Middle_gold_lose_pct, red_ADC_gold_lose_pct, red_Support_gold_lose_pct]])]
    
    N = 5
    theta = radar_factory(N, frame='polygon')

    fig, axs = plt.subplots(figsize=(9, 9), nrows=1, ncols=2,
                            subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ['g', 'r']

    for ax, (title, case_data) in zip(axs.flat, data):
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        for d, color in zip(case_data, colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_varlabels(['Top', 'Jungle', 'Middle', 'ADC', 'Support'])
    
    labels = ('Win', 'Lose')
    legend = axs[0].legend(labels, loc=(0.9, .95),
                              labelspacing=0.1, fontsize='small')
    
    plt.savefig("IMAGES/"+"gold-div-radar-pct.png")

    #Let's also plot without the pct, just for show
    data = [('Blue Team Gold Div', [[blue_Top_gold_win, blue_Jungle_gold_win, blue_Middle_gold_win, blue_ADC_gold_win, blue_Support_gold_win],\
        [blue_Top_gold_lose, blue_Jungle_gold_lose, blue_Middle_gold_lose, blue_ADC_gold_lose, blue_Support_gold_lose]]),\
            ('Red Team Gold Div', [[red_Top_gold_win, red_Jungle_gold_win, red_Middle_gold_win, red_ADC_gold_win, red_Support_gold_win],\
        [red_Top_gold_lose, red_Jungle_gold_lose, red_Middle_gold_lose, red_ADC_gold_lose, red_Support_gold_lose]])]

    print(data)

    N = 5
    theta = radar_factory(N, frame='polygon')

    fig, axs = plt.subplots(figsize=(9, 9), nrows=1, ncols=2,
                            subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ['g', 'r']

    for ax, (title, case_data) in zip(axs.flat, data):
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        for d, color in zip(case_data, colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_varlabels(['Top', 'Jungle', 'Middle', 'ADC', 'Support'])
    
    labels = ('Win', 'Lose')
    legend = axs[0].legend(labels, loc=(0.9, .95),
                              labelspacing=0.1, fontsize='small')
    
    plt.savefig("IMAGES/"+"gold-div-radar.png")


