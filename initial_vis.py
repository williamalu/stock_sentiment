import csv

def initial_vis():
"""Parses through csv file and prints each row as a dictionary"""
	with open('sentdex_section.csv') as csvfile:
		reader = csv.DictReader(csvfile)

		for row in reader:
			print row
		# 	print(row['id'], row['time'], row['type'], row['value'],
		# 		row['open'], row['close'], row['high'], row['low'],
		# 		row['MA100'], row['MA250'], row['MA500'], row['M5000'])

if __name__ == '__main__':
	initial_vis()