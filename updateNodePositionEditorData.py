import json


with open('MathNodePositions.json', 'r') as file:
    nodePositions = json.load(file) 
file.close()


with open('mathElements.json', 'r') as file:
    elements = json.load(file)
file.close()


for i, element in enumerate(elements):
    if element['type'] == "node":
        id = element['data']['id']
        if (id in nodePositions):
            elements[i]['position']['x'] = nodePositions[id]['x']*1000
            elements[i]['position']['y'] = nodePositions[id]['y']*707
            elements[i]['position']['locked'] = "true"
        else:
            elements[i]['position'] = {
                "x": 0.0,
                "y": 0.0,
                "locked": "true"
            }
    
    

print(elements)



"""
    nodeData = {
        "data": {
            "id": id,
            "label": label,
            "level": 3,
            "profile": profiles[id]

        },
        "position": {
            "x": 0.0,
            "y": 0.0,
            "locked": "true"
        }
    }
    
    edgeData = {
        "data": {
            "source": id[:-2],
            "target": id,
            "id": id[:-2]+"-"+id
        }
    }
    
    elements.append(nodeData)
    elements.append(edgeData)
    """
#    print(nodeData)
#    print(edgeData)

#print(profiles)
#print(elements)

with open("mathElementsUp.json", "w") as outfile:
   json.dump(elements, outfile, indent=4)
outfile.close()

#print(correct)

#print(elements)