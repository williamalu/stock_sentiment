# stock_sentiment

##The GitHub repository for a stock sentiment analyzer and data visualizer.

**Authors: William Lu and Kevin Crispie**

**Obtaining necessary packages:**

This data visualizer uses Bokeh. Install Bokeh by following the directions on Bokeh's website here:
http://bokeh.pydata.org/en/latest/docs/installation.html

In order to run the visualizer, the module ystockquote must also be downloaded. It can be downloaded using the terminal as the following:

```
$ pip install ystockquote
```

Further directions can be found here: https://pypi.python.org/pypi/ystockquote

It is possible that ystockquote must be modified in order to get the code to run. It is line 165, and must be modified to:

```
url = 'http://real-chart.finance.yahoo.com/table.csv?%s' % params
```

Also, stocks_sentdex.csv must be downlaoded. This provides the sentiment data. It can be downloaded here: 
http://sentdex.com/downloads/stocks_sentdex.csv.gz

**Running the data visualizer:**

When running the data visualizer, it is important to input a ticker in all capital letters, according to the proper ticker form (e.g. Google is GOOG, Apple is AAPL). Also, the date must be inputted as YYYY-mm-dd, or year (4 digits), then month(2 digits) and then day (2 digits), all separated by dashes. Input a start date and and end date that is after 2012. The end date should be after the start date for the program to work.

The code will likely take a long time to run. Hit Ctrl-C to stop execution.
