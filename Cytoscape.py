from dash import Dash, html, dcc, Input, Output, State, ctx, callback
import dash_mantine_components as dmc
import dash_cytoscape as cyto
import json
import pdfkit

cyto.load_extra_layouts()

with open("mathTargetsElementsScrabbed.json", "r") as file:
    default_elements = json.load(file)


app = Dash(__name__)
server = app.server
with open('stylesheet.json','r') as file:
    stylesheet=json.load(file)

with open('jobIdsToJobNames.json', 'r') as file:
    profilesLabels = json.load(file)

profilesLabelsSelectData = [{"value": "all", "label": "Alle Lernziele anzeigen"}]
for value in profilesLabels:
    profilesLabelsSelectData.append({
        "value": value,
        "label": profilesLabels[value]
    })

navbar = dmc.Navbar(
    children=[
        dmc.Group(
            children=[
                dmc.NavLink(label="Home", href="/"),
                dmc.NavLink(label="About", href="/about"),
                dmc.NavLink(label="Contact", href="/contact")
                
            ],
            position="top",
            spacing="lg"
        )
    ],
    height=60,
    p="md",
    style={"backgroundColor": "grey"}
)

app.layout = dmc.MantineProvider([
    navbar,
    dmc.Title("Berufsexplorer"),
    dmc.Grid(
        children=[
            dmc.Col(
                html.Div([
                    cyto.Cytoscape(
                        id='cytoscape-view',
                        layout={
                            'name': 'preset',
                            'animate': True
                        },
                        style={'width': 'auto', 'height': '707px'},
                        elements=default_elements,
                        stylesheet=stylesheet
                    ),
                    html.P(id='cytoscape-tapNodeData-output'),
                    html.P(id='cytoscape-selectedNodeData-output')
                ]), span=8
            ),
            dmc.Col(
                dmc.Tabs(
                    [
                        dmc.TabsList(
                            [
                                dmc.Tab("Explorer", value="explorer"),
                                dmc.Tab("Vergleichen", value="compare")
                            ]
                        ),
                        dmc.TabsPanel(
                            [
                                dmc.Select(
                                    label="Beruf",
                                    placeholder="Wähle einen Beruf",
                                    id="profile-select",
                                    value="all",
                                    data=profilesLabelsSelectData
                                ), 
                                dmc.Button("Generate PDF", id="generate-pdf-button")

                            ], value="explorer"
                        ), 
                        dmc.TabsPanel(
                            [
                                dmc.Select(
                                    label="Berufsprofil A",
                                    placeholder="Berufsprofil A",
                                    id="profile-selectA",
                                    value="all",
                                    data=profilesLabelsSelectData
                                ),
                                dmc.Select(
                                    label="Berufsprofil B",
                                    placeholder="Berufsprofil B",
                                    id="profile-selectB",
                                    value="all",
                                    data=profilesLabelsSelectData
                                ),
                                dmc.Button("Generate PDF", id="generate-pdf-button")
                            ], value="compare"
                        )
                    ],
                    color="red",
                    orientation="horizontal",
                ), span=4
            ),
        ], gutter="xl",
    )
])
"""
@callback(
    Output('cytoscape-view', 'generateImage'),
    Input('generate-pdf-button', 'n_clicks'),
    prevent_initial_call=True
)
def generate_pdf(n_clicks):
    print("generate pdf")
    if n_clicks:
        # HTML-Inhalt der Cytoscape-Ansicht abrufen
        html_content = app.get_asset_url('cytoscape-view')
        print(html_content)
        # PDF-Datei generieren
        pdfkit.from_string(html_content, 'cytoscape_view.pdf')
        
        return {
            'type': "pdf",
            'action': "download"
        }
"""

@callback(
    Output('cytoscape-view', 'elements', allow_duplicate=True),
    Input('profile-selectA','value'),
    Input('profile-selectB', 'value'),
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
    Output('cytoscape-view', 'elements'),
    Input('profile-select', 'value'),
    prevent_initial_call = True
)
def select_profile(value):
    
    print("select profile")
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
    return new_elements

if __name__ == '__main__':
    app.run(debug=True)
    