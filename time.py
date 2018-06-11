import json
import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class TIME(object):
    def __init__(self, file):
        self.file = file

    def readcheckInfile(self):
        temp_list = []
        pp = pprint.PrettyPrinter(indent=4)
        newDict = {}
        tempDict = {'4': 0, '8': 0, '12': 0, '16': 0, '20': 0, '24': 0}
        idlist = list()
        first, sec, third, fourth, fifth, sixth = [], [], [], [], [], []
        count = 0
        with open(self.file) as f:
            for line in f:
                json_data = json.loads(line)
                idlist.append(json_data['business_id'])
                for val in json_data['time']:
                    for key,values in json_data['time'][val].items():
                        key = int(key.split(":")[0])
                        if key<=4:
                            tempDict['4'] +=values
                        if 8 >= key > 4:
                            tempDict['8'] += values
                        if 12 >= key > 8:
                            tempDict['12'] += values
                        if 16 >= key > 12:
                            tempDict['16'] += values
                        if 20 >= key > 16:
                            tempDict['20'] += values
                        if 24 >= key > 20:
                            tempDict['24'] += values

                newDict[json_data['business_id']] = tempDict
                #print(tempDict)
                if sum(tempDict.values()) <=5:
                    count +=1

                tempDict = {'4': 0, '8': 0,'12': 0,'16': 0,'20': 0,'24': 0}

        columns = ['BusinessId','0-4', '4-8', '8-12', '12-16', '16-20', '20-24']

        index = [i for i in range(len(newDict))]
        for val in idlist:
            temp = newDict[val]

            temp_list = temp.keys()

            if '4' in temp_list:
                first.append(int(temp['4']))
            else:
                first.append(0)

            if '8' in temp_list:
                sec.append(int(temp['8']))
            else:
                sec.append(0)

            if '12' in temp_list:
                third.append(int(temp['12']))
            else:
                third.append(0)

            if '16' in temp_list:
                fourth.append(int(temp['16']))
            else:
                fourth.append(0)

            if '20' in temp_list:
                fifth.append(int(temp['20']))
            else:
                fifth.append(0)

            if '24' in temp_list:
                sixth.append(int(temp['24']))
            else:
                sixth.append(0)

        new_data = np.array([idlist, first,sec,third,fourth,fifth,sixth]).transpose()
        df = pd.DataFrame(data=new_data, index=index, columns=columns)
        correctName = []
        for index in range(1, 146351):
            correctName.append('Business' + str(index))
        df['BusinessId'] = correctName
        df[['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']] \
            = df[['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']].apply(pd.to_numeric)
        df.to_csv('time.csv', index=False)


def plotting(file):
    file = open(file, 'r').readlines()
    day = []
    for line in file:
        lines = line.strip().split(',')
        day.append(lines)
    day.pop(0)

    first, sec, third, fourth, fifth, sixth  = 0, 0, 0, 0, 0, 0
    for time in day:
        first += int(time[1])
        sec += int(time[2])
        third += int(time[3])
        fourth += int(time[4])
        fifth += int(time[5])
        sixth += int(time[6])

    store = [first, sec, third, fourth, fifth, sixth]
    name = ('first', 'second', 'third', 'fourth', 'fifth', 'sixth')
    objects = np.arange(len(name))

    plt.bar(name, store, alpha=0.5)
    plt.xticks(objects, name, rotation=45)
    plt.ylabel('Total count of checkins')
    plt.title('Count of checkins during the day')
    plt.show()


def main():
    file_checkIn = "dataset/checkin.json"
    file_csv = "time.csv"

    yelp1 = TIME(file_checkIn)
    yelp1.readcheckInfile()

    plotting(file_csv)

if __name__ == '__main__':
    main()