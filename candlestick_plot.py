"""
A Python program that pulls stock price and sentiment data from 
Yahoo Finance and SentDex, respectively, and graphs an interactive
candlestick chart.

created by William Lu and Kevin Crispie at Olin College of Engineering

To use: install ystockquote and bokeh. See README for more details

On docstrings: this code is not "doctestable" because almost all our
data is stored in dictionaries.  Keys are not stored in the same order
on every computer, which means doctests will not work properly.
"""

import csv
import datetime
import time
import pandas as pd
import ystockquote

from math import pi
#be careful about using import *s in general, it's not unreasonable to do here
#given that it's the only package you did an import * from, but it still makes
#it so that it isn't as easy to track where functions are coming from.
from bokeh.plotting import *
from bokeh.models import HoverTool 
from collections import OrderedDict

"""
on docstrings: this code is not doctestable for two main reasons
"""

class convert_time(object):
	"""Converts time back and forth between unix time and normal time"""
	def __init__(self, time):
		self.time = time

	def __str__(self):
		return self.time

	def convert_to_ISO(self):
		"""
		Converts from unix timestamps to ISO time (string output)
		"""
		return datetime.datetime.fromtimestamp(int(self.time)).strftime('%Y-%m-%d')

	def convert_to_datetime(self):
		"""
		Converts ISO date in string format to datetime format
		"""
		datetime_conv = time.strptime(str(self), "%Y-%m-%d") #separates out each component of ISO date
		return datetime.date(datetime_conv.tm_year, datetime_conv.tm_mon, datetime_conv.tm_mday)

def load_stock(ticker,start_date,end_date):
	"""
	Loads historical stock data from Yahoo Finance given the stock ticker, start date, and end date
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

                #oh my lord this is nested deep, but it really seems unavoidable. To make this look less terrible,
                #consider yet another function!
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
	avg_data = {
        #some really funny indenting going on here. Why did you guys use 8 spaces for indents?
				'date' : [],
				'sentiment' : [],
	}

	for k in data:
		avg_sent = sum(data[k]) / float(len(data[k]))
		avg_data['date'].append(k)
		avg_data['sentiment'].append(avg_sent)

	return avg_data

def plot_candlestick():

	ticker = raw_input('What is the stock ticker you want to graph? ')
	start_date = raw_input('What start date would you like? [yyyy-mm-dd] ')
	end_date = raw_input('What end date would you like? [yyyy-mm-dd] ')

	data = load_stock(ticker, start_date, end_date)

	"""Test code"""
	sent_data = load_sentiment(ticker, start_date, end_date)
	#print sent_data
	avg_data = process_sentiment(sent_data)
	#print avg_data
	"""End test code"""

	df = pd.DataFrame(data)
	df["date"] = pd.to_datetime(df["date"])

	df2 = pd.DataFrame(avg_data)
	df2["date"] = pd.to_datetime(df2["date"])
	print df2

	mids = (df.open + df.close)/2
	spans = abs(df.close-df.open)

	inc = df.close > df.open
	dec = df.open > df.close
	w = 12*60*60*1000 # half day in ms

	output_file("candlestick.html", title="candlestick.py example")

	TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover"

	p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000)

	p.segment(df.date, df.high, df.date, df.low, color="black", toolbar_location="left")
	p.rect(df.date[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black", source = ColumnDataSource(data={"open": df.open[inc], "close": df.close[inc], "sentiment": df2.sentiment}))
	p.rect(df.date[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black", source = ColumnDataSource(data={"open": df.open[dec], "close": df.close[dec], "sentiment": df2.sentiment}))

	hover = p.select(dict(type=HoverTool))
	hover.tooltips = {"open":"@open","closing":"@close", "sentiment":"@sentiment"}

	p.title = "{} Candlestick".format(ticker)
	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha=0.3

	show(p)  # open a browser

if __name__ == '__main__':
	plot_candlestick()

#I don't have many comments on your code! It's nice and modular, and really well documented. Really the only thing to consider is maybe getting even more functions in there to break up the particularly long bits of code.
