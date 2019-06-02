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
import userInterface

# globally stores the titles of each data entry from csv
labels = []

# returns list of all features dicts drawn from the csv
def getCSVFeatures():
	allFeatures = []
	with open('data/password-data.csv') as file:
		data = csv.reader(file, delimiter = ',')
		counter = 0
		for row in data:
			if counter > 1: break
			counter += 1
			# at header: populate labels
			if row[0] == 'subject':
				labels = row
			else:
				keyList = getListFromCSVEntry(row, labels)
				features = getFeaturesFromList(keyList)
				allFeatures.append(features)
	return allFeatures

# given list of attempts, return list of features normalized by phi
def getNormalizedFeatureSet(attemptList, phi):
	normalized = []
	for attempt in attemptList:
		print('Attempt:')
		print(attempt)
		normalizedAttempt = {}
		for feature in attempt:
			keystroke = (feature[0], feature[1], feature[2])
			normalizedAttempt[feature] = abs(attempt[feature] - phi[keystroke])
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
	# DEBUG
	# print(keyList)
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
	# DEBUG
	# print(features)
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
			# special case for shift key
			if labelList[1] == "Shift":
				currKey = "R"
			keyPress = (currKey, "DOWN", time)
			holdTime = float(row[index])
			keyRelease = (currKey, "UP", time+holdTime)
			attempt.append(keyPress)
			attempt.append(keyRelease)
		# time between key-presses held in Down-Down
		elif labelList[0] == "DD":
			time += float(row[index])
	return attempt

########################################################
# generateAllFeatureSets
# returns a tuple of two lists of feature vectors,
# 	one from the authentic user and one from other users
########################################################
def generateAllFeatureSets():
	return None

# DEBUG
def test():
	userData = userInterface.welcomeUserAndCollectUserPasswordData(5)
	features = []
	for datum in userData:
		features.append(getFeaturesFromList(datum))
	phi = getPhiFromAttemptList(features)
	# print('PHI, BITCH:')
	# print(phi)
	# print("And those dummy thicc raw features, too:")
	print(features)
	normalizedFeatures = getNormalizedFeatureSet(features, phi)
	print("Real Friends:")
	for f in normalizedFeatures:
		print("Trial:")
		print(f)
		print(sum(f.values()))

	imposterData = userInterface.welcomeUserAndCollectUserPasswordData(5)
	imposterFeatures = []
	for datum in imposterData:
		imposterFeatures.append(getFeaturesFromList(datum))
	normalizedImposterFeatures = getNormalizedFeatureSet(imposterFeatures, phi)
	print("Fake Friends:")
	for f in normalizedImposterFeatures:
		print("Trial:")
		print(f)
		print(sum(f.values()))

test()
