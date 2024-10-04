# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', 
                                    options=[{'label':'All Sites','value':'ALL'}, 
                                        {'label':'CCAFS LC-40','value':'CCAFS LC-40'}, 
                                        {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}, 
                                        {'label':'KSC LC-39A','value':'KSC LC-39A'}, 
                                        {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}],
                                ##        [{'label':name,'value':name} for name in ['CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40']]],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', 
                                    min=0, max=10000, step=1000, 
                                    marks={0:'0', 100:'100'}, 
                                    value=[0, 10000]), 

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ]
                        )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        sites2cnums = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(sites2cnums, 
            values='class', 
            names='Launch Site', 
            title='Success Launch Number for All Sites')
    else:
    # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        sites2cnum = filtered_df.groupby('class').count().reset_index().iloc[:, :2]
        sites2cnum.columns = ['class', 'count']
        fig = px.pie(sites2cnum, 
            values='count', 
            names='class', 
            title='Success Launch Number for ' + str(entered_site))
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, slided_payload):
    if entered_site == 'ALL':
        factors2cnum = spacex_df[(spacex_df['Payload Mass (kg)'] > float(slided_payload[0]))&(spacex_df['Payload Mass (kg)'] < float(slided_payload[1]))]
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        factors2cnum = filtered_df[(filtered_df['Payload Mass (kg)'] > float(slided_payload[0]))&(filtered_df['Payload Mass (kg)'] < float(slided_payload[1]))]
    fig = px.scatter(factors2cnum, 
        x='Payload Mass (kg)', 
        y='class', 
        color='Booster Version Category',
        title='Factors to Success Launch Number at ' + str(entered_site))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()