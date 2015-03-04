import csv

def initial_vis():
	"""Parses through csv file and prints each row as a dictionary"""
	with open('sentdex_section.csv') as csvfile:
		fieldnames = ['row_id', 'time', 'ticker', 'value', 'open_price', 'close', 'high', 'low', 'MA100', 'MA250', 'MA500', 'M5000']
		reader = csv.DictReader(csvfile, fieldnames = fieldnames)
		
		for row in reader:
			print row
		# 	print(row['id'], row['time'], row['type'], row['value'],
		# 		row['open'], row['close'], row['high'], row['low'],
		# 		row['MA100'], row['MA250'], row['MA500'], row['M5000'])

if __name__ == '__main__':
	initial_vis()