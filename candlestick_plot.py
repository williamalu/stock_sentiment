import csv
import datetime
import time
import pandas as pd
import ystockquote

from math import pi
from bokeh.plotting import *
from bokeh.models import HoverTool 
from collections import OrderedDict

class convert_time(object):
	"""Converts time back and forth between unix time and normal time"""
	def __init__(self, time):
		self.time = time

	def __str__(self):
		return self.time

	def convert_to_ISO(self):
		return datetime.datetime.fromtimestamp(int(self.time)).strftime('%Y-%m-%d')

	def convert_to_datetime(self):
		"""Converts ISO date in string format to datetime format"""
		datetime_conv = time.strptime(str(self), "%Y-%m-%d")
		return datetime.date(datetime_conv.tm_year, datetime_conv.tm_mon, datetime_conv.tm_mday)

def load_stock(ticker,start_date,end_date):
	"""
	Loads historical stock data from Yahoo Finance given the stock ticker and date range
	"""
 	data = {
 		'date' : [],
 		'open' : [],
 		'high' : [],
 		'low' : [],
 		'close' : [],
 		'volume' : [],
 		'adj_close': [],
 	}
	
	raw_stock_data = ystockquote.get_historical_prices(ticker, start_date, end_date)

	for day in raw_stock_data:
		data['date'].append(str(day))
		data['open'].append(float(raw_stock_data[day]['Open']))
		data['high'].append(float(raw_stock_data[day]['High']))
		data['low'].append(float(raw_stock_data[day]['Low']))
		data['close'].append(float(raw_stock_data[day]['Close']))
		data['volume'].append(int(raw_stock_data[day]['Volume']))
		data['adj_close'].append(float(raw_stock_data[day]['Adj Close']))

	return data

def load_sentiment(ticker,start_date,end_date):
	"""
	Loads sentiment from sentdex csv file as a dictionary 
	with format {date1:[1,2,3...] , date2:[1,2,3...]}
	"""
	data = {}

	with open('stocks_sentdex.csv') as f:
		next(f)
		fieldnames = ['row_id','time','ticker','value','open_price','close','high','low','MA100','MA250','MA500','M5000']
		reader = csv.DictReader(f, fieldnames = fieldnames)

		time_step = datetime.timedelta(days = 1)
		curr_date = start_date
		curr_date = convert_time(curr_date)
		curr_date = curr_date.convert_to_datetime() #converts curr_date to datetime format for incrementing
		end_date = convert_time(end_date)
		end_date = end_date.convert_to_datetime() #converts end_date to datetime format for incrementing
		date_list = []
		while curr_date <= end_date:
			date_list.append(str(curr_date))
			curr_date += time_step

		for row in reader:
			converted_time = convert_time(row['time'])
			for a in date_list:
				if a == converted_time.convert_to_ISO():
					if row['ticker'] == ticker.lower():
						if converted_time.convert_to_ISO() not in data:
							data[converted_time.convert_to_ISO()] = list()
							data[converted_time.convert_to_ISO()].append(int(row['value']))
						else:
							data[converted_time.convert_to_ISO()].append(int(row['value']))
					else:
						pass #ignores row of data if the data is not for a ticker we care about
				else:
					pass

	return data

def process_sentiment(data):
	"""
	Averages all the sentiment numbers for a date key in a dictionary
	"""
	avg_data = {}
	for k in data:
		avg_sent = sum(data[k]) / float(len(data[k]))
		avg_data[k] = avg_sent

	return avg_data

def plot_candlestick():

	ticker = raw_input('What is the stock ticker you want to graph? ')
	start_date = raw_input('What start date would you like? [yyyy-mm-dd] ')
	end_date = raw_input('What end date would you like? [yyyy-mm-dd] ')

	data = load_stock(ticker, start_date, end_date)

	"""Test code"""
	sent_data = load_sentiment(ticker, start_date, end_date)
	print sent_data
	avg_data = process_sentiment(sent_data)
	print avg_data
	"""End test code"""

	df = pd.DataFrame(data)
	df["date"] = pd.to_datetime(df["date"])

	mids = (df.open + df.close)/2
	spans = abs(df.close-df.open)

	inc = df.close > df.open
	dec = df.open > df.close
	w = 12*60*60*1000 # half day in ms

	output_file("candlestick.html", title="candlestick.py example")

	TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover"

	p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000)

	p.segment(df.date, df.high, df.date, df.low, color="black", toolbar_location="left")
	p.rect(df.date[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black", source = ColumnDataSource(data={"open": df.open[inc], "close": df.close[inc]}))
	p.rect(df.date[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black", source = ColumnDataSource(data={"open": df.open[dec], "close": df.close[dec]}))

	hover = p.select(dict(type=HoverTool))
	hover.tooltips = {"open":"@open","closing":"@close"}

	p.title = "{} Candlestick".format(ticker)
	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha=0.3

	show(p)  # open a browser

if __name__ == '__main__':
	plot_candlestick()