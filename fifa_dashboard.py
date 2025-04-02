# FIFA World Cup Dashboard - Hosted with Dash
# If hosted on Render, include link here (e.g., https://your-app.onrender.com)

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load the dataset
df = pd.read_csv("fifa_world_cup_finals.csv")

# Treat "West Germany" and "Germany" as the same
df['Winner'] = df['Winner'].replace("West Germany", "Germany")
df['Runner-Up'] = df['Runner-Up'].replace("West Germany", "Germany")

# Prepare wins per country
wins = df['Winner'].value_counts().reset_index()
wins.columns = ['Country', 'Wins']

# Choropleth map
fig = px.choropleth(wins,
                    locations="Country",
                    locationmode="country names",
                    color="Wins",
                    color_continuous_scale="Blues",
                    title="FIFA World Cup Wins by Country")

# Dash app setup
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard"),

    dcc.Graph(figure=fig),

    html.Br(),
    html.Label("Select a country:"),
    dcc.Dropdown(
        options=[{'label': c, 'value': c} for c in wins['Country']],
        id='country-dropdown'
    ),
    html.Div(id='country-output'),

    html.Br(),
    html.Label("Select a year:"),
    dcc.Dropdown(
        options=[{'label': y, 'value': y} for y in df['Year']],
        id='year-dropdown'
    ),
    html.Div(id='year-output')
])

# Callbacks
@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country(country):
    if country:
        num_wins = wins[wins['Country'] == country]['Wins'].values[0]
        return f"{country} has won the World Cup {num_wins} times."
    return ""

@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year(year):
    if year:
        row = df[df['Year'] == year]
        return f"In {year}, {row['Winner'].values[0]} won, and {row['Runner-Up'].values[0]} was the runner-up."
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
