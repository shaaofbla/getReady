from dash import Dash, html, dcc, Input, Output, State, ctx, callback, register_page
import dash_mantine_components as dmc
import dash_cytoscape as cyto
import json


register_page(__name__, path="/deutsch")

cyto.load_extra_layouts()


with open("germanElements.json", "r") as file:
    default_elements = json.load(file)
file.close()


with open('stylesheetGerman.json','r') as file:
    stylesheet=json.load(file)
file.close()

with open('jobIdstoJobNames.json', 'r') as file:
    profilesLabels = json.load(file)
file.close()

profilesLabelsSelectData = [{"value": "all", "label": "Alle Kompetenzen anzeigen"}]
for value in profilesLabels:
    profilesLabelsSelectData.append({
        "value": value,
        "label": profilesLabels[value]
    })

layout = html.Div([
    dmc.Grid(
        grow = True,
        children = [
            dmc.Col(        
                html.Div([
                    cyto.Cytoscape(
                        id='cytoscape-view-deutsch',
                        layout={
                            'name': 'preset', #'euler'->is taking the positions into account,#'preset',
                            'animate': True
                                },
                        style={
                            'width': 'auto', 
                            'height': '707px',
                            'background-color': 'white'
                            },
                        elements= default_elements,
                        stylesheet=stylesheet
                    ),
                    html.P(id='cytoscape-tapNodeData-output-deutsch'),
                    html.P(id='cytoscape-selectedNodeData-output-deutsch') 
                ]), span = 8
            ),
            dmc.Col(
                dmc.Tabs(
                    [
                        dmc.TabsList(
                            [
                                dmc.Tab("Explorer", value="explorer"),
                                dmc.Tab("Compare", value="compare")
                            ]
                        ),
                        dmc.TabsPanel(
                            [
                                dmc.Select(
                                label="Beruf",
                                placeholder="Wähle einen Beruf",
                                id="profile-select-deutsch",
                                value="all",
                                searchable = True,
                                data=profilesLabelsSelectData
                                ),
                                html.Div(
                                    dmc.CheckboxGroup(
                                        id = "select-field-deutsch",
                                        label="Felder",
                                        orientation="vertical",
                                        children =[
                                            dmc.Checkbox(label="Hören", value="Hören"),
                                            dmc.Checkbox(label="Lesen", value="Lesen"),
                                            dmc.Checkbox(label="Sprechen", value="Sprechen"),
                                            dmc.Checkbox(label="Schreiben", value="Schreiben")

                                            ],
                                        value=["Hören", "Lesen", "Sprechen", "Schreiben"],

                                    )
                                ),
                                dmc.Button("Generate SVG", id="generate-svg-button-deutsch"),
                                html.Div(id='image-text-deutsch')

                            ], value = "explorer",
                        ),
                        dmc.TabsPanel(
                            [
                                dmc.Select(
                                label="Berufsprofil A",
                                placeholder="Berufsprofil A",
                                id="profile-selectA-deutsch",
                                value="all",
                                searchable = True,
                                data=profilesLabelsSelectData
                                ),
                                dmc.Select(
                                label="Berufsprofil B",
                                placeholder="Berufsprofil B",
                                id="profile-selectB-deutsch",
                                value="all",
                                searchable = True,
                                data=profilesLabelsSelectData
                                ),
                            ], value = "compare"
                        )
                    ], 
                    color="red",
                    orientation="horizontal",
                ), span = 2
            ),
        ], gutter="xl",
    )
    ]
)
@callback(
        Output('cytoscape-view-deutsch', 'elements', allow_duplicate=True),
        Input('select-field-deutsch', 'value'),
        prevent_initial_call = True
)
def select_fields(value):
    elements = []
    for val in value:
        for element in default_elements:
            if val == element['data']['field']:
                elements.append(element)
    return elements

@callback(
    Output('cytoscape-view-deutsch', 'elements', allow_duplicate=True),
    Input('profile-selectA-deutsch','value'),
    Input('profile-selectB-deutsch', 'value',),
    prevent_initial_call = True
)
def compare_profiles(value1, value2):
    innerNodes = [] 
    leafNodes = {}
    edges = {}
    profiles = {}
    # Extract data from elements
    for element in default_elements:
        if 'position' in element:
            if (element['data']['level']) == 3:
                profiles[element['data']['id']] = element['data']['profile']
                leafNodes[element['data']['id']] = element
            else:
                innerNodes.append(element)
        else:
            edges[element['data']['target']] = element
    
    #Check profile
    new_elements = innerNodes
    removed_elements = []
    for id in profiles:
        if (value1 in profiles[id] and value2 in profiles[id]):
            print("add to profileAB:")
            leafNodes[id]['data']['classes'] = "both"
            print(leafNodes[id])
            print("\n")
            new_elements.append(leafNodes[id])
        elif (value1 in profiles[id]):
            print("add to profile A")
            leafNodes[id]['data']['classes'] = "A"
            print(leafNodes[id])
            new_elements.append(leafNodes[id])
            print("\n")
        elif (value2 in profiles[id]):
            print("add to profile B")
            leafNodes[id]['data']['classes'] = "B"
            print(leafNodes[id])
            new_elements.append(leafNodes[id])
            print("\n")
        else:
            removed_elements.append(leafNodes[id])

    for node in removed_elements:
        edges.pop(node['data']['id'])

    for edge in edges:
        new_elements.append(edges[edge]) 

    return new_elements

@callback(
    Output('cytoscape-view-deutsch', 'generateImage'),
    Output('image-text-deutsch', 'children'),
    Input('generate-svg-button-deutsch', 'n_clicks'),
    State('profile-select-deutsch', 'value'),
    prevent_initial_call=True
)
def export_svg(n_clicks, value):
    print("value: ", value)
    # Trigger PNG generation
    return (
        {
            'type': 'png',  
            'action': 'both',
            'filename': 'Kompetenzen-Deutsch-{0}'.format(value)  # Optional filename
        },
        "Generating SVG. Check your downloads!"
    )



@callback(
    Output('cytoscape-view-deutsch', 'elements'),
    Input('profile-select-deutsch', 'value'),
    prevent_initial_call = True
)
def select_profile(value):
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
        edges.pop(node['data']['id'])

    for edge in edges:
        new_elements.append(edges[edge])
    
    if value != 'all':
        new_elements.append({
            'data': {
                'id': 'annotation',
                'label': profilesLabels[value],
                'field': 'annotation'
            },
            'position': {
                    'x': 500.,
                    'y': 30.,
                    'locked': 'true'
                }
            }
        )

    
    return new_elements
