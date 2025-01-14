import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# Dynamically set the file path to the same directory as the script
current_dir = os.path.dirname(os.path.abspath(__file__))

def get_data(data_path, skiprows=None):
    """
    Reads a CSV file and returns its contents as a DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The contents of the CSV file as a DataFrame.
    """
    try:
        if skiprows:
            data = pd.read_csv(data_path, skiprows=skiprows)
        else:
            data = pd.read_csv(data_path)
        return data
    except FileNotFoundError:
        print(f"ERROR -  The file '{data_path}' does not exist.")
    except Exception as e:
        print(f"The followingg error occurred: {e}")

"""
# - EXERCISE 2 - #
Create an improved version of the “bad/manipulative” visualization.
"""
# Import dataset 
data_path = os.path.join(current_dir, "datasets", "energy-consumption-by-source-and-country.csv")
df = get_data(data_path)

# Print Check
# print(df.columns)
# print(df.head(5))

# Check for NaN values
# NaN_values = df.isna().sum().sum()
# print(f"The number of NaN values is {NaN_values}")

# Drop useless column 
df_filtered= df.iloc[:, :12].drop(df.columns[[0, 1]], axis=1)

# Print check 
# print(energy_data_filtered.head(5))

# Define consistent color mapping for each energy source
color_mapping = {
    'Biofuels consumption - TWh': '#FDB813',  # yellow-orange
    'Coal consumption - TWh': '#E6550D',      # dark orange
    'Gas consumption - TWh': '#FD8D3C',       # light orange
    'Hydro consumption - TWh': '#9ECAE1',     # light blue
    'Nuclear consumption - TWh': '#3182BD',   # medium blue
    'Oil consumption - TWh': '#6BAED6',       # teal
    'Solar consumption - TWh': '#31A354',     # green
    'Wind consumption - TWh': '#74C476',      # light green
    'Other renewables (including geothermal and biomass) - TWh': '#D9D9D9'  # grey
}

# Identify minor energy sources
minor_sources = ['Solar consumption - TWh', 'Wind consumption - TWh',
                 'Biofuels consumption - TWh', 'Other renewables (including geothermal and biomass) - TWh']

# Major energy sources (excluding minor sources)
major_sources = [col for col in df_filtered.columns[1:] if col not in minor_sources]

# Set the first column as the 'Year' column
df_filtered.columns = ['Year'] + list(df_filtered.columns[1:])
df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')

# NOTE: The following lines has been done by an exstensive use of ChatGPT.
# Plot 1: Full Energy Consumption by Major Sources
fig_major = px.area(
    df_filtered,
    x='Year',
    y=df_filtered.columns,
    title="<b>Global Energy Consumption by Major Sources (1965-2014)</b>",
    labels={'value': 'Percentage of Energy Consumption', 'Year': 'Year'},
    color_discrete_map=color_mapping
)

fig_major.update_layout(
    yaxis_title='Percentage of Energy Consumption (%)',
    xaxis_title='Year',
    yaxis_range=[0, 100],
    title_font=dict(size=24, family='Arial Black'),
    font=dict(size=14, family='Arial'),
    legend=dict(
        title='Energy Source',
        orientation='v',
        x=1.05,
        y=0.95,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='Black',
        borderwidth=1,
        font=dict(size=12)
    ),
    plot_bgcolor='white',
    margin=dict(l=50, r=150, t=80, b=50)
)

fig_major.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgrey', tickangle=45, ticks='outside')
fig_major.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgrey')

# data_path = os.path.join(current_dir, "figures", "figure2.html")
# fig_major.write_html(data_path)
fig_major.show()

# Plot 2: Energy Consumption by Minor Sources
fig_minor = px.area(
    df_filtered,
    x='Year',
    y=minor_sources,
    title="<b>Global Energy Consumption by Minor Sources (1965-2014)</b>",
    labels={'value': 'Percentage of Energy Consumption', 'Year': 'Year'},
    color_discrete_map=color_mapping
)

fig_minor.update_layout(
    yaxis_title='Percentage of Energy Consumption (%)',
    xaxis_title='Year',
    yaxis_range=[0, 10],  # Zoom in for better visibility
    title_font=dict(size=24, family='Arial Black'),
    font=dict(size=14, family='Arial'),
    legend=dict(
        title='Energy Source',
        orientation='v',
        x=1.05,
        y=0.95,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='Black',
        borderwidth=1,
        font=dict(size=12)
    ),
    plot_bgcolor='white',
    margin=dict(l=50, r=150, t=80, b=50)
)

fig_minor.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgrey', tickangle=45, ticks='outside')
fig_minor.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgrey')

# data_path = os.path.join(current_dir, "figures", "figure3.html")
# fig_minor.write_html(data_path)
fig_minor.show()
# - CHATGPT CODE ENDS HERE - #

"""
# - EXERCISE 4/5 - #

Create a viz about climate change for use in social media and write a hypothetical LinkedIn
post to accompany this viz.

Create a black-and-white visualization (no grey levels)
"""
# Import dataset 
data_path = os.path.join(current_dir, "datasets", "Indicator_3_1_Climate_Indicators_Annual_Mean_Global_Surface_Temperature_577579683071085080.csv")
df = get_data(data_path)

# Print Check
# print(df.columns)
# print(df.head(5))

# Filter for the 'World' series
df_world = df[df['Country'] == 'World']

# Keep only the 'Country' column and all number columns (years)
year_columns = [col for col in df_world.columns if col.isdigit()]
final_df = df_world[['Country'] + year_columns]

# Check for NaN values
# NaN_values = final_df.isna().sum().sum()
# print(f"The number of NaN values is {NaN_values}")

# Convert year columns to integers for proper plotting
year_columns_int = [int(year) for year in year_columns]
temperature_values = final_df.iloc[0, 1:].values  # Exclude 'Country' column

# NOTE: The following lines has been done by an exstensive use of ChatGPT.
# Create a black and white line chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=year_columns_int,
    y=temperature_values,
    mode='lines',
    line=dict(color='black')
))

fig.update_layout(
    title='Global Surface Temperature Change Over Time (Measured in °C)',
    xaxis_title='Year',
    yaxis_title='Temperature Change (°C)',
    template='plotly_white',
    xaxis=dict(tickmode='linear', dtick=5),  # Better scale on x-axis with 5-year intervals
    yaxis=dict(tickformat=".2f")             # Format y-axis for two decimal points
)
#Specify the path to save the figure
# data_path = os.path.join(current_dir, "figures", "figure4.html")
# fig.write_html(data_path)
fig.show()
# - CHATGPT CODE ENDS HERE - #

"""
# - EXERCISE 6 - #

Create a visualization that uses color as an important aesthetics
"""
# Filter to keep only 'Country' and year columns
year_columns = [col for col in df.columns if col.isdigit()]
filtered_df = df[['Country'] + year_columns]

# Remove the 'World' observation
filtered_df = filtered_df[filtered_df['Country'] != 'World']

# Print Check
#print(filtered_df.head(5))

# Melt the DataFrame to long format for the map
melted_df = filtered_df.melt(id_vars='Country', var_name='Year', value_name='TemperatureChange')

# NOTE: The following lines has been done by an exstensive use of ChatGPT.
# Create the choropleth map with an improved color scale
fig = px.choropleth(
    melted_df,
    locations="Country",
    locationmode="country names",
    color="TemperatureChange",
    hover_name="Country",
    animation_frame="Year",
    color_continuous_scale="YlOrRd",  # Yellow to Red for better contrast
    title="Global Temperature Change Over Time by Country (°C)"
)

# Update layout for better appearance
fig.update_layout(
    geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
    coloraxis_colorbar=dict(title="Temperature Change (°C)")
)

#Specify the path to save the figure
# data_path = os.path.join(current_dir, "figures", "figure6.html")
# fig.write_html(data_path)
fig.show()
# - CHATGPT CODE ENDS HERE - #

"""
# - EXERCISE 7 - #

Create a visualization that rigorously maximizes Tufte’s "data-ink ratio"
"""
# Import dataset 
data_path = os.path.join(current_dir, "datasets", "API_EG.FEC.RNEW.ZS_DS2_en_csv_v2_3673.csv")
df = get_data(data_path, skiprows=4) # Skip first 4 rows that contains metadata

# Print Check
# print(df.columns)
# print(df.head(5))
# print('\n \n')

# Filter for the 'World' observation and data from 1990 onwards
world_data = df[df['Country Name'] == 'World']
world_data = world_data[['Country Name'] + [str(year) for year in range(1990, 2024)]]

# Convert the DataFrame to long format for plotting
melted_df = world_data.melt(id_vars='Country Name', var_name='Year', value_name='Value')
melted_df['Year'] = melted_df['Year'].astype(int)

# Drop missing values
melted_df.dropna(inplace=True)

# Identify the year with the highest value and highlight it
max_value = melted_df['Value'].max()
max_value_year = melted_df[melted_df['Value'] == max_value]['Year'].values[0]
melted_df['Color'] = melted_df['Year'].apply(lambda x: 'red' if x == max_value_year else 'black')

# NOTE: The following lines has been done by an exstensive use of ChatGPT.
# Create the bar chart
fig = px.bar(
    melted_df,
    x='Year',
    y='Value',
    color='Color',
    color_discrete_map={'black': 'black', 'red': 'red'},
    title='Global Renewable Energy Consumption (1990 Onwards)',
    labels={'Value': 'Renewable Energy Consumption (%)'}
)

# Add annotation to highlight the maximum bar's value in red on the y-axis
fig.add_annotation(
    x=max_value_year,
    y=max_value,
    text=f"{max_value:.2f}%",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color="red", size=12),
    arrowcolor="red"
)

# Maximize data-ink ratio
fig.update_layout(
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False, linecolor='black', ticks='outside'),
    yaxis=dict(showgrid=False, zeroline=False, linecolor='black', ticks='outside'),
    margin=dict(l=20, r=20, t=40, b=20)
)

# Simplify bar appearance
fig.update_traces(marker=dict(opacity=0.9))

#Specify the path to save the figure
# data_path = os.path.join(current_dir, "figures", "figure7.html")
# fig.write_html(data_path)
fig.show()
# - CHATGPT CODE ENDS HERE - #


"""
# - EXERCISE 8/10 - # 

8.Create a visualization that is none of the following: map, bar chart, scatter plot, pie chart,
doughnut chart, line chart, box plot, density plot, histogram

10. Create one visualization with ChatGPT Pro / Microsoft Copilot (or any similar tool). Include
the visualization as you download it from the AI assistant without any further processing /
improving it. Document your conversation (screenshots!) in the appendix.
"""
# NOTE: The following lines has been done by an exstensive use of ChatGPT.
# Import dataset
data_path = os.path.join(current_dir, "datasets", "willingness-climate-action.csv")
df = get_data(data_path)

# Print Check
# print(df.columns)
# print(df.head(5))
# print('\n \n')

# Filter out rows with missing values
df_cleaned = df.dropna()

# Create the violin plot
fig = px.violin(df_cleaned, 
                x='World regions according to OWID', 
                y='Willingness to give 1% of income', 
                box=True, 
                points="all",
                title="Distribution of Willingness to Give 1% of Income to Combat Climate Change by Region",
                labels={"Willingness to give 1% of income": "Willingness to Give 1% of Income", 
                        "World regions according to OWID": "Region"})

# Show the plot
fig.show()
# - CHATGPT CODE ENDS HERE - #

#Specify the path to save the figure
# data_path = os.path.join(current_dir, "figures", "figure8.html")
# fig.write_html(data_path)


"""
# - EXERCISE 11 - # 

Create one data map
"""
# Import dataset 
data_path = os.path.join(current_dir, "datasets", "pm25-air-pollution.csv")
df = get_data(data_path)

# Print Check
print(df.columns)
print(df.head(5))
print('\n \n')

# Identify the latest year in the dataset
latest_year = df['Year'].max()

# Filter the DataFrame to include only rows from the latest year
latest_year_df = df[df['Year'] == latest_year]

# NOTE: The following lines has been done by an exstensive use of ChatGPT.
# Corrected column name in the 'color' parameter
fig = px.choropleth(
    latest_year_df,
    locations="Entity",               # Country names
    locationmode="country names",     # Matches with country names
    color="Concentrations of fine particulate matter (PM2.5) - Residence area type: Total",  # Correct column name
    hover_name="Entity",              # Tooltip will display country name
    color_continuous_scale="YlOrRd", # Yellow to Red color scale for intensity
    title="Global PM2.5 Air Pollution Over Time by Country (μg/m³) - 2019"
)

# Update the layout for a cleaner appearance
fig.update_layout(
    geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
    coloraxis_colorbar=dict(title="PM2.5 Concentration (μg/m³)")
)

fig.show()
# - CHATGPT CODE ENDS HERE - #

#Specify the path to save the figure
data_path = os.path.join(current_dir, "figures", "figure11.html")
fig.write_html(data_path)