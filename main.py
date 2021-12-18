# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
import pandas as pd
import dash_table
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from sqlalchemy.types import String
from fpdf import FPDF
import base64
import plotly.express as px
import plotly.graph_objects as go

server = Flask(__name__)
app = dash.Dash(
    __name__,server=server,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
        }
    ] , external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.config.suppress_callback_exceptions = True

encoded = base64.b64encode(open('kth.jpg', 'rb').read())

logo_img=html.Img(src='data:image/jpg;base64,{}'.format(encoded.decode()), id='logo_img', height='70vh',
                  style=dict(marginLeft='1vh'))

db_logo_img=dbc.Col([ logo_img] ,
        xs=dict(size=2,offset=0), sm=dict(size=2,offset=0),
        md=dict(size=1,offset=0), lg=dict(size=1,offset=0), xl=dict(size=1,offset=0))

header_text=html.Div('Transport Model For Simulating Urban Scenarios For Oslo City, Norway',style=dict(color='white',
                     fontWeight='bold',fontSize='2.8vh',marginTop='1vh',marginLeft='1.5vh'))
db_header_text=  dbc.Col([ header_text] ,
        xs=dict(size=10,offset=0), sm=dict(size=10,offset=0),
        md=dict(size=10,offset=0), lg=dict(size=10,offset=0), xl=dict(size=10,offset=0))



df=pd.read_csv('sample_map.csv')
df['lat']=df['location'].apply(lambda x:x.split(',')[0])
df['long']=df['location'].apply(lambda x:x.split(',')[1])

hov_text=[]
for ind in df.index:
    hov_text.append('City Name : {}<br>State Name : {}<br>Population : {}'.format(df['name_of_city'][ind],df['state_name'][ind],df['population_total'][ind]))

df['hover']=hov_text


locations = go.Scattermapbox(
    lon=df['long'],
    lat=df['lat'],
    mode='markers',
    marker={'color': 'red','size':10},
    unselected={'marker': {'opacity': 1}},
    selected={'marker': {'opacity': 0.5, 'size': 15}},
    hoverinfo='text',
    hovertext=df['hover'],
    customdata=df['state_name']
)

myfig=go.Figure(data=locations,layout= go.Layout(
            uirevision= 'foo', #preserves state of figure/map after callback activated
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            mapbox=dict(
                bearing=25,
                style='light',
                center=dict(
                    lon=88.4345078,
                    lat=22.9750855
                ),
                pitch=40,zoom=11.5
            ),margin = dict(l = 0, r = 0, t = 30, b = 0)
        ))
myfig.update_layout(mapbox_style="open-street-map")

map_div1=html.Div([
            dcc.Graph(id='map1', config={'displayModeBar': True, 'scrollZoom': True,'displaylogo': False},
                style={'height':'60vh'} ,figure=myfig
            ) ]
        )

db_map_div1=dbc.Col([ map_div1] ,
        xs=dict(size=10,offset=1), sm=dict(size=10,offset=1),
        md=dict(size=5,offset=1), lg=dict(size=5,offset=1), xl=dict(size=5,offset=1))

map_div2=html.Div([
            dcc.Graph(id='map2', config={'displayModeBar': True, 'scrollZoom': True,'displaylogo': False},
                style={'height':'60vh'} ,figure=myfig
            ) ]
        )

db_map_div2=dbc.Col([ map_div2] ,
        xs=dict(size=10,offset=1), sm=dict(size=10,offset=1),
        md=dict(size=5,offset=0), lg=dict(size=5,offset=0), xl=dict(size=5,offset=0))

navigation_header=dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Simulations", active='exact', href="/Simulations",id='Simulations',
                                style=dict(fontSize='1.8vh'))),
        dbc.NavItem(dbc.NavLink("Register", href="/Register",active='exact',id='Register',
                                style=dict(fontSize='1.8vh'))),
        dbc.NavItem(dbc.NavLink("About us", href="/About_us", active='exact', id='About_us',
                                style=dict(fontSize='1.8vh')))
    ],
    pills=True,
)
db_navigation_header=dbc.Col([navigation_header],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=12, offset=0), lg=dict(size=8, offset=0), xl=dict(size=8, offset=0)
                             )
map_header1=html.H1('Existing Transport Model (2019 flows)',
                           style=dict(fontSize='2.5vh',fontWeight='bold',color='#1e90ff'))
map_header2=html.H1('Simulated Transport Scenario',
                           style=dict(fontSize='2.5vh',fontWeight='bold',color='#1e90ff'))

db_map_header1=dbc.Col([map_header1],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=5, offset=1), lg=dict(size=5, offset=1), xl=dict(size=5, offset=1)
                             )

db_map_header2=dbc.Col([map_header2],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=5, offset=0), lg=dict(size=5, offset=0), xl=dict(size=5, offset=0)
                             )

simulation_type_text=html.H1('Type of Simulation For Visualization',
                           style=dict(fontSize='1.8vh',fontWeight='bold',color='black',marginTop='1vh'))

db_simulation_type_text=dbc.Col([simulation_type_text],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=2, offset=1), lg=dict(size=2, offset=1), xl=dict(size=2, offset=1)
                             )


simulation_type_menu=  dcc.Dropdown(
        id='sim_dropdown',
        options=[
            dict(label='Node-Node(Network)', value='Network'), dict(label='Zone-Zone(Flows)', value='Flows')
        ],
        value='Network' , style=dict(color='black',fontWeight='bold',textAlign='center')
    )
# height='50px' ,
# width='12%', marginLeft='1520px' marginTop='-400px' fontSize=26

simulation_type_menu_div= html.Div([simulation_type_menu],
                          style=dict( border='2px solid #082255',fontSize='2vh'))

db_simulation_type_menu=dbc.Col([simulation_type_menu_div],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=2, offset=0), lg=dict(size=2, offset=0), xl=dict(size=2, offset=0)
                             )

model_type_text=html.H1('Transport Model For Simulation',
                           style=dict(fontSize='2vh',fontWeight='bold',color='black',marginTop='1vh'))

db_model_type_text=dbc.Col([model_type_text],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=2, offset=0), lg=dict(size=2, offset=0), xl=dict(size=2, offset=0)
                             )
model_type_menu=  dcc.Dropdown(
        id='model_dropdown',
        options=[
            dict(label='Gravity Model(SIM)', value='SIM'), dict(label='Machine Learning(AI)', value='AI')
        ],
        value='SIM' , style=dict(color='black',fontWeight='bold',textAlign='center')
    )

model_type_menu_div= html.Div([model_type_menu],
                          style=dict( border='2px solid #082255',fontSize='2vh'))

db_model_type_menu=dbc.Col([model_type_menu_div],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=2, offset=0), lg=dict(size=2, offset=0), xl=dict(size=2, offset=0)
                             )



app.layout=html.Div([ dbc.Row([db_logo_img,db_header_text],style=dict(backgroundColor='#2358a6') ),
                      dbc.Row([db_navigation_header]),html.Br(),
                      dbc.Row([db_map_header1,db_map_header2]),
                      dbc.Row([db_map_div1,db_map_div2]),html.Br(),
                      dbc.Row([db_simulation_type_text,db_simulation_type_menu,
                               db_model_type_text,db_model_type_menu])




                      ,dcc.Location(id='url', refresh=True,pathname='/Simulations')




])

if __name__ == '__main__':
    app.run_server(port=8700,debug=False)