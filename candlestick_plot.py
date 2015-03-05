import csv
import datetime
import pandas as pd

from math import pi
from bokeh.plotting import *
from bokeh.models import HoverTool 

def convert_time(unix_time):
	"""
	Converts unix time to 'normal' time
	returns date from unix time
	Note: not currently being used
	"""
	return(datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d'))

def load_stock():
	data = {
		'date' : [],
		'open' : [],
		'high' : [],
		'low' : [],
		'close' : [],
		'volume' : [],
		'adj_close': [],
	}

	with open('GOOG.csv') as f:
		next(f)
		reader = csv.reader(f,delimiter=',')
		
		for row in reader:
			date, open_price, high, low, close, volume, adj_close = row
			data['date'].append(date)
			data['open'].append(float(open_price))
			data['high'].append(float(high))
			data['low'].append(float(low))
			data['close'].append(float(close))
			data['volume'].append(int(volume))
			data['adj_close'].append(float(adj_close))
	return data

def plot_candlestick():
	data = load_stock()
	data_ = ColumnDataSource(data=data)
	data_2 = ColumnDataSource(data=data)
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
	p.rect(df.date[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black", source = data_)
	p.rect(df.date[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black", source = data_2)

	hover = p.select(dict(type=HoverTool))
	hover.tooltips = {"open":"@open","closing":"@close"}

	#p.select(dict(type=HoverTool)).tooltips = {"sentiment value":"@openprice", "closing price":"@closeprice"}
	#p.select(dict(type=HoverTool)).tooltips = {"opening price":"$df.open", "closing price":"$df.close"}

	p.title = "GOOG Candlestick"
	p.xaxis.major_label_orientation = pi/4
	p.grid.grid_line_alpha=0.3

	show(p)  # open a browser

if __name__ == '__main__':
	plot_candlestick()