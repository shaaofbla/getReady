from dash import Dash, html, dcc, Input, Output, ctx, callback
import dash_mantine_components as dmc
import dash_cytoscape as cyto
import xlwings as xw
import json

cyto.load_extra_layouts()

data = xw.Book("Berufsprofile-Kompetenzraster.xlsx")
sheetRaster = data.sheets[0]
sheetProfiles = data.sheets[1]

with open('MathNodePositions.json', 'r') as file:
    nodePositions = json.load(file)
file.close()

def parseRaster(data, profile, nodesPositions):
    maxRows = getMaxRows(data)
    nodes = getNodes(data, maxRows, profile, nodesPositions)
    #print(nodes)
    edges = getEdges(data, maxRows, profile)
    return nodes + edges

def getNodes(data, maxRows, profile, nodePositions):
    nodeSet = {}
    for i in range(1,maxRows):
        for j in range(4):
            label = data[i,2*j].value
            id = data[i,2*j+1].value

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
            id_source = data[i,2*j+1].value
            id_target = data[i,2*j+3].value
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

#pyprofiles = parseProfiles(sheetProfiles)
#profiles = []

with open("mathTargetsElements.json", "r") as file:
    elements = json.load(file)
"""    
elements = parseRaster(sheetRaster, profiles, nodePositions)
with open("mathelementsWorking.json","w") as file:
    json.dump(elements,file, indent=4)
"""

#elements = cyto.filter('[id *="ZuV"]')

#filterElementsByProfile(elements, elementsNotInProfile)

styles = {
    'output': {
        'overflow-y': 'scroll',
        'overflow-wrap': 'break-word',
        'height': 'calc(100% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {'height': 'calc(98vh - 115px)'}
}

app = Dash(__name__)
server = app.server
with open('stylesheet.json','r') as file:
    stylesheet=json.load(file)

app.layout = dmc.MantineProvider([
    dmc.Title("Berufsexplorer"),
    dmc.Grid(
        children = [
            dmc.Col(        
                html.Div([
                    cyto.Cytoscape(
                        id='cytoscape-view',
                        layout={
                            'name': 'preset',
                                },
                        style={'width': 'auto', 'height': '707px'},
                        elements= elements,
                        stylesheet=stylesheet
                    ),
                    html.P(id='cytoscape-tapNodeData-output'),
                    html.P(id='cytoscape-selectedNodeData-output') 
                ]), span = 8
            ),
            dmc.Col(
                dmc.Select(
                    label="Beruf",
                    placeholder="Wähle einen Beruf",
                    id="profile-select",
                    value="all",
                    data=[
                        {"value": "automobilAs","label":"Automobilassistent"},
                        {"value": "detailhandelAs", "label": "Detailhandelsassistent"},
                        {"value": "all", "label": "Alle Lernziele anzeigen"}
                    ]
                ), span = 4
            ),
        ], gutter="xl",
    )
]
)
"""
html.Div(className='four columns', children=[
    dcc.Tabs(id='tabs-image-export', children=[
        dcc.Tab(label='generate jpg', value='jpg'),
        dcc.Tab(label='generate png', value='png')
    ]),
    html.Div(style=styles['tab'], children=[
        html.Div(
            id='image-text',
            children='image data will appear here',
            style=styles['output']
        )
    ]),
    html.Div('Download graph:'),
    html.Button("as jpg", id="btn-get-jpg"),
    html.Button("as png", id="btn-get-png"),
    html.Button("as svg", id="btn-get-svg")

])
"""

@callback(
    Output('cytoscape-view', 'elements'),
    Input('profile-select', 'value')
)

def select_profile(data):
    print("this is from the select profile callback: ")
    print(data)

"""
@callback(
    Output('image-text', 'children'),
    Input('cytoscape-image-export', 'imageData'),
)
def put_image_string(data):
    return data

@callback(
    Output("cytoscape-image-export", "generateImage"),
    [
        Input('tabs-image-export', 'value'),
        Input("btn-get-jpg", "n_clicks"),
        Input("btn-get-png", "n_clicks"),
        Input("btn-get-svg", "n_clicks"),
    ])
def get_image(tab, get_jpg_clicks, get_png_clicks, get_svg_clicks):
    ftype = tab
    action = 'store'

    if ctx.triggered:
        if ctx.triggered_id != "tabs-image-export":
            action = "download"
            ftype = ctx.triggered_id.split("-")[-1]
    return{
        'type': ftype,
        'action': action
    }
    """

if __name__ == '__main__':
    app.run(debug=True)
    