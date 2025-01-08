from dash import Dash, dcc, html, Input, Output, ctx

app = Dash(__name__)

app.layout = html.Div([
    dcc.Cytoscape(
        id='cytoscape-image-export',
        layout={'name': 'preset'},
        style={'width': '800px', 'height': '400px'},
        elements=[
            {'data': {'id': 'A', 'label': 'Node A'}, 'position': {'x': 100, 'y': 100}},
            {'data': {'id': 'B', 'label': 'Node B'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'A', 'target': 'B'}}
        ]
    ),
    html.Button("Export SVG", id="btn-get-svg"),
    html.Div(id='image-text')  # For debugging or displaying image data
])

@app.callback(
    Output('cytoscape-image-export', 'generateImage'),
    Output('image-text', 'children'),
    Input('btn-get-svg', 'n_clicks'),
    prevent_initial_call=True
)
def export_svg(n_clicks):
    # Trigger SVG generation
    return (
        {
            'type': 'pdf',  # File type for SVG
            'action': 'both',  # Store image in `imageData` and download it
            'filename': 'cytoscape_graph.pdf'  # Optional filename
        },
        "Generating SVG. Check your downloads or image data!"
    )

if __name__ == '__main__':
    app.run_server(debug=True)
