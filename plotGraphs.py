import matplotlib.pyplot as plt
from textwrap import wrap
import numpy as np
import plotly as py
from plotly.graph_objs import *
py.tools.set_credentials_file(username='avk1063', api_key='EiZa8XKkkUieEsSpVvAz')

mapbox_access_token = 'pk.eyJ1IjoiYXZrMTA2MyIsImEiOiJjamZuaHVrdG4xYjdtMzNsenRycHBwN3Z0In0.X2_FX0EwshNX3a9OO7816A'


def plotInfo(daysList, businessNameList, flag):
    colorsList = ['blue', 'red', 'green', 'black', 'pink', 'orange', 'brown']
    plt.figure(figsize=(8, 7))
    businessNameList = ['\n'.join(wrap(l, 9)) for l in businessNameList]
    if flag == 'Day':
        daysName = ['Late night', 'Early morning', 'Morning', 'Afternoon', 'Evening', 'Night']
    else:
        daysName = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for index in range(len(daysName)):
        plt.scatter([i for i in range(1, 11)], daysList[index], color=colorsList[index], label=daysName[index])

    plt.xticks([i for i in range(1, 11)], businessNameList, fontsize=8)
    plt.legend(loc='upper center', ncol=3)
    plt.title('Overview of top ten businesses', fontsize=20)
    plt.xlabel('Name of top ten businesses')
    plt.ylabel('Count of check-ins')
    plt.show()


def plotInfoIndividual(daysList, businessNameList, flag):
    fig = plt.figure(figsize=(10, 9))
    colorsList = ['blue', 'red', 'green', 'black', 'pink', 'orange', 'brown']

    if flag == 'Day':
        daysName = ['Late night', 'Early morning', 'Morning', 'Afternoon', 'Evening', 'Night']
    else:
        daysName = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for index in range(len(daysName)):
        ax = fig.add_subplot(2, 4, index + 1)
        ax.scatter([i for i in range(1, 11)], daysList[index], color=colorsList[index], label=daysName[index])
        if index == 3:
            plt.xticks([i for i in range(1, 11)], businessNameList, rotation=90, fontsize=8)
        else:
            plt.xticks([i for i in range(1, 11)])
        plt.legend(loc='upper center')

    fig.text(0.5, 0.04, 'Name of top ten businesses', ha='center', va='center', fontsize=15)
    fig.text(0.06, 0.5, 'Count of check-ins', ha='center', va='center', rotation='vertical', fontsize=15)
    plt.suptitle('Check-in count for top ten businesses', fontsize=20)
    plt.show()


def plotting(timeInfo, flag):
    """
    Plots the total count of check-ins during an entire day
    :param timeInfo: the list of lists containing count for each day for a particular business
    :param flag: a flag to check whether the list contains check-ins for the day or the week
    :return: None
    """
    first, sec, third, fourth, fifth, sixth, seventh = 0, 0, 0, 0, 0, 0, 0
    colorsList = ['blue', 'red', 'green', 'yellow', 'black', 'pink', 'orange']
    plt.figure(figsize=(8, 7))

    if flag == 'Week':
        store = [first, sec, third, fourth, fifth, sixth, seventh]
        name = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        plt.xlabel('Days of the week')
        plt.title('Count of check-ins during the week')

    else:
        store = [first, sec, third, fourth, fifth, sixth]
        name = ('Late night', 'Early morning', 'Morning', 'Afternoon', 'Evening', 'Night')
        plt.xlabel('Time ranges during the day')
        plt.title('Count of check-ins during the day')

    for day in timeInfo:
        for idx in range(1, len(store) + 1):
            store[idx - 1] += int(day[idx])

    objects = np.arange(len(name))
    barList = plt.bar(name, store, alpha=0.5)
    for index in range(len(barList)):
        barList[index].set_color(colorsList[index])

    plt.xticks(objects, name, rotation=15)
    plt.ylabel('Total count of check-ins')
    plt.show()


def plotOnMap(lat, long, text):
    data = Data([Scattermapbox(lat=lat, lon=long, mode='markers', text=text)])
    layout = Layout(autosize=True, hovermode='closest', mapbox=dict(accesstoken=mapbox_access_token, bearing=0))
    fig = dict(data=data, layout=layout)
    py.offline.plot(fig, filename='Yelp analysis.html')
