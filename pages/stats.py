from dash import html, dcc, Input, Output, State, callback, register_page
import dash_mantine_components as dmc
import json
import pandas as pd
import plotly.express as px
import os

register_page(__name__, path="/stats")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(BASE_DIR, 'data', 'statData.json')
with open(file_path, 'r') as file:
    data = json.load(file)
file.close()

df = pd.DataFrame(data)

fig_scatter = px.scatter(
    df,
    x="nTargetsGerman",
    y="nTargetsMath",
    hover_data=["jobName"],
    color="Level",
    title="Scatter Plot: Deutsch vs Mathematik",
)
fig_scatter.update_layout(
    xaxis_title="Anzahl Kompetenzen Deutsch",
    yaxis_title="Anzahl Kompetenzen Mathematik",
    height=600,
)


layout = dmc.Container([
    html.H1("Statistics"),
    dmc.Card(
        children = [
            dcc.Graph(id="scatter-plot", figure=fig_scatter),
        ],
        shadow="sm",
        #padding="lg",
        radius="md",
        withBorder=True,
        style={
            "maxWidth": "1000px", 
            "margin": "auto",
            }
    ),
    ], fluid=True)
