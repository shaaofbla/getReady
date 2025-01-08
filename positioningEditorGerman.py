from dash import Dash, html, dcc, Input, Output, ctx, callback
import dash_cytoscape as cyto
import json
from copy import deepcopy
import shutil
import datetime

cyto.load_extra_layouts()


with open('germanNodePositions.json', 'r') as file:
    nodePositions = json.load(file)
file.close()

newNodePositions = deepcopy(nodePositions)

with open("germanElements.json", "r") as file:
    elements = json.load(file)
file.close()

for i, element in enumerate(elements):
    id = element['data']['id']
    if element['type'] == 'node':
       
        if id in nodePositions:
            element['position']['x'] = nodePositions[id]['x']*1000
            element['position']['y'] = nodePositions[id]['y']*707
            elements[i] = element

with open("germanElements.json", "w") as outfile:
    json.dump(elements, outfile, indent=4)
outfile.close()
"""
for i, element in enumerate(elements):
    
    id = element['data']['id']
    if element['type'] == 'node':
        if element['data']['field'] == 'Hören':
            if id in nodePositions:
                element['position']['x'] = nodePositions[id]['x']*500
                element['position']['y'] = nodePositions[id]['y']*353
                elements[i] = element
        elif element['data']['field'] == 'Lesen':
            if id in nodePositions:
                element['position']['x'] = nodePositions[id]['x']*500
                element['position']['y'] = nodePositions[id]['y']*352+353
                elements[i] = element
        elif element['data']['field'] == 'Sprechen':
            if id in nodePositions:
                element['position']['x'] = nodePositions[id]['x']*500+500
                element['position']['y'] = nodePositions[id]['y']*353
                elements[i] = element
        elif element['data']['field'] == 'Schreiben':
            if id in nodePositions:
                element['position']['x'] = nodePositions[id]['x']*500+500
                element['position']['y'] = nodePositions[id]['y']*353+352
                elements[i] = element
        else:
            element['position']['x'] = -500.0
            element['position']['y'] = 0.0
            elements[i] = element
"""
app = Dash(__name__)
server = app.server
with open('stylesheetGerman.json','r') as file:
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
    with open("germanNodePositions.json", "w") as outfile:
        json.dump(newNodePositions, outfile, indent=4)
    outfile.close()
    print("wrote new positions.")

try:
    app.run(debug=True)
finally:
    shutil.copyfile('germanNodePositions.json','germanNodePositions{0}.json'.format(str(datetime.datetime.now())))