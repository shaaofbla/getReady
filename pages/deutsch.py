from dash import Dash, html, dcc, Input, Output, State, ctx, callback, register_page
import dash_mantine_components as dmc
import dash_cytoscape as cyto
import json
import pages.theme as theme
import os

register_page(__name__, path="/deutsch")

cyto.load_extra_layouts()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(BASE_DIR,'data', 'germanElements.json')
with open(file_path, "r") as file:
    default_elements = json.load(file)
file.close()

file_path = os.path.join(BASE_DIR,'data', 'stylesheetGerman.json')
with open(file_path,'r') as file:
    stylesheet=json.load(file)
file.close()
default_stylesheet = stylesheet.copy()


file_path = os.path.join(BASE_DIR,'data', 'jobIdstoJobNames.json')
with open(file_path, 'r') as file:
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
                    id="tabs-deutsch",
                    value="explorer",
                    children=[
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
                                    dmc.RadioGroup(
                                        id = "select-field-deutsch",
                                        label="Felder",
                                        orientation="vertical",
                                        value="all",
                                        children =[
                                            dmc.Radio(label="Alle", value="all",color="deutsch.7"),
                                            dmc.Radio(label="Hören", value="Hören", color="deutsch.4"),
                                            dmc.Radio(label="Lesen", value="Lesen", color="deutsch.2"),
                                            dmc.Radio(label="Sprechen", value="Sprechen", color="deutsch.6"),
                                            dmc.Radio(label="Schreiben", value="Schreiben", color="deutsch.0")
                                            ],
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
                                dmc.Badge("Profil A",variant="filled",size="xl",radius="xs",color="deutsch.1"),
                                dmc.Badge("Profil B",variant="filled",size="xl",radius="xs",color="deutsch.5"),
                                dmc.Badge("Beide",variant="filled",size="xl",radius="xs",color="deutsch.3"),
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
        Input('tabs-deutsch', 'value'),
        prevent_initial_call=True
)
def annotationHandling(value):
    if value == "compare":
        return default_elements
    else:
        return default_elements

@callback(
    Output('cytoscape-view-deutsch', 'stylesheet',allow_duplicate=True),
    Input('tabs-deutsch', 'value'),
    prevent_initial_call=True
)
def change_stylesheet(value):
    colorA = theme.custom_pallete['deutsch'][1]
    colorB = theme.custom_pallete['deutsch'][5]
    colorBoth = theme.custom_pallete['deutsch'][3]
    if value == "explorer":
        return default_stylesheet
    else:
        stylesheet = default_stylesheet
        new_stylesheet = [
            {
                "selector": "[classes *= 'A']",
                "style" : {
                    "background-color": colorA,
                    "border-color": colorA
                }
            },
            {
                "selector": "[classes *= 'both']",
                "style" : {
                    "background-color": colorBoth,
                    "border-color": colorBoth
                }
            },
            {
                "selector": "[classes *= 'B']",
                "style" : {
                    "background-color": colorB,
                    "border-color": colorB
                }
            }
        ]
        return stylesheet+new_stylesheet

@callback(
        Output('cytoscape-view-deutsch', 'elements', allow_duplicate=True),
        Input('select-field-deutsch', 'value'),
        Input('profile-select-deutsch', 'value'),
        Input('tabs-deutsch', 'value'),
        prevent_initial_call = True
)
def select_fields(value, profile, tab):
    elements = []
    print("field ", value)
    print("profile ", profile)
    # Filter elements by field
    if value != 'all':
        for element in default_elements:
            if value == element['data']['field']:
                elements.append(element)
    else:
        elements = default_elements

    if profile == 'all':
        return elements
    
    new_elements = []
    targetIds = []

    # Filter elements by profile
    for element in elements:

        if element['type'] == 'node' and element['data']['level'] == 3:
            if profile in element['data']['profile']:
                new_elements.append(element)
                targetIds.append(element['data']['id'])
        elif element['type'] == 'node' and element['data']['level'] <= 2:
            new_elements.append(element)
            targetIds.append(element['data']['id'])
        elif element['type'] == 'edge':
            if element['data']['target'] in targetIds:
                new_elements.append(element)

    # Add annotation
    if profile == 'all':
        label = 'Alle Kompetenzen'
    else:
        label = profilesLabels[profile]
        label = label.replace("/", "/\n")

    annotation_Positions = {
        'Hören': {'x': -25., 'y': 170.},
        'Lesen': {'x': -25., 'y': 500.},
        'Sprechen': {'x': 430., 'y': 170.},
        'Schreiben': {'x': 435., 'y': 520.},
        'all': {'x': -25., 'y': 350.}
    }

    new_elements.append({
        'data': {
            'id': 'annotation',
            'label': label,
            'field': 'annotation'
        },
        'position': annotation_Positions[value]
    })
    
    return new_elements

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
    State('select-field-deutsch', 'value'),

    prevent_initial_call=True
)
def export_svg(n_clicks, value, fields):
    # Trigger PNG generation
    print(value)
    print(fields)
    print(profilesLabels)

    if value == "all":
        jobName = "AlleKompetenzen"
    else:
        jobName = profilesLabels[value]
        if "/" in jobName:
            jobName = jobName.split("/")
            jobName = jobName[0]
            jobName = jobName.replace(" ", "")
        elif "(" in jobName:
            jobName = jobName.split("(")
            #jobName = jobName.split(")")
            jobName = jobName[1]
            jobName = jobName.replace(")", "")
            jobName = jobName.replace(" ", "-")
        else:
            print(jobName)
            
    if fields[0] == "all":
        fields = "AlleFelder"
    filename = 'Kompetenzen-Deutsch-{0}-{1}'.format(jobName,fields)
    print(filename)
    return (
        {
            'type': 'svg',  
            'action': 'download',
            'filename': filename  # Optional filename
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
                    'x': -25.,
                    'y': 350.,
                    'locked': 'true'
                }
            }
        )
    return new_elements
    
@callback(
        Output('cytoscape-view-deutsch', 'stylesheet'),
        Input('select-field-deutsch', 'value'),
        Input('profile-select-deutsch', 'value'),
        prevent_initial_call=True
    )
def annotation_styling(value, tab):
    if value == 'all':
        stylesheet.append(
            {
                "selector": "[field = 'annotation']",
                "style": {
                    "label": "data(label)",
                    "font-size": "14",
                    "background-color": "#aaaaaa",
                    "border-color": "#888888",
                    "text-max-width": "300px",
                    "text-wrap": "wrap",
                    "text-justify": "left",
                    "text-border-color":"black",
                    "shape":"rectangle",
                    "border-width":"3px",
                    "text-rotation": "270deg",
                    "width": "40",
                    "height": "330"

                }
        }
    )
    else:
        stylesheet.append(
            {
                "selector": "[field = 'annotation']",
                "style": {
                    "label": "data(label)",
                    "font-size": "10",
                    "background-color": "#aaaaaa",
                    "border-color": "#888888",
                    "text-max-width": "250px",
                    "text-wrap": "wrap",
                    "text-justify": "left",
                    "text-border-color":"black",
                    "shape":"rectangle",
                    "border-width":"3px",
                    "text-rotation": "270deg",
                    "width": "20",
                    "height": "250"
                }
            }
        )
    return stylesheet

    
