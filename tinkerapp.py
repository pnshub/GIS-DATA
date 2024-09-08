import tkinter as tk
from tkinter import ttk
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors

# Load shapefiles into GeoDataFrames
shapefile_paths = [file path1, file path2]
dataframes = [gpd.read_file(shapefile) for shapefile in shapefile_paths]

# Create the main Tkinter window
root = tk.Tk()
root.title("Map Visualization")

# Create a frame for the map
frame_map = tk.Frame(root)
frame_map.pack(fill=tk.BOTH, expand=True)

# Create a frame for the controls
frame_controls = tk.Frame(root)
frame_controls.pack(fill=tk.X)

# Global canvas variable
canvas = None

def plot_map():
    global canvas
    fig, ax = plt.subplots(figsize=(8, 8))

    # Clear previous plot
    ax.clear()

    # Get selected layers
    selected_layers = [var.get() for var in layer_vars if var.get() is not None]

    # Plot each selected layer
    for i, gdf in enumerate(dataframes):
        if str(i) in selected_layers:
            # Plot each GeoDataFrame
            gdf.plot(ax=ax, edgecolor='k', alpha=0.5)
            # Use a unique identifier for each shape
            for idx, row in gdf.iterrows():
                ax.annotate(row.name, xy=(row.geometry.centroid.x, row.geometry.centroid.y), 
                            xytext=(3, 3), textcoords="offset points", fontsize=8)

    plt.title(f"Map with Attribute: {attribute_var.get()}")
    plt.tight_layout()

    # Clear the previous canvas and draw the new plot
    if canvas is not None:
        canvas.get_tk_widget().pack_forget()

    canvas = FigureCanvasTkAgg(fig, master=frame_map)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Enable hover functionality with metadata display
    mplcursors.cursor(ax, hover=True).connect(
        "add", lambda sel: sel.annotation.set_text(
            f'{attribute_var.get()}: {sel.target[0]}'
        )
    )

# Checkbox for layer visibility
layer_vars = []
for i, label in enumerate(["Indian States", "Districts"]):
    var = tk.StringVar(value=str(i))
    cb = ttk.Checkbutton(frame_controls, text=label, variable=var, command=plot_map)
    cb.pack(side=tk.LEFT)
    layer_vars.append(var)

# Dropdown for attribute selection
attribute_var = tk.StringVar(value=dataframes[0].columns[0])
attribute_dropdown = ttk.Combobox(frame_controls, textvariable=attribute_var)
attribute_dropdown['values'] = list(dataframes[0].columns) + list(dataframes[1].columns)
attribute_dropdown.bind("<<ComboboxSelected>>", lambda event: plot_map())
attribute_dropdown.pack(side=tk.LEFT)

# Plot initial map
plot_map()

# Start the Tkinter main loop
root.mainloop()
