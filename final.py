import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import os

app = Dash(__name__)

df=pd.read_excel('dashboard.xlsx')
totac=df.groupby('Date')['Outcome'].count()
totsuc=df[df['Outcome']=='Success'].groupby('Date')['Outcome'].count()
totnsuc=df[df['Outcome']=='Failure'].groupby('Date')['Outcome'].count()


# df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
# df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
# pieFig = px.pie(df, values='pop', names='country', title='Population of European continent')
sizes=[df[df['Outcome']=='Success'].shape[0],df[df['Outcome']=='Failure'].shape[0]]
pieFig = px.pie(values=sizes, labels=["failure", "success"], title='Success-Fail Rate')

totac2=df.groupby('State')['Outcome'].count()
pieFig2 = px.pie(values=totac2.values.flatten(), names=totac2.index, title='Outcome count for each state')

totac5=df.groupby('State')['Outcome'].count().reset_index()
totsuc5=df[df['Outcome']=='Success'].groupby('State')['Outcome'].count().reset_index()
totnsuc5=df[df['Outcome']=='Failure'].groupby('State')['Outcome'].count().reset_index()

app.layout = html.Div(children=[
    html.H1(children='CourseWork 2 Erlan'),

    html.Div(children='''
        Dashboard.
    '''),

    dcc.Dropdown(
                ["Total", "Success", "Failure"],
                'Total',
                id='first-y-axis'
            ),

    dcc.Graph(
        id='first-graph',
        figure={}
    ),

    dcc.Dropdown(
            ["Total", "Success", "Failure"],
            'Total',
            id='second-y-axis'
        ),

    dcc.Graph(
        id='second-graph',
        figure={}
    ),

    dcc.Graph(id="third-graph", figure=pieFig),
    dcc.Graph(id="fourth-graph", figure=pieFig2),

    dcc.Dropdown(
            ["Total", "Success", "Failure"],
            'Total',
            id='fifth-y-axis'
        ),
    dcc.Graph(
        id='fifth-graph',
        figure={}
    ),
])

@app.callback(
    Output('first-graph', 'figure'),
    Input('first-y-axis', 'value'))
def update_graph(first_y_axis):
    xValues = totac.index
    yValues = totac
    if first_y_axis == "Success":
      xValues = totsuc.index
      yValues = totsuc
    elif first_y_axis == "Failure":
      xValues = totnsuc.index
      yValues = totnsuc
    fig = px.line(x=xValues, y = yValues, labels={"x": "Dates", "y": first_y_axis})
    return fig

@app.callback(
    Output('second-graph', 'figure'),
    Input('second-y-axis', 'value'))
def update_graph(first_y_axis):
    xValues = totac.index
    yValues = totac
    if first_y_axis == "Success":
      xValues = totsuc.index
      yValues = totsuc
    elif first_y_axis == "Failure":
      xValues = totnsuc.index
      yValues = totnsuc
    fig = px.scatter(x=xValues, y = yValues, labels={"x": "Dates", "y": first_y_axis})
    return fig

@app.callback(
    Output('fifth-graph', 'figure'),
    Input('fifth-y-axis', 'value'))
def update_graph(first_y_axis):
    xValues = totac5.State
    yValues = totac5.Outcome
    if first_y_axis == "Success":
      xValues = totsuc5.State
      yValues = totsuc5.Outcome
    elif first_y_axis == "Failure":
      xValues = totnsuc5.State
      yValues = totnsuc5.Outcome
    fig = px.bar(x=xValues, y = yValues, labels={"x": "Dates", "y": first_y_axis})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=int(os.environ.get('PORT', 8000)))