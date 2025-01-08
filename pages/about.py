from dash import html, register_page

# Register this file as a page
register_page(__name__, path="/about")

layout = html.Div("Welcome to the About Page!")
