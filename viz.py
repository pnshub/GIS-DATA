import geopandas as gpd
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import GeoJSONDataSource, HoverTool, CheckboxGroup, CustomJS, Select
from bokeh.layouts import column
import pandas as pd

# Paths to your shapefiles
shapefile_paths = [r"C:\Users\pkumar105\Downloads\archive (1)\Indian_States.shp", r"C:\Users\pkumar105\Downloads\archive\output.shp"]

# Load shapefiles into GeoDataFrames
dataframes = [gpd.read_file(shapefile) for shapefile in shapefile_paths]

# Create a Bokeh figure
p = figure(title="Multiple Layers Visualization with Attributes", height=800, width=800)

# Define colors for different layers
colors = ['blue', 'green']
layers = []

# Define attributes for each layer
attributes_list = [['st_nm'], ['statename', 'distname']]  # Replace with actual attribute names

# Add patches for each layer
for i, (gdf, color) in enumerate(zip(dataframes, colors)):
    geojson = gdf.to_json()
    geo_source = GeoJSONDataSource(geojson=geojson)
    
    # Add layer to the plot
    patch = p.patches('xs', 'ys', source=geo_source, fill_color=color, line_color='white', fill_alpha=0.6, name=f'layer_{i}')
    layers.append(patch)

# Create a HoverTool with a placeholder tooltip
hover = HoverTool()
hover.tooltips = [('', '')]  # Placeholder tooltips
p.add_tools(hover)

# Create a CheckboxGroup widget for layer visibility
checkbox = CheckboxGroup(labels=["Indian States", "Districts"], active=[0, 1])

# Create a Select widget for filtering
attributes_0 = dataframes[0].columns.tolist()
attributes_1 = dataframes[1].columns.tolist()
select = Select(title="Attribute:", options=attributes_0 + attributes_1)

# Create a CustomJS callback to filter data based on dropdown selection
callback = CustomJS(args=dict(layers=layers, checkbox=checkbox, hover=hover, select=select), code="""
    var active = checkbox.active;
    var attribute = select.value;
    
    // Update visibility of layers
    for (var i = 0; i < layers.length; i++) {
        layers[i].visible = active.includes(i);
    }
    
    // Update tooltips based on active layer
    var tooltips = [];
    var activeLayer = active.length > 0 ? active[0] : null;  // Assume single active layer for simplicity
    
    if (activeLayer !== null) {
        tooltips.push([attribute, '@{' + attribute + '}']);
    }
    
    hover.tooltips = tooltips;
""")

# Add the callback to the CheckboxGroup and Select widget
checkbox.js_on_change('active', callback)
select.js_on_change('value', callback)

# Layout the figure, checkbox, and dropdown
layout = column(p, checkbox, select)

# Show plot in notebook
output_notebook()
show(layout)
