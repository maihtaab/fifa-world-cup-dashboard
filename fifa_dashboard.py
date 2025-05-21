# FIFA World Cup Dashboard

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import os

# Load the dataset
df = pd.read_csv("fifa_world_cup_finals.csv")

# Combine Germany/West Germany for clarity
df['Winner'] = df['Winner'].replace("West Germany", "Germany")
df['Runner-Up'] = df['Runner-Up'].replace("West Germany", "Germany")

# Calculate wins per country
wins = df['Winner'].value_counts().reset_index()
wins.columns = ['Country', 'Wins']

# Create a prettier choropleth map
fig = px.choropleth(
    wins,
    locations="Country",
    locationmode="country names",
    color="Wins",
    color_continuous_scale="pinkyl",
    title="FIFA World Cup Wins by Country"
)

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("🌸 FIFA World Cup Dashboard", style={
            'textAlign': 'center',
            'fontFamily': 'Quicksand',
            'color': '#c25b7c',
            'padding': '10px'
        }),
        html.P("An aesthetic view of FIFA World Cup winners from 1930 to 2022 ✨", style={
            'textAlign': 'center',
            'color': '#888',
            'fontSize': '14px',
            'marginBottom': '30px'
        }),
    ]),

    dcc.Graph(figure=fig),

    html.Br(),
    html.Label("Select a country:", style={'fontWeight': 'bold'}),
    dcc.Dropdown(
        options=[{'label': c, 'value': c} for c in wins['Country']],
        id='country-dropdown'
    ),
    html.Div(id='country-output', style={'margin': '10px 0'}),

    html.Br(),
    html.Label("Select a year:", style={'fontWeight': 'bold'}),
    dcc.Dropdown(
        options=[{'label': y, 'value': y} for y in df['Year']],
        id='year-dropdown'
    ),
    html.Div(id='year-output', style={'marginTop': '10px'})
], style={'padding': '40px', 'fontFamily': 'Quicksand', 'maxWidth': '800px', 'margin': '0 auto'})

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

# Run server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=True)
