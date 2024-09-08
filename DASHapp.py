import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import geopandas as gpd
import pandas as pd

# Load shapefiles into GeoDataFrames
shapefile_paths = [path1, path2]

dataframes = [gpd.read_file(shapefile) for shapefile in shapefile_paths]

# Create a Dash app
app = dash.Dash(__name__)

# Prepare initial figures
figures = []
for gdf in dataframes:
    fig = px.choropleth_mapbox(gdf,
                              geojson=gdf.geometry.__geo_interface__,
                              locations=gdf.index,
                              featureidkey="properties.index",
                              color=gdf.columns[0],
                              color_continuous_scale="Viridis",
                              mapbox_style="carto-positron",
                              center={"lat": 20.5937, "lon": 78.9629},
                              zoom=3)
    figures.append(fig)

# App layout
app.layout = html.Div([
    dcc.Checklist(
        id='layer-checklist',
        options=[
            {'label': 'Indian States', 'value': '0'},
            {'label': 'Districts', 'value': '1'}
        ],
        value=['0', '1'],
        inline=True
    ),
    dcc.Dropdown(
        id='attribute-dropdown',
        options=[{'label': col, 'value': col} for col in dataframes[0].columns] + 
                [{'label': col, 'value': col} for col in dataframes[1].columns],
        value=dataframes[0].columns[0]  # Default value
    ),
    dcc.Graph(id='map')
])

# Callback to update the map based on layer selection and attribute
@app.callback(
    Output('map', 'figure'),
    [Input('layer-checklist', 'value'),
     Input('attribute-dropdown', 'value')]
)
def update_map(selected_layers, selected_attribute):
    fig = px.choropleth_mapbox(dataframes[int(selected_layers[0])],
                              geojson=dataframes[int(selected_layers[0])].geometry.__geo_interface__,
                              locations=dataframes[int(selected_layers[0])].index,
                              featureidkey="properties.index",
                              color=selected_attribute,
                              color_continuous_scale="Viridis",
                              mapbox_style="carto-positron",
                              center={"lat": 20.5937, "lon": 78.9629},
                              zoom=3)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
