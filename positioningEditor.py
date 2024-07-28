from dash import Dash, html, dcc, Input, Output, ctx, callback
import dash_cytoscape as cyto
import xlwings as xw
import json
from copy import deepcopy
import shutil
import datetime

cyto.load_extra_layouts()

data = xw.Book("Berufsprofile-Kompetenzraster.xlsx")
sheetRaster = data.sheets[0]
sheetProfiles = data.sheets[1]

with open('MathNodePositions.json', 'r') as file:
    nodePositions = json.load(file)
file.close()
newNodePositions = deepcopy(nodePositions)


def parseRaster(data, profile, nodePositions):
    maxRows = getMaxRows(data)
    nodes = getNodes(data, maxRows, profile, nodePositions)
    edges = getEdges(data, maxRows, profile)
    return nodes + edges

def getNodes(data, maxRows, profile, nodePositions):
    nodeSet = {}
    for i in range(1,maxRows):
        for j in range(4):
            label = data[i,4*j].value
            id = data[i,4*j+1].value

            if (id not in nodeSet and id not in profile):
                position = nodePositions[id]
                position['x'] = position['x']*1000
                position['y'] = position['y']*707
                nodeSet[id] = {
                    'data': {'id': id, 'label': label, 'level': j},
                    'position': position
                }

    nodes = []
    for key in nodeSet: 
        nodes.append(nodeSet[key] )
    return nodes

def getEdges(data, maxRows, profile):
    edgeSet = {}
    for i in range(1,maxRows):
        for j in range(3):
            id_source = data[i,4*j+1].value
            id_target = data[i,4*j+5].value
            id = str(id_source)+ "-"+str(id_target)
            if (id not in edgeSet and id_target not in profile):
                edgeSet[id] = {'source': id_source, 'target': id_target}
    edges = []
    for key in edgeSet: 
        edges.append(
            {
            'data': edgeSet[key]
            }
        )
    return edges

def parseProfiles(data):
    maxRows = getMaxRows(data)
    items = []
    for i in range(1,maxRows):
        if data[(i,3)].value != "x": #2: automobilassisten, 3: detailhandelassistent
            items.append(data[i,1].value)
    return items

def filterElementsByProfile(elements, notProfile):
    newDict = { key:value for (key,value) in elements[0].items() if value not in notProfile}
    print(newDict)

def getMaxRows(data):
    i = 1
    condition = True
    while condition:        
        if data[(i,0)].value == None:
            condition = False 
        if i > 1000:
            condition = False
            print("Warning: Maxrows reachted")
        i += 1
    return(i-1)

profiles = parseProfiles(sheetProfiles)
profiles = []
elements = parseRaster(sheetRaster, profiles, nodePositions)

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
            zoomingEnabled = 0,
            panningEnabled = 0,
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