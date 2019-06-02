# @file: userData.py
# Ryan is a Guinea Pig and writes password data to a CSV file
# feels bad man

import csv
import userInterface

def main():
	# prompt user and generate raw feature outputs, akin to CSV file
	with open('user-password-data.csv', 'wb') as file:
		writer = csv.writer(file)
		writer.writerow(['row'.encode('utf-8')])

if __name__ == '__main__':
	main()