import csv
import datetime
import pandas as pd

from math import pi
from bokeh.plotting import *

def convert_time(unix_time):
	"""
	Converts unix time to 'normal' time
	returns date from unix time
	"""
	return(datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d'))

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
			data['row_id'].append(row['row_id'])
			data['time'].append(convert_time(row['time']))
			data['ticker'].append(row['ticker'])
			data['value'].append(row['value'])
			data['open_price'].append(float(row['open_price']))
			data['close'].append(float(row['close']))
			data['high'].append(float(row['high']))
			data['low'].append(float(row['low']))
			data['MA100'].append(float(row['MA100']))
			data['MA250'].append(float(row['MA250']))
			data['MA500'].append(float(row['MA500']))
			data['M5000'].append(float(row['M5000']))
	return data

def plot_candlestick():

	df = pd.DataFrame(load_stock())

	print df.open_price

	mids = (df.open_price + df.close)/2
	spans = abs(df.close-df.open_price)

	inc = df.close > df.open_price
	dec = df.open_price > df.close
	w = 12*60*60*1000 # half day in ms

	output_file("candlestick.html", title="candlestick.py example")

	TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

	p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000)

	p.segment(df.time, df.high, df.time, df.low, color="black", toolbar_location="left")
	p.rect(df.time[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black")
	p.rect(df.time[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black")

	p.title = "AAPL Candlestick"
	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha=0.3

	show(p)  # open a browser

if __name__ == '__main__':
	plot_candlestick()