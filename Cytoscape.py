from dash import Dash, html
import dash_cytoscape as cyto
import xlwings as xw

data = xw.Book("Berufsprofile-Kompetenzraster.xlsx")
sheetRaster = data.sheets[0]
sheetProfiles = data.sheets[1]


def parseRaster(data, profile):
    maxRows = getMaxRows(data)
    nodes = getNodes(data, maxRows, profile)
    edges = getEdges(data, maxRows, profile)
    return nodes + edges

def getNodes(data, maxRows, profile):
    nodeSet = {}

    for i in range(1,maxRows):
        for j in range(4):
            label = data[i,2*j].value
            id = data[i,2*j+1].value
            if (id not in nodeSet and id not in profile):
                nodeSet[id] = {'id': id, 'label': label, 'level': j}
    
    nodes = []
    for key in nodeSet: 
        nodes.append(
            {
            'data': nodeSet[key]
            }
        )
    print(nodes)
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
    print(edges)
    return edges

def parseProfiles(data):
    maxRows = getMaxRows(data)
    items = []
    for i in range(1,maxRows):
        if data[(i,2)].value != "x":
            items.append(data[i,1].value)
    return items

def filterElementsByProfile(elements, notProfile):
    print(elements[1])
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

elements = parseRaster(sheetRaster, profiles)

#filterElementsByProfile(elements, elementsNotInProfile)

app = Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'cose'},## cose, consentic,breadthfirst
        style={'width': '100%', 'height': '800px'},
        elements= elements,
        stylesheet=[

        {
            'selector': 'node',
            'style': {
                'content': 'data(id)',
                'text-halign':'center',
                'text-valign':'center',
                'text-wrap':'wrap',
                'text-max-width': '300px',
                'width':'label',
                'height':'label',
                'background-color': 'blue',
                'shape':'ellipse',
                'padding': '30px',
                }
            },
        {
                'selector': '[id *= "A1_"],[id *= "A2_"]',
                'style': {
                    'content': 'data(label)',
                    'border-color': '#173F5F',
                    'border-width': '20px',
                    'shape': 'rectangle'
                }
            },
                {
                'selector': '[id *= "B1_"],[id *= "B2_"]',
                'style': {
                    'content': 'data(label)',
                    'border-color': '#20639B',
                    'border-width': '20px',
                    'shape': 'rectangle'
                }
            },
        {
                'selector': '[id *= "C1_"],[id *= "C2_"]',
                'style': {
                    'content': 'data(label)',
                    'border-color': '#3CAEA3',
                    'border-width': '20px',
                    'shape': 'rectangle'
                }
            },
        {
                'selector': '[id *= "D1_"],[id *= "D2_"]',
                'style': {
                    'content': 'data(label)',
                    'border-color': '#F6D55C',
                    'border-width': '20px',
                    'shape': 'rectangle'
                }
            },
        {
                'selector': '[id *= "E1_"],[id *= "E2_"]',
                'style': {
                    'content': 'data(label)',
                    'border-color': '#ED553B',
                    'border-width': '20px',
                    'shape': 'rectangle'
                }
            },
        {
                'selector': '[id *= "ZuV"]',
                'style': {
                    'background-color': '#05C793',
                    'shape': 'rectangle'
                }
            },
        {
                'selector': '[id *= "FuR"]',
                'style': {
                    'background-color': '#EF4365',
                    'shape': 'rectangle'
                }
            }, 
                {
                'selector': '[id *= "GFDZ"]',
                'style': {
                    'background-color': '#FFCE5C',
                    'shape': 'rectangle'
                }
            }, 
            {
                'selector': '[level < "2"]',
                'style': {
                    'shape': 'diamond',
                    'content': 'data(label)',
                    'font-size': '40',
                    'min-width': '60px'
                }
            }, 

        
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)

    #parseRaster(sheet)
    pass