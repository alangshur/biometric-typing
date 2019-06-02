# @file: userData.py
# Ryan is a Guinea Pig and writes password data to a CSV file
# ...feels bad man

import csv
import data
import pickle

def getUserDataFeatures():
	fileRead = open('data/user-password-data.csv', 'rb')
	userDataFeatures = pickle.load(fileRead)
	return userDataFeatures

def main():
	# load previous data
	fileRead = open('data/user-password-data.csv', 'rb')
	theResurrection = pickle.load(fileRead)
	# prompt user and generate raw feature outputs, akin to CSV file
	userData = userInterface.welcomeUserAndCollectUserPasswordData(10, 0)
	for datum in userData:
		theResurrection.append(data.getFeaturesFromList(datum))
	file = open('data/user-password-data.csv', 'wb')
	pickle.dump(theResurrection, file)

if __name__ == '__main__':
	main()