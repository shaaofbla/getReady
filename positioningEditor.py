from dash import Dash, html, dcc, Input, Output, ctx, callback
import dash_cytoscape as cyto
import xlwings as xw
import json
from copy import deepcopy
import shutil
import datetime

cyto.load_extra_layouts()
readNodePositionsFromExcel = False

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
    if (readNodePositionsFromExcel):
        nodePositions = {}
        for node in nodes:
            print(node)
            id = node['data']['id']
            try:
                position = node['position']
                position['x'] = position['x']/1000
                position['y'] = position['y']/707
                nodePositions[id] = position
            except:
                nodePositions[id] = {'x': 1.0, 'y': 1.0, 'locked': 'true'}
        print(nodePositions)
        with open("MathNodePositions.json", "w") as outfile:
            json.dump(nodePositions, outfile, indent=4)
    

    edges = getEdges(data, maxRows, profile)
    return nodes + edges

def getNodes(data, maxRows, profile, nodePositions):
    nodeSet = {}
    for i in range(1,maxRows):
        for j in range(4):
            label = data[i,4*j].value
            id = data[i,4*j+1].value
            if (readNodePositionsFromExcel):
                posX = data[i,4*j+2].value
                posY = data[i,4*j+3].value
                if (id not in nodeSet and id not in profile):
                    if (posX == None or posY == None):
                        nodeSet[id] = {
                            'data': {'id': id, 'label': label, 'level': j}
                        }
                    else:
                        nodeSet[id] = {
                            'data': {'id': id, 'label': label, 'level': j},
                            'position': {'x': posX*1000, 'y': posY*707, 'locked': 'true'}
                    }
            else:
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
    #print(nodes)
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
    #print(edges)
    return edges

def parseProfiles(data):
    maxRows = getMaxRows(data)
    items = []
    for i in range(1,maxRows):
        if data[(i,3)].value != "x": #2: automobilassisten, 3: detailhandelassistent
            items.append(data[i,1].value)
    return items

def filterElementsByProfile(elements, notProfile):
    #print(elements[1])
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
    print(nodePositions['GFDZGuM3.1.3D1_desc'])
    id = data['data']['id']
    print(id)
    renderedPos = data['renderedPosition']
    print("nodePosition: ")
    print(data['position'])
    print(renderedPos)
    renderedX = renderedPos['x']
    renderedY = renderedPos['y']
    print("relativ Position:")
    print("X: "+str(renderedX/1000)+" Y: "+str(renderedY/707))
    newNodePositions[id]['x'] = renderedX/1000
    newNodePositions[id]['y'] = renderedY/707

    print(newNodePositions['ZuV'])
    with open("MathNodePositions.json", "w") as outfile:
        json.dump(newNodePositions, outfile, indent=4)
    outfile.close()
    print("wrote new positions.")

try:
    app.run(debug=True)
finally:
    shutil.copyfile('MathNodePositions.json','MathNodePositions{0}.json'.format(str(datetime.datetime.now())))