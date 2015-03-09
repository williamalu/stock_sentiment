import csv
import datetime
import pandas as pd
import ystockquote

from math import pi
from bokeh.plotting import *
from bokeh.models import HoverTool 
from collections import OrderedDict

def convert_time(unix_time):
	"""
	Converts unix time to 'normal' time
	returns date from unix time
	Note: not currently being used
	"""
	return(datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d'))

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

def plot_candlestick():

	ticker = raw_input('What is the stock ticker you want to graph? ')
	start_date = raw_input('What start date would you like? [yyyy-mm-dd] ')
	end_date = raw_input('What end date would you like? [yyyy-mm-dd] ')

	data = load_stock(ticker, start_date, end_date)
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