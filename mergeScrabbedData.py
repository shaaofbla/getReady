import json

with open('MathNodePositions.json', 'r') as file:
    nodePositions = json.load(file)
file.close()

with open('jobProfiles.json', 'r') as file:
    profiles = json.load(file)
file.close()

with open('MathTargetsIdsToLabels.json', 'r') as file:
    nodeLabels = json.load(file)
file.close()

with open('mathTargetsElements.json', 'r') as file:
    elements = json.load(file)
file.close()

for i, element in enumerate(elements):
    #print(element['data']['id'])
    id = element['data']['id']

    if len(id.split("-"))<=1:
        print(f'node: {id}, i: {i}')
        elements[i]['type'] = "node"
    else:
        print(f'edge: {id}, i: {i}')
        elements[i]['type'] = "edge"

correct = 0

for i, element in enumerate(elements):
    if element['type'] == "node":
        #print(element)
        # Update labels
        writtenLabel = element['data']['label']
        id = element['data']['id']
        scrabbedLabel = nodeLabels[id]
        if(writtenLabel==scrabbedLabel):
            print("well done.")
            correct = correct + 1
        else:
            print(f"replace: {writtenLabel}")
            print(f"with: {scrabbedLabel}")
            elements[i]['data']['label'] = scrabbedLabel
        nodeLabels.pop(id)
        # Update profiles
        if (element['data']['level']==3):
            elements[i]['data']['profile'] = profiles[id]
#print(nodeLabels)

for id, label in nodeLabels.items():
#    print(label)
 #   print(id)
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
#    print(nodeData)
#    print(edgeData)

#print(profiles)
print(elements)

with open("mathTargetsElementsScrabbed.json", "w") as outfile:
    json.dump(elements, outfile, indent=4)
outfile.close() 
#print(correct)

#print(elements)