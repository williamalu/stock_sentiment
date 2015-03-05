import numpy as np
import bokeh.plotting as bp
from bokeh.plotting import figure, HBox, output_file, show, VBox
from bokeh.models import HoverTool 
bp.output_file('test.html')

TOOLS="pan,wheel_zoom,box_zoom,reset,save"

fig = bp.figure(title = "Stock Sentiment",tools="reset,hover")
N = 40
sentiments = np.array(np.random.normal(size=N))
ticker_prices = np.array(np.random.randint(5,100,size=N))
colors = [
    "#%02x%02x%02x" % (r, g, 150) for r, g in zip(np.floor(50+2*sentiments), np.floor(30+2*ticker_prices))
]

s1 = fig.scatter(x=sentiments,y=ticker_prices,color=colors,size=10,legend='Stock Sentiment Series')
s1.select(dict(type=HoverTool)).tooltips = {"sentiment value":"@x", "closing price":"@y"}
fig.xaxis.axis_label="Stock Sentiment"
fig.yaxis.axis_label="Closing Price"
bp.show(fig)
