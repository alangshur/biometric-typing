import re
import csv
from collections import defaultdict

# globally stores the titles of each data entry from csv
labels = []

# returns list of all features dicts drawn from the csv
def getPhatPheatures():
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

def getFeaturesFromList(keyList):
	features = defaultdict(int)
	# add 1-feature
	features[(None, None, None)] = 1

	prevKey, currKey = None, None
	awaitingRelease = False
	lastReleaseTime = 0.0
	lastPressTime = 0.0
	for entry in keyList:
		keyChar, event, time = entry
		if event == "press":
			# set "flags"
			currKey = keyChar
			awaitingRelease = True

			# check if we need to add between-key features
			if prevKey is not None:
				upDownTime = time - lastReleaseTime
				features[(currKey, prevKey, "UD")] = upDownTime

				downDownTime = time - lastPressTime
				features[(currKey, prevKey, "DD")] = downDownTime

				# update
				lastPressTime = time
		elif event == "release":
			holdTime = time - lastPressTime
			features[(currKey, None, "H")] = holdTime
			prevKey = currKey
			lastReleaseTime = time
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
			keyPress = (currKey, "press", time)
			holdTime = float(row[index])
			keyRelease = (currKey, "release", time+holdTime)
			attempt.append(keyPress)
			attempt.append(keyRelease)
		# time between key-presses held in Down-Down
		elif labelList[0] == "DD":
			time += float(row[index])
	return attempt