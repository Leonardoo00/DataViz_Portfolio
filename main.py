import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# Dynamically set the file path to the same directory as the script
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "datasets", "energy-consumption-by-source-and-country.csv")

def get_data(data_path):
    """
    Reads a CSV file and returns its contents as a DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The contents of the CSV file as a DataFrame.
    """
    try:
        data = pd.read_csv(data_path)
        return data
    except FileNotFoundError:
        print(f"ERROR -  The file '{data_path}' does not exist.")
    except Exception as e:
        print(f"The followingg error occurred: {e}")

# - EXERCISE 2 - #
# Import dataset 
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

fig_major.write_html("figure2.html")
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

fig_minor.show()
# - CHATGPT CODE ENDS HERE - #

# - EXERCISE 4/5 - #

# Explicit new data path 
data_path = os.path.join(current_dir, "datasets", "Indicator_3_1_Climate_Indicators_Annual_Mean_Global_Surface_Temperature_577579683071085080.csv")
# Import dataset 
df = get_data(data_path)

# Print Check
# print(df.columns)
# print(df.head(5))

# Filter for the 'World' series
df = df[df['Country'] == 'World']

# Keep only the 'Country' column and all number columns (years)
year_columns = [col for col in df.columns if col.isdigit()]
final_df = df[['Country'] + year_columns]

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

fig.show()
# - CHATGPT CODE ENDS HERE - #