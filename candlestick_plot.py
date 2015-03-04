import csv
import datetime
import pandas as pd

from bokeh.plotting import *

def convert_time(unix_time):
	"""
	Converts unix time to 'normal' time
	returns date from unix time
	"""
	return(datetime.datetime.fromtimestamp(int(unix_time)).strftime('%m-%d-%Y'))

def load_stock():
	data = {
		'row_id' : [],
		'time' : [],
		'ticker' : [],
		'value' : [],
		'open_price' : [],
		'close' : [],
		'high' : [],
		'low' : [],
		'MA100' : [],
		'MA250' : [],
		'MA500' : [],
		'M5000' : [],
	}
	with open('sentdex_section.csv') as f:
		next(f)
		fieldnames = ['row_id','time','ticker','value','open_price','close','high','low','MA100','MA250','MA500','M5000']
		reader = csv.DictReader(f, fieldnames = fieldnames)
		
		for row in reader:
			data['time'].append(convert_time(row['time']))
			data['open_price'].append(float(row['open_price']))
			data['high'].append(float(row['high']))
			data['low'].append(float(row['low']))
			data['close'].append(float(row['close']))
	return data

# def initial_vis():
# """Parses through csv file and prints each row as a dictionary"""
# 	with open('sentdex_section.csv') as csvfile:
# 		reader = csv.DictReader(csvfile)

# 		for row in reader:
# 			print row
# 		# 	print(row['id'], row['time'], row['type'], row['value'],
# 		# 		row['open'], row['close'], row['high'], row['low'],
# 		# 		row['MA100'], row['MA250'], row['MA500'], row['M5000'])

# def candlestick_plot():
# 	"""Plots stock data from a csv file as a candlestick chart"""

if __name__ == '__main__':
	load_stock()