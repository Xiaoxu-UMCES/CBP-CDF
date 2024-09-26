#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 01:33:26 2024

@author: xiaoxug
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import TextBox
from scipy.spatial import distance
import netCDF4 as nc

# Load your data from CSV
data = pd.read_csv('Cell2LonLat.csv')

# Check if the necessary columns are present
if not all(col in data.columns for col in ['Latitude', 'Longitude', 'Cell_ID', 'Layer#']):
    raise ValueError("CSV file must contain 'Latitude', 'Longitude', 'Cell_ID', and 'Layer#' columns.")

x = data['Longitude']
y = data['Latitude']
cell_id = data['Cell_ID']
layer = data['Layer#']


# Compute the total number of layers at each (X, Y) coordinate
layer_counts = data.groupby(['Longitude', 'Latitude']).size()


# Load NetCDF file
nc_file = '/Users/xiaoxug/CBP-Decipher/netCDF_output/S.nc'
nc_data = nc.Dataset(nc_file, 'r')

# Global variables for selected point information
selected_x = None
selected_y = None
selected_layer = None
selected_cell_id = None

def get_nc_variable_info_at_point(x, y, layer, jday):
    info = ""
    
    for var_name in nc_data.variables:
            var = nc_data.variables[var_name]
            
            if len(var.dimensions) == 3:  # Assuming dimensions ('Cell_ID', 'Jday', 'Layer#')
                try:
                    # Access data using the indices
                    var_data = var[selected_cell_id,selected_layer,jday]
                    info += f"Variable: {var_name}\nData: {var_data}\n"
                except IndexError:
                    info += f"IndexError for variable: {var_name}\n"
            else:
                info += "Cell_ID or Layer# not found in NetCDF dimensions."
    
    return info

def get_nearest_points_within_layer(xy, current_layer, num_points=6):
    # Filter data to only include points from the same layer
    layer_data = data[data['Layer#'] == current_layer]
    
    # Extract coordinates for the current layer
    x_layer = layer_data['Longitude'].values
   
    y_layer = layer_data['Latitude'].values
   
    
    # Compute distances within the same layer
    points = np.column_stack((x_layer, y_layer))
    distances = distance.cdist([xy], points)[0]
    
    # Get indices of the nearest points within the layer
    nearest_indices = np.argsort(distances)[:num_points]
    return layer_data.iloc[nearest_indices]

def update_layer(layer_index):
    global sc, cbar

    # Clear the left panel and reinitialize
    ax_left.clear()

    # Filter data for the current layer
    layer_data = data[data['Layer#'] == layer_index]
   

    # Replot the scatter plot for the current layer
    sc = ax_left.scatter(layer_data['Longitude'], layer_data['Latitude'],
                         c=[layer_counts.get((xi, yi), 0) for xi, yi in zip(layer_data['Longitude'], layer_data['Latitude'])],
                         cmap='viridis', s=10, alpha=0.7)
    ax_left.set_xlabel('Longitude')
    ax_left.set_ylabel('Latitude')
    ax_left.set_title(f'Scatter Plot for Layer {layer_index}')

    # Create or update colorbar
    if cbar is None:
        cbar = plt.colorbar(sc, ax=ax_left)
        cbar.set_label('Total Number of Layers')
    else:
        cbar.update_normal(sc)

    # Update the info panel for the current layer
    info_panel.clear()
    info_panel.axis('off')

    fig.canvas.draw_idle()

def on_click(event):
    global selected_x, selected_y, selected_layer, selected_cell_id

    if event.inaxes == ax_left:
        # Find nearest point
        distances = np.sqrt((x - event.xdata) ** 2 + (y - event.ydata) ** 2)
        nearest_idx = distances.idxmin()
        
        # Get the information for the selected point
        selected_x = x.iloc[nearest_idx]
        selected_y = y.iloc[nearest_idx]
        selected_layer = layer.iloc[nearest_idx]
        selected_cell_id = cell_id.iloc[nearest_idx]

        # Filter the data for the selected (X, Y) point across all layers
        selected_data = data[(data['Longitude'] == selected_x) & (data['Latitude'] == selected_y)]
      
        # Get the nearest 6 points within the same layer as the selected point
        nearest_points = get_nearest_points_within_layer((selected_x, selected_y), selected_layer)
        
        # Display information on the right panel
        info_panel.clear()  # Clear previous information
        info_panel.text(0.05, 0.95, 'All Layers at Selected (Lon, Lat):', fontsize=12, weight='bold')

        # Adjust vertical spacing dynamically for the selected point information
        y_offset = 0.90
        for i, row in selected_data.iterrows():
            info_panel.text(0.05, y_offset, f'Layer: {row["Layer#"]}, Cell ID: {row["Cell_ID"]}', fontsize=10)
            y_offset -= 0.05
        
        # Column for nearest points information, adjusted for better spacing
        info_panel.text(0.55, 0.95, f'Nearest 6 Points in Layer {selected_layer}:', fontsize=12, weight='bold')  # Adjusted starting point
        y_offset = 0.90
        for i, row in nearest_points.iterrows():
            # Output all available information for each point
            info_panel.text(0.55, y_offset, f'X: {row["Longitude"]}, Y: {row["Latitude"]}, Layer: {row["Layer#"]}, Cell ID: {row["Cell_ID"]}', fontsize=10)
            y_offset -= 0.05
        
        # Prompt for Jday in the terminal and print NetCDF data
        try:
            jday = int(input("Enter day#: "))
            jday_dim_size = nc_data.dimensions['time'].size

            if jday < 0 or jday >= jday_dim_size:
                raise ValueError("Day# not found in NetCDF dimensions.")
            
            # Print NetCDF data for the selected point and nearest points to the terminal
            nc_info = get_nc_variable_info_at_point(selected_x, selected_y, selected_layer, jday)
            print(f'NetCDF Data for Point ({selected_x}, {selected_y})"/"({nc_info})')
        except ValueError as e:
            print(e)
        
        info_panel.set_xlim(0, 1)
        info_panel.set_ylim(0, 1)
        info_panel.axis('off')
        
        fig.canvas.draw_idle()

def submit_layer(text):
    try:
        layer_index = int(text)
        if layer_index in layer.unique():
            update_layer(layer_index)
        else:
            print(f"Layer {layer_index} not found.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

# Set up the figure and axes with better sizing
fig = plt.figure(figsize=(14, 8))  # Increased figure width for more right panel space
gs = fig.add_gridspec(2, 3, width_ratios=[4, 1, 2], height_ratios=[1, 4])  # Adjust grid for better spacing

ax_left = fig.add_subplot(gs[1, 0])
info_panel = fig.add_subplot(gs[1, 1:])
info_panel.axis('off')

# Create a text box for layer input
text_box_ax = plt.axes([0.35, 0.02, 0.15, 0.05])
text_box = TextBox(text_box_ax, 'Enter Layer: ')

# Initialize the colorbar
sc = None
cbar = None

# Connect the submit function to the text box
text_box.on_submit(submit_layer)

# Initialize with the first layer
update_layer(layer.unique()[0])

# Connect the click event
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()
