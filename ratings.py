import json
import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class yelping(object):
    def __init__(self, file):
        self.file = file

    def readcheckInfile(self):
        temp_list = []
        pp = pprint.PrettyPrinter(indent=4)
        newDict = {}
        tempDict = {'Business ID': 0, 'Users': 0}
        columns = ['Business id', 'Users']
        idlist = list()
        id = list()
        userRate = list()
        combos = {}
        count = 0
        with open(self.file, encoding='utf8') as f:
            for line in f:
                json_data = json.loads(line,encoding='utf-8')
                if json_data['business_id'] in combos:
                    combos[json_data['business_id']] += 1
                else:
                    combos[json_data['business_id']] = 1

        index = [i for i in range(len(newDict))]
        valuesD = combos.values()
        keysD = combos.keys()
        print(len(keysD))
        print(len(valuesD))
        new_data = np.array([keysD, valuesD]).transpose()
        df = pd.DataFrame(data=new_data, index=index, columns=columns)
        df[['Users']] \
            = df[['Users']].apply(pd.to_numeric)
        print(df)
        df.to_csv('UserRating.csv', index=False)


def main():
    file_checkIn = "dataset/tip.json"
    file_csv = "UserRating.csv"

    yelp = yelping(file_checkIn)
    yelp.readcheckInfile()

    #yelp = yelping(file_csv)
    # yelp.readcsvCheckin()


if __name__ == '__main__':
    main()