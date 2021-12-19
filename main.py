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

Urban_Districts = ['30101 Gamle Oslo','30102 Grünerløkka', '30103 Sagene','30104 St.Hanshaugen', '30105 Frogner','30106 Ullern', '30107 Vestre Aker','30108 Nordre Aker',
                   '30109 Bjerke','30110 Grorud', '30111 Stovner','30112 Alna', '30113 Østensjø','30114 Nordstrand',
                   '30115 Søndre Nordstrand','30116 Sentrum', '30117 Marka']






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
                           style=dict(fontSize='2.2vh',fontWeight='bold',color='black'))
map_header2=html.H1('Simulated Transport Scenario',
                           style=dict(fontSize='2.2vh',fontWeight='bold',color='black'))
##1e90ff
db_map_header1=dbc.Col([map_header1],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=5, offset=1), lg=dict(size=5, offset=1), xl=dict(size=5, offset=1)
                             )

db_map_header2=dbc.Col([map_header2],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=5, offset=0), lg=dict(size=5, offset=0), xl=dict(size=5, offset=0)
                             )

simulation_type_text=html.Div(html.H1('Type of Simulation For Visualization: ',
                           style=dict(fontSize='1.7vh',fontWeight='bold',color='black',marginTop='1vh')),
                           style=dict(display='inline-block'))

#db_simulation_type_text=dbc.Col([simulation_type_text],
                       #      xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                        #     md=dict(size=2, offset=1), lg=dict(size=2, offset=1), xl=dict(size=2, offset=1)
                         #    )


simulation_type_menu=  dcc.Dropdown(
        id='sim_dropdown',
        options=[
            dict(label='Node-Node(Network)', value='Network'), dict(label='Zone-Zone(Flows)', value='Flows')
        ],
        value='Network' , style=dict(color='black',fontWeight='bold',textAlign='center',width='15vh',backgroundColor='skyblue')
    )
# height='50px' ,
# width='12%', marginLeft='1520px' marginTop='-400px' fontSize=26

simulation_type_menu_div= html.Div([simulation_type_menu],
                          style=dict( display='inline-block',border='2px solid #082255',fontSize='1.7vh',
                                      marginLeft='2vh',marginBottom='-2vh'))

db_simulation_type_menu=dbc.Col([simulation_type_text,simulation_type_menu_div,html.Br(),html.Br()],
                             xs=dict(size=8, offset=2), sm=dict(size=8, offset=2),
                             md=dict(size=10, offset=1), lg=dict(size=4, offset=1), xl=dict(size=4, offset=1)
                             )

model_type_text=html.Div(html.H1('Transport Model Used For Simulation',
                           style=dict(fontSize='1.7vh',fontWeight='bold',color='black',marginTop='1vh')),
                         style=dict(display='inline-block'))

#db_model_type_text=dbc.Col([model_type_text],
                        #     xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                          #   md=dict(size=2, offset=0), lg=dict(size=2, offset=0), xl=dict(size=2, offset=0)
                          #   )
model_type_menu=  dcc.Dropdown(
        id='model_dropdown',
        options=[
            dict(label='Gravity Model(SIM)', value='SIM'), dict(label='Machine Learning(AI)', value='AI')
        ],
        value='SIM' , style=dict(color='black',fontWeight='bold',textAlign='center',width='15vh',backgroundColor='skyblue')
    )

model_type_menu_div= html.Div([model_type_menu],
                          style=dict( display='inline-block',border='2px solid #082255',fontSize='1.7vh',
                                      marginLeft='2vh',marginBottom='-2vh'))

db_model_type_menu=dbc.Col([model_type_text,model_type_menu_div,html.Br(),html.Br()],
                             xs=dict(size=8, offset=2), sm=dict(size=8, offset=2),
                             md=dict(size=10, offset=1), lg=dict(size=4, offset=0), xl=dict(size=4, offset=0)
                             )



city_text=html.Div(html.H1('City Subdivisons',
                           style=dict(fontSize='1.7vh',fontWeight='bold',color='black',marginTop='1vh')),
                         style=dict(display='inline-block'))

#db_model_type_text=dbc.Col([model_type_text],
                        #     xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                          #   md=dict(size=2, offset=0), lg=dict(size=2, offset=0), xl=dict(size=2, offset=0)
                          #   )
city_menu=  dcc.Dropdown(
        id='city_dropdown',
        options=[
            dict(label='Urban Districts', value='Urban'), dict(label='Grunnkrets', value='Grunnkrets')
        ],
        value='Urban' , style=dict(color='black',fontWeight='bold',textAlign='center',width='15vh',backgroundColor='skyblue')
    )

city_menu_div= html.Div([city_menu],
                          style=dict( display='inline-block',border='2px solid #082255',fontSize='1.7vh',
                                      marginLeft='2vh',marginBottom='-2vh'))

db_city_menu=dbc.Col([city_text,city_menu_div],
                             xs=dict(size=8, offset=2), sm=dict(size=8, offset=2),
                             md=dict(size=10, offset=1), lg=dict(size=3, offset=0), xl=dict(size=3, offset=0)
                             )


scenario_header=html.H1('Oslo City Transport Simulation',
                           style=dict(fontSize='2vh',fontWeight='bold',color='black'))


db_scenario_header=dbc.Col([scenario_header],
                             xs=dict(size=8, offset=2), sm=dict(size=8, offset=2),
                             md=dict(size=8, offset=1), lg=dict(size=8, offset=1), xl=dict(size=8, offset=1)
                             )

navigation_header2=dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Scenario Selection", active='exact', href="/Scenario",id='Scenario',
                                style=dict(fontSize='1.8vh'))),
        dbc.NavItem(dbc.NavLink("Infographics", href="/Infographics",active='exact',id='Infographics',
                                style=dict(fontSize='1.8vh'))),
        dbc.NavItem(dbc.NavLink("Model Analysis", href="/Analysis", active='exact', id='Analysis',
                                style=dict(fontSize='1.8vh'))),
        dbc.NavItem(dbc.NavLink("Report", href="/Report", active='exact', id='Report',
                                style=dict(fontSize='1.8vh')))
    ],
    pills=True,
)



db_navigation_header2=dbc.Col([navigation_header2],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=10, offset=1), lg=dict(size=10, offset=1), xl=dict(size=10, offset=1)
                             )


scenario_selection_text=html.Div(html.H1('Select the Scenario Parameter for Simulation: ',
                           style=dict(fontSize='1.7vh',fontWeight='bold',color='black',marginTop='1vh')),
                           style=dict(display='inline-block'))



scenario_selection_menu=  dcc.Dropdown(
        id='scenario_dropdown',
        options=[
            dict(label='Population (residential)', value='Population'), dict(label='Employment (Jobs)', value='Employment'),
            dict(label='Cost of transport', value='Cost'), dict(label='Income-levels', value='Income'),
            dict(label='Literacy-levels', value='Literacy'), dict(label='Built-Area', value='Area'),
            dict(label='Urbanisation (Developed Area)', value='Urbanisation')

        ],
        value='Population' , style=dict(color='black',fontWeight='bold',textAlign='center',width='15vh',backgroundColor='skyblue')
    )


scenario_selection_menu_div= html.Div([scenario_selection_menu],
                          style=dict( display='inline-block',border='2px solid #082255',fontSize='1.7vh',
                                      marginLeft='2vh',marginBottom='-2vh'))

db_scenario_selection_menu=dbc.Col([scenario_selection_text,scenario_selection_menu_div,html.Br(),html.Br()],
                             xs=dict(size=8, offset=2), sm=dict(size=8, offset=2),
                             md=dict(size=10, offset=1), lg=dict(size=4, offset=1), xl=dict(size=4, offset=1)
                             )



subdivision_text=html.Div(html.H1('Select Subdivision: ',
                           style=dict(fontSize='1.7vh',fontWeight='bold',color='black',marginTop='1vh')),
                           style=dict(display='inline-block'))



subdivision_menu=  dcc.Dropdown(
        id='subdivision_dropdown',
        options=[{ 'label':x ,'value':x } for x in Urban_Districts],
        value='30101 Gamle Oslo' , style=dict(color='black',fontWeight='bold',textAlign='center',width='15vh',backgroundColor='skyblue')
    )


subdivision_menu_div= html.Div([subdivision_menu],
                          style=dict( display='inline-block',border='2px solid #082255',fontSize='1.7vh',
                                      marginLeft='2vh',marginBottom='-2vh'))

db_subdivision_menu=dbc.Col([subdivision_text,subdivision_menu_div,html.Br(),html.Br()],
                             xs=dict(size=8, offset=2), sm=dict(size=8, offset=2),
                             md=dict(size=10, offset=1), lg=dict(size=4, offset=0), xl=dict(size=4, offset=0)
                             )


app.layout=html.Div([ dbc.Row([db_logo_img,db_header_text],style=dict(backgroundColor='#2358a6') ),
                      dbc.Row([db_navigation_header]),html.Br(),
                      dbc.Row([db_map_header1,db_map_header2]),
                      dbc.Row([db_map_div1,db_map_div2]),html.Br(),
                      dbc.Row([db_simulation_type_menu,db_model_type_menu,db_city_menu]),html.Br(),
                      dbc.Row([db_scenario_header]),html.Br(),
                      dbc.Row([db_navigation_header2]),html.Br(),
                      dbc.Row([db_scenario_selection_menu,db_subdivision_menu])







                      ,dcc.Location(id='url', refresh=True,pathname='/Simulations')




])

if __name__ == '__main__':
    app.run_server(port=8700,debug=False)