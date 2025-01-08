from dash import html, register_page

register_page(__name__, path="/")

layout = html.Div("Welcome to the Home Page!")