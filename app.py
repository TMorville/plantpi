import dash
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader.data import DataReader
import time
from collections import deque
import plotly.graph_objs as go
import random

app = dash.Dash('plant-data')

max_length = 50
times = deque(maxlen=max_length)
temp = deque(maxlen=max_length)
lumen = deque(maxlen=max_length)
humidity = deque(maxlen=max_length)

data_dict = {"Temperature":temp,
"Lumen": lumen,
"Humidity": humidity}

def update_obd_values(times, temp, lumen, humidity):

    times.append(time.time())
    if len(times) == 1:
        #starting relevant values
        temp.append(random.randrange(15,30))
        lumen.append(random.randrange(0,25))
        humidity.append(random.randrange(10,20))
    else:
        for data_of_interest in [temp, lumen, humidity]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))

    return times, temp, lumen, humidity

times, temp, lumen, humidity = update_obd_values(times, temp, lumen, humidity)

app.layout = html.Div([
    html.Div([
        html.H2('Plant data',
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='plant-data-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Temperature','Lumen','Humidity'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=100),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('plant-data-name', 'value')],
    events=[dash.dependencies.Event('graph-update', 'interval')]
    )

def update_graph(data_names):
    graphs = []
    update_obd_values(times, temp, lumen, humidity)


    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'


    for data_name in data_names:

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})

if __name__ == '__main__':
    app.run_server(debug=True)