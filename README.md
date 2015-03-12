# stock_sentiment

The GitHub repository for a stock sentiment analyzer and data visualizer.

-William Lu and Kevin Crispie

Obtaining necessary packages:

This data visualizer uses bokeh. Install Bokeh by following the directions on Bokeh's website here:
http://bokeh.pydata.org/en/latest/docs/installation.html

In order to run the visualizer, ystockquote must also be downloaded. It can be downloaded using the terminal as the following:

$ pip install ystockquote

It is possible that ystockquote must be modified in order to get the code to run. It is line 165, and must be modified to:

url = 'http://real-chart.finance.yahoo.com/table.csv?%s' % params

Also, stocks_sentdex.csv must be downlaoded. This provides the sentiment data. It can be downloaded here: 
http://sentdex.com/downloads/stocks_sentdex.csv.gz

Running the data visualizer:

When running the data visualizer, it is important to input a ticker in all capital letters, according to the proper ticker form (eg Google is GOOG, Apple is AAPL). Also, the date must be inputted as YYYY-mm-dd, or year (4 digits), then month(2 digits) and then day (2 digits), all separated by dashes. The code will likely take a long time to run. Hit control-c to stop execution. 
