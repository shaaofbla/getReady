from dash import Dash, html, Input, Output, State
import dash_mantine_components as dmc
import dash 

app = Dash(__name__, use_pages=True)

app.layout = dmc.MantineProvider(
    children=html.Div(
        [
            dmc.Header(
                height = "7%",
                children= [
                    dmc.Grid(
                        children=[
                            dmc.Col(
                                dmc.Burger(
                                    id="burger-icon",
                                    opened=False,  
                                    size="sm",
                                    color="black",
                                ), span=1
                            ),
                            dmc.Col(
                                dmc.Group(
                                    children=[
                                    dmc.Title("Get Ready", order=1),
                                    ],
                                    position="center",
                                    spacing="lg"
                                ), span=10
                            )
                        ]
                    )
                ]
            ),
            dmc.Drawer(
                id="navbar",
                title="Get Ready",
                padding="md",
                size="300px",
                opened= False,  
                children=[
                    dmc.NavLink(label="Home", href="/"),
                    dmc.NavLink(label="About", href="/about"),
                    dmc.NavLink(label="Mathematik", href="/math"),
                    dmc.NavLink(label="Deutsch", href="/deutsch"),
                ],
            ),
            dash.page_container,
        ]
    )
)

@app.callback(
    Output("navbar", "opened"), 
    Output("burger-icon", "opened"),  
    Input("burger-icon", "opened"),
    prevent_initial_call=True
)
def toggle_navbar(is_opened):
    print(is_opened)
    return  is_opened, not is_opened


if __name__ == "__main__":
    app.run_server(__name__)
    server = app.server
