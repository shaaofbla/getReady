from dash import Dash, html, dcc, Input, Output, State, ctx, callback
import dash_mantine_components as dmc
import dash_cytoscape as cyto
import xlwings as xw
import json

cyto.load_extra_layouts()



with open("mathTargetsElements.json", "r") as file:
    default_elements = json.load(file)


app = Dash(__name__)
server = app.server
with open('stylesheet.json','r') as file:
    stylesheet=json.load(file)

with open('profilesLabels.json', 'r') as file:
    profilesLabels = json.load(file)

profilesLabelsSelectData = [{"value": "all", "label": "Alle Lernziele anzeigen"}]
for value in profilesLabels:
    profilesLabelsSelectData.append({
        "value": value,
        "label": profilesLabels[value]
    })


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
                            'animate': 'true'
                                },
                        style={'width': 'auto', 'height': '707px'},
                        elements= default_elements,
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
                    data=profilesLabelsSelectData
                ), span = 4
            ),
        ], gutter="xl",
    )
]
)

@callback(
    Output('cytoscape-view', 'elements'),
    Input('profile-select', 'value'),
)

def select_profile(value):
    print(len(default_elements))
    print(default_elements[-1])
    if value == "all":
        return default_elements
    
    nodes = []
    edges = {}

    for element in default_elements:
        if 'position' in element:
            nodes.append(element)
        else:
            edges[element['data']['target']] = element

    new_elements = []
    removed_elements = []
    for node in nodes:
        if 'profile' not in node['data']:
            new_elements.append(node)
        else:
            if value in node['data']['profile']:
                new_elements.append(node)
            else:
                removed_elements.append(node)

    for node in removed_elements:
        print(node['data']['id'])
        edges.pop(node['data']['id'])

    print(edges)
    for edge in edges:
        print(edge)
        new_elements.append(edges[edge])
    #print(new_elements)
    return new_elements


if __name__ == '__main__':
    app.run(debug=True)
    