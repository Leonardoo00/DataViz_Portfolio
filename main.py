import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import logging #TODO: implement logging code

data_path = "/Users/leonardo/Desktop/Ongoing_Courses/Data_Visualization/progetto/energy_production_dataset/energy-consumption-by-source-and-country.filtered/energy-consumption-by-source-and-country.csv"

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

# Import dataset 
df = get_data(data_path)

# Print Check
print(df.columns)
print(df.head(5))

# Check for NaN values
# NaN_values = data.isna().sum().sum()
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

# TODO: DECIDE ON TABLE TEST 
# # Calculate the latest percentage of each energy source for the last year
# latest_year = df_filtered['Year'].iloc[-1]
# latest_data = df_filtered[df_filtered['Year'] == latest_year].iloc[0, 1:]

# # Prepare data for the table
# sources = [source.split(' consumption')[0] for source in latest_data.index]
# percentages = [f"{value:.2f}%" for value in latest_data.values]

# # Create a table to display the percentages
# table_fig = go.Figure(data=[go.Table(
#     header=dict(values=["<b>Energy Source</b>", "<b>Percentage in {}</b>".format(int(latest_year))],
#                 fill_color='lightgrey',
#                 align='left',
#                 font=dict(size=14, family='Arial Black')),
#     cells=dict(values=[sources, percentages],
#                fill_color='white',
#                align='left',
#                font=dict(size=12, family='Arial'))
# )])

# table_fig.update_layout(
#     title_text=f"<b>Energy Consumption by Source in {int(latest_year)}</b>",
#     title_font=dict(size=20, family='Arial Black'),
#     margin=dict(l=20, r=20, t=40, b=20)
# )

# table_fig.show()

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

fig_major.write_html("interactive_plot.html")
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

exit()

# EXERCISE 2
# Load the dataset
file_path = '/Users/leonardo/Desktop/Ongoing_Courses/Data_Visualization/progetto/natural_disaster_dataset/decadal-average-annual-number-of-deaths-from-disasters.csv'
df = pd.read_csv(file_path)

# Create a choropleth map using Plotly
fig = px.choropleth(
    df,
    locations="Country name",
    locationmode="country names",
    color="Number of deaths from disasters",
    hover_name="Country name",
    color_continuous_scale="Reds",
    labels={"Number of deaths from disasters": "Annual Deaths from Disasters"},
    title="Decadal Average: Annual Number of Deaths from Disasters (2020)",
    range_color=[df["Number of deaths from disasters"].min(), df["Number of deaths from disasters"].max()]
)

fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")
fig.update_layout(coloraxis_colorbar={
    'title': 'Deaths',
    'ticks': 'outside',
    'tickvals': [1, 10, 100, 1000, 10000, 100000],
    'ticktext': ['1', '10', '100', '1,000', '10,000', '100,000']
})

fig.show()
