from dash import Dash, html, dcc, Input, Output, ctx, callback
import dash_cytoscape as cyto
import json
from copy import deepcopy
import shutil
import datetime

cyto.load_extra_layouts()


with open('MathNodePositions.json', 'r') as file:
    nodePositions = json.load(file)
file.close()
newNodePositions = deepcopy(nodePositions)

with open("mathElementsUp.json", "r") as file:
    elements = json.load(file)
file.close()


app = Dash(__name__)
server = app.server
with open('stylesheet.json','r') as file:
    style=json.load(file)

app.layout = html.Div([
    html.Div(className = 'eight columns', children=[
        cyto.Cytoscape(
            id='cytoscape-image-export',
            layout={
                'name': 'preset',
                    },
            style={'width': '1000px', 'height': '707px'},
            elements= elements,
            zoomingEnabled = False,
            panningEnabled = False,
            stylesheet = style

        ),
        html.P(id='cytoscape-tapNodeData-output'),
        html.P(id='cytoscape-selectedNodeData-output')
    ])
])

@callback(Output('cytoscape-tapNodeData-output', 'children'),
              Input('cytoscape-image-export', 'tapNode'),
              log = True)
def displayTapNodeData(data):
    if data is  None:
        return
    global newNodePositions
    id = data['data']['id']
    print(id)
    renderedPos = data['renderedPosition']
    renderedX = renderedPos['x']
    renderedY = renderedPos['y']
    if id not in newNodePositions:
        newNodePositions[id] = {}
    newNodePositions[id]['x'] = renderedX/1000
    newNodePositions[id]['y'] = renderedY/707
    with open("MathNodePositions.json", "w") as outfile:
        json.dump(newNodePositions, outfile, indent=4)
    outfile.close()
    print("wrote new positions.")

try:
    app.run(debug=True)
finally:
    shutil.copyfile('MathNodePositions.json','MathNodePositions{0}.json'.format(str(datetime.datetime.now())))