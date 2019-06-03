#'########::'##::::'##::::'###::::'########:::   '########:'########::::'###::::'########:'##::::'##:'########::'########:
# ##.... ##: ##:::: ##:::'## ##:::... ##..::::    ##.....:: ##.....::::'## ##:::... ##..:: ##:::: ##: ##.... ##: ##.....::
# ##:::: ##: ##:::: ##::'##:. ##::::: ##::::::    ##::::::: ##::::::::'##:. ##::::: ##:::: ##:::: ##: ##:::: ##: ##:::::::
# ########:: #########:'##:::. ##:::: ##::::::    ######::: ######:::'##:::. ##:::: ##:::: ##:::: ##: ########:: ######:::
# ##.....::: ##.... ##: #########:::: ##::::::    ##...:::: ##...:::: #########:::: ##:::: ##:::: ##: ##.. ##::: ##...::::
# ##:::::::: ##:::: ##: ##.... ##:::: ##::::::    ##::::::: ##::::::: ##.... ##:::: ##:::: ##:::: ##: ##::. ##:: ##:::::::
# ##:::::::: ##:::: ##: ##:::: ##:::: ##::::::    ##::::::: ########: ##:::: ##:::: ##::::. #######:: ##:::. ##: ########:
#..:::::::::..:::::..::..:::::..:::::..:::::::.   .::::::::........::..:::::..:::::..::::::.......:::..:::::..::........::
#
#      '########:'##::::'##:'########:'########:::::'###:::::'######::'########::'#######::'########::
#       ##.....::. ##::'##::... ##..:: ##.... ##:::'## ##:::'##... ##:... ##..::'##.... ##: ##.... ##:
#       ##::::::::. ##'##:::::: ##:::: ##:::: ##::'##:. ##:: ##:::..::::: ##:::: ##:::: ##: ##:::: ##:
#       ######:::::. ###::::::: ##:::: ########::'##:::. ##: ##:::::::::: ##:::: ##:::: ##: ########::
#       ##...:::::: ## ##:::::: ##:::: ##.. ##::: #########: ##:::::::::: ##:::: ##:::: ##: ##.. ##:::
#       ##:::::::: ##:. ##::::: ##:::: ##::. ##:: ##.... ##: ##::: ##:::: ##:::: ##:::: ##: ##::. ##::
#       ########: ##:::. ##:::: ##:::: ##:::. ##: ##:::: ##:. ######::::: ##::::. #######:: ##:::. ##:
#........::..:::::..:::::..:::::..:::::..::..:::::..:::......::::::..::::::.......:::..:::::..::

import re
import csv
from collections import defaultdict
from data import userInterface
import random
import sys
import pickle

# globally stores the titles of each data entry from csv
labels = []

# returns list of all features dicts drawn from the csv
def getCSVFeatures():
	allFeatures = []
	with open('data/password-data.csv') as file:
		data = csv.reader(file, delimiter = ',')
		for row in data:
			# at header: populate labels
			if row[0] == 'subject':
				labels = row
			else:
				keyList = getListFromCSVEntry(row, labels)
				features = getFeaturesFromList(keyList)
				allFeatures.append(features)
	return allFeatures

def getRandomCSVFeatures(limit):
	it = 0
	allFeatures = []
	with open('data/password-data.csv') as file:
		data = csv.reader(file, delimiter = ',')
		d = list(data)
		labels = d[0]
		while True:
			it += 1
			if it == limit: break
			row = random.choice(d)
			if row[0] == 'subject': continue
			keyList = getListFromCSVEntry(row, labels)
			features = getFeaturesFromList(keyList)
			allFeatures.append(features)
	return allFeatures



def getValidCSVFeatures():
	allFeatures = []
	validFeatures = []
	with open('data/password-data.csv') as file:
		data = csv.reader(file, delimiter = ',')
		it = 0
		for row in data:
			it += 1
			if it == 2001: break
			# at header: populate labels
			if row[0] == 'subject':
				labels = row
			elif row[0] == 's002':
				keyList = getListFromCSVEntry(row, labels)
				features = getFeaturesFromList(keyList)
				validFeatures.append(features)
			else:
				keyList = getListFromCSVEntry(row, labels)
				features = getFeaturesFromList(keyList)
				allFeatures.append(features)
	return validFeatures, allFeatures

# given list of attempts, return list of features normalized by phi
def getNormalizedFeatureSet(attemptList, phi):
	normalized = []
	for attempt in attemptList:
		normalizedAttempt = {}
		for feature in attempt:
			keystroke = (feature[0], feature[1], feature[2])
			difference = attempt[feature] - phi[keystroke]
			normalizedAttempt[feature] = difference
			if feature[1] != None:
				normalizedAttempt[(feature[0], feature[1], feature[2], 'squared')] = difference**2
		normalized.append(normalizedAttempt)
	return normalized

# attemptList is a list of defaultdict(int)s, each representing one password
# attempt for a given user
# @return phi: a dict from keystroke tuples to average times
def getPhiFromAttemptList(attemptList):
	# generate list of (prevKey, currKey, event) keystroke tuples, agnostic to time values
	phi = {}
	for f in attemptList[0]:
		keystroke = (f[0], f[1], f[2])
		phi[keystroke] = 0.0
	# populate phi with total times for all attempts
	for attempt in attemptList:
		for f in attempt:
			keystroke = (f[0], f[1], f[2])
			phi[keystroke] += attempt[f]
	# normalize phi to get average times
	for k in phi:
		phi[k] /= float(len(attemptList))

	return phi

# given list of (keystroke, UP/DOWN, time) events, generate features for password attempt
# each feature represented by (pastKey, currKey, event) tuple
def getFeaturesFromList(keyList):
	features = defaultdict(int)
	# add 1-feature
	features[(None, None, None)] = 1

	prevKey = None
	prevDownTime, prevUpTime = 0.0, 0.0
	while keyList != []:
		# take 0-th index entry
		downEvent = keyList[0]
		key, event, time = downEvent
		# if key down event:
		if event == "DOWN":
			# search for corresponding key up event w/ matching keystroke
			upEvent = (None, None, None)
			index = 0
			while upEvent[0] != key or upEvent[1] != 'UP':
				# temp fix for index out of range bug
				if index > len(keyList): break
				upEvent = keyList[index]
				index += 1
			# compute H, UD, DD times
			holdTime = upEvent[2] - downEvent[2]
			upDownTime = downEvent[2] - prevUpTime
			downDownTime = downEvent[2] - prevDownTime
			# add features based on previous keystroke and previous times
			features[(None, key, 'H', 'linear')] = max(holdTime, 0)
			# features[(None, key, 'H', 'squared')] = holdTime**2
			features[(prevKey, key, 'UD', 'linear')] = max(upDownTime, 0)
			# features[(prevKey, key, 'UD', 'squared')] = upDownTime**2
			features[(prevKey, key, 'DD', 'linear')] = max(downDownTime, 0)
			# features[(prevKey, key, 'DD', 'squared')] = downDownTime**2
			# update latest key up and key down times, and prev key
			prevDownTime = downEvent[2]
			prevUpTime = upEvent[2]
			prevKey = key
			# remove both key up and key down event from list
			keyList.remove(downEvent)
			keyList.remove(upEvent)
	return features

# returns a list of (keyChar, pressed/released, timeIndex) tuples
def getListFromCSVEntry(row, labels):
	# list to fill with data
	attempt = []
	time = 0.0
	for index in range(3, len(labels)): # 3-offset avoids metadata at beginning
		label = labels[index]
		labelList = label.split(".")
		# time between key press & release held in Hold
		if labelList[0] == "H":
			currKey = labelList[1]
			if currKey == "Return": continue
			# special case for shift key
			if labelList[1] == "Shift":
				currKey = "R"
			# special cases for 'period' and 'five'
			if currKey == "period":
				currKey = "."
			if currKey == "five":
				currKey = "5"
			keyPress = (currKey, "DOWN", time)
			holdTime = float(row[index])
			keyRelease = (currKey, "UP", time+holdTime)
			attempt.append(keyPress)
			attempt.append(keyRelease)
		# time between key-presses held in Down-Down
		elif labelList[0] == "DD":
			time += float(row[index])
	return attempt

################################################################################
# @function: userFeatureSetsFromInterface
# calls userInterface to request password attempts from user
# 
# @return normalizedFeatures: a list of features, normalized by
# 	their distance from the average time
# @return phi: a vector representing the average times for each keystroke event
# 	for a user
################################################################################
def userFeatureSetsFromInterface():
	userData = userInterface.welcomeUserAndCollectUserPasswordData(2, 0)
	features = []
	for datum in userData:
		features.append(getFeaturesFromList(datum))
	phi = getPhiFromAttemptList(features)
	normalizedFeatures = getNormalizedFeatureSet(features, phi)
	return normalizedFeatures, phi

def getUserDataFeaturesValid():
	fileRead = open('data/user-password-data-harry.txt', 'rb')
	userDataFeatures = pickle.load(fileRead)
	return userDataFeatures

def getUserDataFeaturesInvalid():
	fileRead1 = open('data/user-password-data-alex.txt', 'rb')
	fileRead2 = open('data/user-password-data-ryan.txt', 'rb')
	userDataFeatures1 = pickle.load(fileRead1)
	userDataFeatures2 = pickle.load(fileRead2)
	return userDataFeatures1 + userDataFeatures2

################################################################################
# @function: generateAllFeatureSets
# generates all normalized features for a user and for CSV entries
# 
# @return userFeatureSets: a list of dict() objects representing the features
# 	for password attempts from the genuine user
# @return CSVFeatureSets: a list of dict() objects representing the features
# 	for password attempts from imposters, generated from the CSV
################################################################################
def generateAllFeatureSets(mode):

	if mode == 'demo':

		userAttempts = getUserDataFeaturesValid()
		phi = getPhiFromAttemptList(userAttempts)
		invalidAttempts = getUserDataFeaturesInvalid()
		userFeatureSets = getNormalizedFeatureSet(userAttempts, phi)
		CSVFeatureSets = getNormalizedFeatureSet(invalidAttempts, phi)

	elif mode == 'csv': 

		userFeatureSets, CSVFeatures = getValidCSVFeatures()
		phi = getPhiFromAttemptList(userFeatureSets)
		userFeatureSets = getNormalizedFeatureSet(userFeatureSets, phi)
		CSVFeatureSets = getNormalizedFeatureSet(CSVFeatures, phi)

	elif mode == 'user':

		userAttempts = getUserDataFeaturesValid()
		phi = getPhiFromAttemptList(userAttempts)
		userFeatureSets = getNormalizedFeatureSet(userAttempts, phi)
		CSVFeatures = getRandomCSVFeatures(1000) # arbitrary
		CSVFeatureSets = getNormalizedFeatureSet(CSVFeatures, phi)

	else:
		
		userFeatureSets, phi = userFeatureSetsFromInterface()
		CSVFeatures = getCSVFeatures()
		CSVFeatureSets = getNormalizedFeatureSet(CSVFeatures, phi)

	return userFeatureSets, CSVFeatureSets, phi

#####################################################################################
# @function: requestPasswordAttempt
# for the live demo -- gets one password attempt from user input
#
# @param phi: a vector representing the authenticated user's average times, for
# 	normalizing the requested password's feature set
# @return attempt: a list containing one password attempt to check against the model
#####################################################################################
def requestPasswordAttempt(phi):
	password = userInterface.getOnePassword()
	passwordFeatures = getFeaturesFromList(password[0])
	attempt = getNormalizedFeatureSet([passwordFeatures], phi)
	return attempt

def main():
	assert sys.argv[1] == 'alex' or sys.argv[1] == 'harry' or sys.argv[1] == 'ryan'
	
	# load previous data
	fileRead = open('user-password-data-{}.txt'.format(sys.argv[1]), 'rb')
	theResurrection = pickle.load(fileRead)
	# prompt user and generate raw feature outputs, akin to CSV file
	userData = userInterface.welcomeUserAndCollectUserPasswordData(10, 0)
	for datum in userData:
		theResurrection.append(getFeaturesFromList(datum))
	file = open('user-password-data-{}.txt'.format(sys.argv[1]), 'wb')
	pickle.dump(theResurrection, file)

if __name__ == '__main__':
	main()
