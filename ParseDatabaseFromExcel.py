import xlwings as xw
import json

def getElements(nodeData, nodePositions, profiles, edges):
    nodes = getNodes(nodeData, nodePositions, profiles)
    edges = getEdges(edges)
    return nodes + edges

def getNodes(nodeData, nodePositions, profiles):
    nodes = []
    for id in nodeData:
        label = nodeData[id]['label']
        position = nodePositions[id]
        position['x'] = position['x']*1000
        position['y'] = position['y']*707
        level = nodeData[id]['level']
        if (id not in profiles):
            nodes.append({
                'data': {
                    'id': id, 
                    'label': label, 
                    'level': level
                    },
                'position': position 
            })
        else:
            profile = profiles[id]
            nodes.append({
                'data': {
                    'id': id, 
                    'label': label, 
                    'level': level,
                    'profile': profile
                    },
                'position': position 
            })
    return nodes

def parseNodeData(data):
    maxRows = getMaxRows(data)  
    nodeData = {}
    for i in range(1,maxRows):
        for j in range(4):
            label = data[i,2*j].value
            id = data[i,2*j+1].value
            if (id not in nodeData):
                nodeData[id] = {
                    "label": label,
                    "level": j
                }

    return nodeData

def getEdges(edges):
    edgeList = []
    for edge in edges: 
        edgeList.append(
            {
            'data': edges[edge]
            }
        )
    return edgeList

def parseEdges(data):
    maxRows = getMaxRows(data)  
    edgeSet = {}
    for i in range(1,maxRows):
        for j in range(3):
            id_source = data[i,2*j+1].value
            id_target = data[i,2*j+3].value
            id = str(id_source)+ "-"+str(id_target)
            if (id not in edgeSet):
                edgeSet[id] = {'source': id_source, 'target': id_target, 'id': id}
    
    return edgeSet

def parseProfiles(data):
    maxRows = getMaxRows(data)
    profilesByNodeId = {}
    nJobs = 2
    for j in range(2,nJobs+2):
        jobId = data[(1,j)].value
        for i in range(2,maxRows):
            idTree = data[(i,1)].value
            if data[(i,j)].value == "x": #2: automobilassisten, 3: 
                if idTree not in profilesByNodeId:
                    profilesByNodeId[idTree] = [jobId]
                else:
                    profilesByNodeId[idTree].append(jobId)
    return profilesByNodeId

        
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

if __name__ == '__main__':

    data = xw.Book("Berufsprofile-Kompetenzraster.xlsx")
    sheetRaster = data.sheets[0]
    sheetProfiles = data.sheets[1]
    profiles = parseProfiles(sheetProfiles)
    nodeData = parseNodeData(sheetRaster)
    edges = parseEdges(sheetRaster)

    with open("MathNodePositions.json", "r") as file:
        nodePositions = json.load(file)
    
    elements = getElements(nodeData, nodePositions, profiles, edges)
    print(elements)
    with open("mathTargetsElements.json", "w") as outfile:
        json.dump(elements, outfile, indent=4)
    outfile.close()