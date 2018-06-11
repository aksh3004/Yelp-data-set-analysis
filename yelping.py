import json
import operator
import plotGraphs
import numpy as np
import pandas as pd


class Yelping(object):
    def __init__(self, file):
        self.file = file

    def extractBusinessNames(self):
        """
        From the given JSON file, extract the names of the businesses
        :return: the dictionary of business names
        """
        businessName = {}
        with open(self.file, encoding='utf8') as f:
            for line in f:
                json_data = json.loads(line)
                businessName[json_data['business_id']] = json_data['name']

        return businessName

    def readCheckinFileDays(self, businessName):
        """
        Reads the Check-in file in JSON format and creates the corresponding file in CSV file
        :param businessName: the dictionary containing the business names
        :return: None
        """
        newDict = {}
        idList = []
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = [], [], [], [], [], [], []
        columns = ['BusinessId', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        with open(self.file, encoding='utf8') as f:
            for line in f:
                tempDict = {}
                json_data = json.loads(line)
                idList.append(businessName.get(json_data['business_id']).replace(",", "-"))

                for val in json_data['time']:
                    tempDict[val] = sum(json_data['time'][val].values())

                newDict[businessName.get(json_data['business_id']).replace(",", "-")] = tempDict

        indexList = [i for i in range(len(idList))]
        for val in idList:
            temp = newDict[val]
            temp_list = temp.keys()
            if 'Monday' in temp_list:
                monday.append(int(temp['Monday']))
            else:
                monday.append(0)

            if 'Tuesday' in temp_list:
                tuesday.append(int(temp['Tuesday']))
            else:
                tuesday.append(0)

            if 'Wednesday' in temp_list:
                wednesday.append(int(temp['Wednesday']))
            else:
                wednesday.append(0)

            if 'Thursday' in temp_list:
                thursday.append(int(temp['Thursday']))
            else:
                thursday.append(0)

            if 'Friday' in temp_list:
                friday.append(int(temp['Friday']))
            else:
                friday.append(0)

            if 'Saturday' in temp_list:
                saturday.append(int(temp['Saturday']))
            else:
                saturday.append(0)

            if 'Sunday' in temp_list:
                sunday.append(int(temp['Sunday']))
            else:
                sunday.append(0)

        new_data = np.array([idList, monday, tuesday, wednesday, thursday, friday, saturday, sunday]).transpose()
        df = pd.DataFrame(data=new_data, index=indexList, columns=columns)
        df[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']] \
            = df[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']].apply(pd.to_numeric)
        df.to_csv('checkins.csv', index=False)

    def readCheckinFileTime(self, businessName):
        """
        Reads the Time file in JSON format and creates the corresponding file in CSV file
        :param businessName: the dictionary containing business names
        :return: None
        """
        newDict = {}
        idList = []
        first, sec, third, fourth, fifth, sixth = [], [], [], [], [], []
        columns = ['BusinessId', '0-4', '4-8', '8-12', '12-16', '16-20', '20-24']

        with open(self.file) as f:
            for line in f:
                tempDict = {'4': 0, '8': 0, '12': 0, '16': 0, '20': 0, '24': 0}
                json_data = json.loads(line)
                idList.append(businessName.get(json_data['business_id']).replace(",", "-"))

                for val in json_data['time']:
                    for key, values in json_data['time'][val].items():
                        key = int(key.split(":")[0])
                        if key <= 4:
                            tempDict['4'] += values
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

                newDict[businessName.get(json_data['business_id']).replace(",", "-")] = tempDict

        indexList = [i for i in range(len(idList))]
        for val in idList:
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

        new_data = np.array([idList, first, sec, third, fourth, fifth, sixth]).transpose()
        df = pd.DataFrame(data=new_data, index=indexList, columns=columns)
        df[['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']] \
            = df[['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']].apply(pd.to_numeric)
        df.to_csv('time.csv', index=False)

    def readBusinessRatings(self, businessName):
        """
        Reads the Time file in JSON format and creates the corresponding file in CSV file
        :param businessName: the dictionary containing business names
        :return: None
        """
        combos = {}
        businessList, usersList = [], []

        with open(self.file, encoding='utf8') as f:
            for line in f:
                json_data = json.loads(line)
                if (businessName.get(json_data['business_id']).replace(",", "-")) in combos:
                    combos[businessName.get(json_data['business_id'])] += 1
                else:
                    combos[businessName.get(json_data['business_id'])] = 1

        columns = ['business', 'users']
        for key, value in combos.items():
            businessList.append(key)
            usersList.append(value)

        new_data = np.array([businessList, usersList]).transpose()
        df = pd.DataFrame(data=new_data, index=[i for i in range(len(combos))], columns=columns)
        df[['users']] = df[['users']].apply(pd.to_numeric)
        df.to_csv('ratings.csv', index=False)

    def extractBusinessInfo(self, businessName):
        columns = ['Name', 'City', 'State', 'Business type', 'Latitude', 'Longitude']
        categories = {}
        name, city, state, businessType, latitude, longitude = [], [], [], [], [], []
        removeBusiness = []
        mainCategories = []

        # MAKING LIST FOR CATEGORY -
        with open(self.file) as f:
            for line in f:
                json_data = json.loads(line)
                listOfCategories = json_data['categories']
                if json_data['categories'] != [] and json_data['state'] != '' and json_data['city'] != '' and json_data[
                    'name'] != '' and json_data['business_id'] != '' and json_data['latitude'] != '' and json_data[
                        'longitude'] != '':

                    for record in listOfCategories:
                        if record in categories.keys():
                            categories[record] += 1
                        else:
                            categories[record] = 1

        sortedDict = sorted((value, key) for (key, value) in categories.items())
        for key, val in sortedDict:
            if key > 1000:
                mainCategories.append(val)

        listToRemove = ['French', 'Greek', 'Pizza', 'American (Traditional)', 'Coffee & Tea', 'Fast Food', 'Sandwiches',
                        'Fashion', 'Nightlife', 'Food', 'Middle Eastern', 'Thai', 'Indian', 'Mobile Phones',
                        'Veterinarians', 'Books', 'Mags', 'Music & Video', 'Electronics', 'Canadian (New)',
                        'Arts & Crafts', 'Barbeque', 'Jewelry', "Men's Clothing", 'Mediterranean', 'Asian Fusion',
                        'Beer', 'Wine & Spirits', 'Waxing', 'Accessories', 'Tires', 'Flowers & Gifts', 'Salad',
                        'Seafood', 'Chicken Wings', 'Japanese', 'Ice Cream & Frozen Yogurt', "Women's Clothing",
                        'Desserts', 'Education', 'Skin Care', 'Breakfast & Brunch', 'American (New)', 'Chinese',
                        'Mexican', 'Burgers', 'Italian', 'Active Life', 'Sporting Goods', 'Home & Garden',
                        'Specialty Food', 'Grocery', 'Massage', 'Trainers', 'Yoga', 'Makeup Artists', 'Home Cleaning',
                        'Dry Cleaning & Laundry', 'Pets', 'Pet Sitting', 'Hair Removal', 'Pet Groomers', 'Delis',
                        'Cosmetic Dentists', 'Caterers', 'Contractors', 'Pet Stores', 'Doctors', 'Chiropractors',
                        'Steakhouses', 'Lounges', 'Optometrists', 'Heating & Air Conditioning/HVAC', 'Massage Therapy',
                        'Hair Stylists', 'General Dentistry', 'Dentists', 'IT Services & Computer Repair',
                        'Auto Repair', 'Gyms', 'Barbers', 'Car Dealers', 'Auto Parts & Supplies', 'Home Decor',
                        'Party & Event Planning', 'Plumbing', 'Real Estate Agents', 'Eyelash Service',
                        'Hair Salons', 'Oil Change Stations', 'Cocktail Bars', 'Wine Bars', 'Sports Bars', 'Bars',
                        'Gas Stations', 'Shoe Stores', 'Diners', 'Medical Centers', 'Department Stores', 'Drugstores',
                        'Furniture Stores', 'Venues & Event Spaces', 'Cosmetics & Beauty Supply', 'Cafes',
                        'Nail Salons', 'Hotels & Travel', 'Sushi Bars', 'Body Shops', 'Apartments', 'Pubs']
        for idx in listToRemove:
            mainCategories.remove(idx)

        # MAKING LIST OF ALL THE BUSINESSES -
        with open(self.file) as f:
            for line in f:
                json_data = json.loads(line)
                listOfCategories = json_data['categories']
                for idx in listOfCategories:
                    if idx in mainCategories:
                        categoryOfBusiness = idx
                        break

                if categoryOfBusiness != '' and json_data['state'] != '' and json_data['city'] != '' and json_data[
                    'name'] != '' and json_data['business_id'] != '' and json_data['latitude'] != '' and json_data[
                        'longitude'] != '':
                    name.append(json_data['name'].replace(",", "-"))
                    city.append(json_data['city'])
                    state.append(json_data['state'])
                    businessType.append(categoryOfBusiness)
                    latitude.append(json_data['latitude'])
                    longitude.append(json_data['longitude'])

                else:
                    removeBusiness.append(businessName.get(json_data['business_id']).replace(",", "-"))

        new_data = np.array([name, city, state, businessType, latitude, longitude]).transpose()
        df = pd.DataFrame(data=new_data, columns=columns)
        df.to_csv('businessDescriptn.csv', index=False)


def readCSV(file):
    """
    Reads in a csv file and returns a list of lists
    :param file: the csv file to be read
    :return: a list of lists
    """
    file = open(file, 'r', encoding='utf8').readlines()
    listOfLists = []
    for line in file:
        lines = line.strip().split(',')
        listOfLists.append(lines)
    listOfLists.pop(0)
    return listOfLists


def busiestBusiness(listOfLists, flag):
    """
    Count the total check-ins for a business and extract the ten businesses with most check-ins
    :param listOfLists: the list of lists containing counts for a particular business
    :param flag: a flag to check whether the list contains check-ins for the day or the week
    :return: the ten businesses with the most check-ins
    """
    countList = {}
    for business in listOfLists:
        if flag == 'Week':
            totalCount = int(business[1]) + int(business[2]) + int(business[3]) + int(business[4]) + int(
                business[5]) + int(business[6]) + int(business[7])
        else:
            totalCount = int(business[1]) + int(business[2]) + int(business[3]) + int(business[4]) + int(
                business[5]) + int(business[6])

        if business[0] not in countList:
            countList[business[0]] = totalCount

    sortedCountList = sorted(countList.items(), key=operator.itemgetter(1))
    return sortedCountList


def findTopTen(sortedCountList, mainList):
    """
    For the top ten businesses, find the count of check-ins from the original list
    :param sortedCountList: the sorted list of all businesses
    :param mainList: the original list of all businesses
    :return: the list of the businesses with their check-ins
    """
    topTen = sortedCountList[-10:]
    finalTopTen = []
    for index in range(len(topTen)):
        for innerIndex in range(len(mainList)):
            if topTen[index][0] == mainList[innerIndex][0]:
                finalTopTen.append(mainList[innerIndex])
    return finalTopTen


def analyzeWeekAndDay(bestTen, flag):
    first, sec, third, fourth, fifth, sixth, seventh = [], [], [], [], [], [], []
    businessNameList = []
    daysList = first, sec, third, fourth, fifth, sixth, seventh
    for value in bestTen:
        businessNameList.append(value[0])
        if flag == 'Week':
            for idx in range(1, 8):
                daysList[idx - 1].append(int(value[idx]))
        else:
            for idx in range(1, 7):
                daysList[idx - 1].append(int(value[idx]))

    return daysList, businessNameList


def analyzeBusiness(businessFile):
    name, city, state, businessType, latitude, longitude = [], [], [], [], [], []
    entireBusiness = name, city, state, businessType, latitude, longitude
    for val in businessFile:
        for idx in range(6):
            entireBusiness[idx].append(val[idx])
    return entireBusiness


def top500(businessName, entireBusiness):
    businessLat, businessLong, businessText = [], [], []
    businessName = businessName[-500:]
    for index in businessName:
        for innerIndex in range(len(entireBusiness[0])):
            if index[0] == entireBusiness[0][innerIndex]:
                businessText.append(entireBusiness[0][innerIndex])
                businessLat.append(entireBusiness[4][innerIndex])
                businessLong.append(entireBusiness[5][innerIndex])
    return businessText, businessLat, businessLong


def checkCity(mainList):
    for record in mainList:
        if len(record[2]) != 2 and len(record[2]) != 3:
            mainList.remove(record)


def main():
    file_checkIn = "yelp_dataset/checkin.json"
    file_business = "yelp_dataset/business.json"
    file_rating = "yelp_dataset/tip.json"

    # Extracting business names
    yelp_business = Yelping(file_business)
    businessName = yelp_business.extractBusinessNames()

    # Extracting check-ins for all the businesses extracted for all the days of week
    yelp_days = Yelping(file_checkIn)
    yelp_days.readCheckinFileDays(businessName)

    # Extracting check-ins for all the businesses extracted for time of the day
    yelp_time = Yelping(file_checkIn)
    yelp_time.readCheckinFileTime(businessName)

    # Extracting ratings for all business
    yelp_rating = Yelping(file_rating)
    yelp_rating.readBusinessRatings(businessName)

    # Extracting business info
    yelp_businessinfo = Yelping(file_business)
    yelp_businessinfo.extractBusinessInfo(businessName)

    # Analyze businesses according to the days of the week
    timeWeek = readCSV('checkins.csv')
    sortedCountListWeek = busiestBusiness(timeWeek, 'Week')
    weekTen = findTopTen(sortedCountListWeek, timeWeek)
    daysList, businessNameList = analyzeWeekAndDay(weekTen, 'Week')

    # Plot the different analysis of businesses on a given week
    flag = 'Week'
    plotGraphs.plotting(timeWeek, flag)
    plotGraphs.plotInfo(daysList, businessNameList, flag)
    plotGraphs.plotInfoIndividual(daysList, businessNameList, flag)

    # Analyze businesses according to the different time ranges in a day
    timeDay = readCSV('time.csv')
    sortedCountListDay = busiestBusiness(timeDay, 'Day')
    dayTen = findTopTen(sortedCountListDay, timeDay)
    daysList, businessNameList = analyzeWeekAndDay(dayTen, 'Day')

    # Plot the different analysis of businesses on a given day
    flag = 'Day'
    plotGraphs.plotting(timeDay, flag)
    plotGraphs.plotInfo(daysList, businessNameList, flag)
    plotGraphs.plotInfoIndividual(daysList, businessNameList, flag)

    businessFile = readCSV('businessDescriptn.csv')
    checkCity(businessFile)
    entireBusiness = analyzeBusiness(businessFile)
    businessText, businessLat, businessLong = top500(sortedCountListWeek, entireBusiness)
    plotGraphs.plotOnMap(businessLat, businessLong, businessText)


if __name__ == '__main__':
    main()
