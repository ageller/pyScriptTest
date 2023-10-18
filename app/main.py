import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

from bokeh.plotting import *
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Scatter, Select, CustomJS
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.embed import json_item

from pyscript import display

from js import document, console, JSON, Bokeh


def count_letters(event):
    input_text = document.querySelector("#input_text").value
    output_div = document.querySelector("#count_letters_output")
    output_div.innerText = len(input_text)

def plot_exponent(event):
    exponent = float(document.querySelector('#exponent').value)
    
    # clear the output div
    output_div = document.querySelector("#plot_exponent_output")
    output_div.innerHTML = ""

    fig, ax = plt.subplots()
    xx = np.linspace(0,4,100)
    ax.plot(xx, xx**exponent)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y = x^{' + str(exponent) +'}$')
    ax.set_ylim(0,10)

    display(fig, target = "plot_exponent_output")

def bokeh_plot():
    # code from my GitHub repo here : https://github.com/ageller/IntroToBokeh/blob/main/BokehDemos.ipynb
    
    def createPlot(
            source, x='x', y='y', 
            xLabel='mass [Earth masses]', yLabel='radius [Earth radii]', 
            xRange=(0.4, 1e5), yRange=(0.3, 50),
            xAxisType='log', yAxisType='log',
            width=350, height=350, title=None
        ):

        # define the tools you want to use
        TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"

        # create a new plot and renderer
        f = figure(tools=TOOLS, width=width, height=height, title=title, x_axis_type=xAxisType, y_axis_type=yAxisType, y_range=yRange, x_range=xRange)
        renderer = f.scatter(x, y, source=source, color='black', alpha=0.5, size=5, marker='circle')
        f.xaxis.axis_label = xLabel
        f.yaxis.axis_label = yLabel

        # (optional) define different colors for highlighted and non-highlighted markers
        renderer.selection_glyph = Scatter(fill_alpha=1, fill_color="firebrick", line_color=None)
        renderer.nonselection_glyph = Scatter(fill_alpha=0.2, fill_color="gray", line_color=None)

        return f

    # I want to send the labels to this function also so that it can be more versatile
    # I will expect the labels to be a dict with a key for each columns that I want to include and value for the label
    def createTable(source, labels, width=350, height=300):
        # create a table to hold the selections
        columns = []
        for field in labels:
            columns.append(TableColumn(field=field, title=labels[field]))

        t = DataTable(source=source, columns=columns, width=width, height=height)

        return t

   
    # read in the data
    df = pd.read_csv('./PS_2021.10.05_11.19.37.csv', comment = '#')

    usedf = df.loc[ (pd.notnull(df['pl_bmasse'])) & (pd.notnull(df['pl_rade'])) & 
                (pd.notnull(df['pl_orbeccen'])) & (pd.notnull(df['pl_orbper'])) ].reset_index()
    
    source = ColumnDataSource(data=dict(x1=usedf['pl_bmasse'], y1=usedf['pl_rade'], 
                                        x2=usedf['pl_orbper'], y2=usedf['pl_orbeccen']))

    # define labels for the plots and table
    labels = dict(x1="mass [Earth masses]", y1="radius [Earth radii]",
                x2="orbital period [days]", y2="eccentricity")

    # create two figures
    f1 = createPlot(source, x='x1', y='y1', xLabel=labels['x1'], yLabel=labels['y1'], xRange=(0.4, 1e5), yRange=(0.3, 50),)
    f2 = createPlot(source, x='x2', y='y2', xLabel=labels['x2'], yLabel=labels['y2'], xRange=(0.1, 1e4), yRange=(0.0, 1), 
                    yAxisType='linear')

    t = createTable(source, labels, width=700)

    # create a griplot layout and show the plot and table
    layout = column(
        row(f1, f2),
        row(t)
    )


    # show the plot
    f_json = json.dumps(json_item(layout, "bokeh_output"))

    Bokeh.embed.embed_item(JSON.parse(f_json))

bokeh_plot()

