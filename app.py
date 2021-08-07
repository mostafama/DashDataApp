# pip install dash
# to run: python dashDemo3Data.py
# View on your browser at http://127.0.0.1:8050/
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Br
from numpy import append
import plotly.express as px
import dash_table
import pandas as pd
from readDB import ReadMongoData as db
from dash.dependencies import Input, Output, State

dash_app = dash.Dash(__name__)
# app = dash.Dash("app")
app = dash_app.server

df = db.getBookingDetails()

# Convert the Decimal128 columns to float to work for the dash_table.DataTable
df[["BasePrice", "AgencyCommission"]] = df[[
    "BasePrice", "AgencyCommission"]].astype(str).astype(float)

# Summary for destinations
df_group_destination = df.groupby(["Destination"]).sum()[
    ["BasePrice", "AgencyCommission"]]

# df_group_destination1 = df[df['Destination'] == "Montreal"]
# fig = px.bar()

dash_app.layout = html.Div(
    children=[
        # represents the URL bar, doesn't render anything
        dcc.Location(id='url', refresh=False),
        dcc.Link('Home', href='/'),
        html.Br(),
        dcc.Link('Agent 1', href='/agent1'),
        html.Br(),
        # content will be rendered in this element
        html.Div(id='page-content'),
        html.H1(children='Travel Experts data'),
        html.Div(children=[
            'TravelExperts Booking details table with a bar chart of showing the sales per destination.'
        ]),
        html.Br(),
        # dash_table.DataTable(
        #     id='mytable',
        #     columns=[{"name": i, "id": i} for i in df.columns],
        #     data=df.to_dict('records'),
        #     page_action='native',
        #     page_size=10
        # ),
        html.Div(id='page-content2'),
    ]
)


@dash_app.callback(dash.dependencies.Output('page-content', 'children'),
                   [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    # We read the parameters passed by Node.js project from the URL
    if isinstance(pathname, str):
        pathname = pathname[1:].split('/')
        print(pathname, '\n')
        df_group_destination1 = df[df['Destination']
                                   == pathname[0]]
        fig = px.bar(df_group_destination1,
                     x=df_group_destination1.index, y="BasePrice")
        # pathname = ''
        return html.Div([
            # html.H3('You are on page {}'.format(pathname))
            dcc.Graph(figure=fig)
        ])


@dash_app.callback(dash.dependencies.Output('page-content2', 'children'),
                   [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if isinstance(pathname, str):
        pathname = pathname[1:].split('/')

        return html.Div([
            dash_table.DataTable(
                id='mytable',
                # [{"name": i, "id": i} for i in df.columns],
                columns=[{"name": "Description", "id": "Description"},
                         {"name": "BasePrice", "id": "BasePrice"}, ],
                data=df[["Description", "BasePrice"]].to_dict('records'),
                page_action='native',
                page_size=10
            ),
        ])


if __name__ == '__main__':
    dash_app.run_server(debug=True)
