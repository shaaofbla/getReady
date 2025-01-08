from dash import html, register_page

# Register this file as a page
register_page(__name__, path="/contact")

layout = html.Div("Welcome to the Contact Page!")
