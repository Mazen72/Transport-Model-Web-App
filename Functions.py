import pandas as pd
import plotly.graph_objects as go

def create_line_map1(df):
    hov_text = []
    for ind in df.index:
        hov_text.append('Origin : {}<br>Destination : {}<br>Trips : {}<br>Population : {}'.format(df['Origin'][ind],
                                                                                                  df['Destination'][
                                                                                                      ind],
                                                                                                  df['Trips'][ind],
                                                                                                  df['OriPop19'][ind]))
    df['hover'] = hov_text

    fig = go.Figure()

    name_arr = []
    for i in range(len(df)):
        if df['Origin'][i] == df['Destination'][i]:
            continue

        current_dist = df['Destination'][i]
        current_origin = df['Origin'][i]
        trips = df['Trips'][i]
        trips_reversed = df[(df['Origin'] == current_dist) & (df['Destination'] == current_origin)]['Trips'].values[0]
        total_trips = trips + trips_reversed

        if total_trips > 15000:
            color = 'red'
            name = '> 15000 Trips'

        elif total_trips <= 15000:
            color = 'black'
            name = '<= 15000 Trips'

        legend = True
        if name in name_arr:
            legend = False
        else:
            legend = True

        fig.add_trace(go.Scattermapbox(name=name, showlegend=legend,
                                       lon=[df['lon-origin'][i], df['lon-dist'][i]],
                                       lat=[df['lat-origin'][i], df['lat-dist'][i]],
                                       mode='lines',
                                       marker={'color': color, 'size': 10, 'allowoverlap': True, 'opacity': 0.1},
                                       # unselected={'marker': {'opacity': 1}},
                                       # selected={'marker': {'opacity': 0.5, 'size': 15}},
                                       hoverinfo='text',
                                       hovertext=['Subdivision : {}<br>Population : {}'.format(df['Origin'][i],
                                                                                               df['OriPop19'][i]),
                                                  'Subdivision : {}<br>Population : {}'.format(df['Destination'][i],
                                                                                               df['OriPop19'][i])],
                                       customdata=[df['Origin'][i], df['Destination'][i]]
                                       )
                      )
        name_arr.append(name)

    fig.update_layout(
        uirevision='foo',  # preserves state of figure/map after callback activated
        clickmode='event+select',
        hovermode='closest',
        hoverdistance=2,
        mapbox=dict(
            #      bearing=25,
            style='light',
            center=dict(
                lon=10.7347673396536,
                lat=59.8992367
            ),
            #   pitch=40,
            zoom=10
        ), margin=dict(l=0, r=0, t=30, b=0), hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell")
    )
    fig.update_layout(mapbox_style='open-street-map')
    return fig

def create_size_map1(df):
    dist_df = df.groupby(['Destination', 'lon-dist', 'lat-dist'])['Trips'].sum()
    dist_df = dist_df.reset_index()
    org_df = df.groupby(['Origin', 'lon-origin', 'lat-origin'])['Trips'].sum()
    org_df = org_df.reset_index()
    inter_df = pd.DataFrame()
    for index, row in df.iterrows():
        if row['Origin'] == row['Destination']:
            inter_df = inter_df.append(row[['Origin', 'Destination', 'Trips']], ignore_index=True)

    inter_df = inter_df.sort_values('Origin', ignore_index=True)
    dist_df['dest._Trips'] = dist_df['Trips'] - inter_df['Trips']
    dist_df['orig._Trips'] = org_df['Trips'] - inter_df['Trips']
    dist_df['inter._Trips'] = inter_df['Trips']
    dist_df['Trips_Total'] = dist_df['dest._Trips'] + dist_df['orig._Trips'] + dist_df['inter._Trips']
    dist_df = dist_df.astype({"dest._Trips": int, "orig._Trips": int, "inter._Trips": int, "Trips_Total": int})

    hov_text = []
    for ind in dist_df.index:
        hov_text.append(
            'Subdivision : {}<br>Incoming Trips : {}<br>Outgoing Trips : {}<br>Intra.Trips : {}<br>Total Trips : {}'.format(
                dist_df['Destination'][ind], dist_df['orig._Trips'][ind],
                dist_df['dest._Trips'][ind], dist_df['inter._Trips'][ind], dist_df['Trips_Total'][ind]))

    dist_df['hover'] = hov_text

    fig2 = go.Figure(go.Scattermapbox(lat=dist_df['lat-dist'], lon=dist_df['lon-dist'],below="\"\"\"",
                                      marker=dict(
                                          size=dist_df['Trips_Total'] / 1000,
                                          color='rgb(0,0,255)',
                                          sizemode='area'
                                      ),
                                      hoverinfo='text', hovertemplate=dist_df['hover'], customdata=dist_df['hover']))

    fig2.update_layout(mapbox_style='open-street-map', mapbox_center_lon=10.7347673396536, mapbox_center_lat=59.8992367,
                       mapbox_zoom=10)
    fig2.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0}, hoverdistance=2, uirevision='foo',
                       clickmode='event+select', hovermode='closest')
    return fig2

def create_combined_map(df):


    fig = go.Figure()

    for i in range(len(df)):
        if df['Origin'][i] == df['Destination'][i]:
            continue

        fig.add_trace(go.Scattermapbox(
            lon=[df['lon-origin'][i], df['lon-dist'][i]],
            lat=[df['lat-origin'][i], df['lat-dist'][i]],
            mode='lines',
            marker={'color': 'rgb(0,0,255)', 'size': 10, 'allowoverlap': True,'opacity':0.1},
           # unselected={'marker': {'opacity': 1}},
           # selected={'marker': {'opacity': 0.5, 'size': 15}},
            hoverinfo='skip',
         #   hovertext=['Subdivision : {}<br>Population : {}'.format(df['Origin'][i], df['OriPop19'][i]),
              #         'Subdivision : {}<br>Population : {}'.format(df['Destination'][i], df['OriPop19'][i])],
            customdata=[df['Origin'][i], df['Destination'][i]]
        )
        )

    fig.update_layout(
        uirevision='foo',  # preserves state of figure/map after callback activated
        clickmode='event+select',
        hovermode='closest',
        hoverdistance=2,
        mapbox=dict(
         #   bearing=25,
            style='light',
            center=dict(
                lon=10.7347673396536,
                lat=59.8992367
            ),
          #  pitch=40,
            zoom=10
        ), showlegend=False, margin=dict(l=0, r=0, t=30, b=0) ,hoverlabel=dict(
        font_size=16,
        font_family="Rockwell")
    )
    fig.update_layout(mapbox_style='open-street-map')

    dist_df = df.groupby(['Destination', 'lon-dist', 'lat-dist'])['Trips'].sum()
    dist_df = dist_df.reset_index()
    org_df = df.groupby(['Origin', 'lon-origin', 'lat-origin'])['Trips'].sum()
    org_df = org_df.reset_index()
    inter_df = pd.DataFrame()
    for index, row in df.iterrows():
        if row['Origin'] == row['Destination']:
            inter_df = inter_df.append(row[['Origin', 'Destination', 'Trips']], ignore_index=True)

    inter_df = inter_df.sort_values('Origin', ignore_index=True)
    dist_df['dest._Trips'] = dist_df['Trips'] - inter_df['Trips']
    dist_df['orig._Trips'] = org_df['Trips'] - inter_df['Trips']
    dist_df['inter._Trips'] = inter_df['Trips']
    dist_df['Trips_Total'] = dist_df['dest._Trips'] + dist_df['orig._Trips'] + dist_df['inter._Trips']
    dist_df = dist_df.astype({"dest._Trips": int, "orig._Trips": int, "inter._Trips": int, "Trips_Total": int})

    hov_text = []
    for ind in dist_df.index:
        hov_text.append(
            'Subdivision : {}<br>Incoming Trips : {}<br>Outgoing Trips : {}<br>Intra.Trips : {}<br>Total Trips : {}'.format(
                dist_df['Destination'][ind], dist_df['orig._Trips'][ind],
                dist_df['dest._Trips'][ind], dist_df['inter._Trips'][ind], dist_df['Trips_Total'][ind]))

    dist_df['hover2'] = hov_text

    fig.add_trace(go.Scattermapbox(lat=dist_df['lat-dist'], lon=dist_df['lon-dist'],
                                      marker=dict(
                                          size=dist_df['Trips_Total'] / 500,
                                          color='rgb(0,0,255)',
                                          sizemode='area',opacity=1
                                      ),
                                      hoverinfo='text', hovertemplate=dist_df['hover2'], customdata=dist_df['hover2']))


    return fig
