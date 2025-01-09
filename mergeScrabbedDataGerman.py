import json

#with open('MathNodePositions.json', 'r') as file:
#    nodePositions = json.load(file)
#file.close()

#with open('jobProfiles.json', 'r') as file:
#    profiles = json.load(file)
#file.close()

#with open('MathTargetsIdsToLabels.json', 'r') as file:
#    nodeLabels = json.load(file)
#file.close()

#with open('mathTargetsElements.json', 'r') as file:
#    elements = json.load(file)
#file.close()

with open('germanDep.json', 'r') as file:
    tree = json.load(file)
file.close()


profiles = {}

for node in tree:
    print(node)
    jobId = node
    for field in tree[node]:
        print(field)
        for subfield in tree[node][field]:
            print(subfield)
            for subsubfield in tree[node][field][subfield]["children"]:
                print(subsubfield)
                for leaf in tree[node][field][subfield]["children"][subsubfield]["children"]:
                    print(tree[node][field][subfield]["children"][subsubfield]["children"][leaf]["checked"])
                    check = tree[node][field][subfield]["children"][subsubfield]["children"][leaf]["checked"]

                    if check: 
                        if leaf not in profiles:
                            profiles[leaf] = [jobId]
                            
                        else:
                            profiles[leaf].append(jobId)
print(profiles)
print(len(tree))
quit()
elements = []
ids = []

for i, node in enumerate(tree):
    jobId = node
    print(jobId)
    if jobId not in ids:
        ids.append(jobId)
    print(tree[jobId])
    for field in tree[jobId]:
        print(field)
        idLevel0 = field[0]+field[2]
        print(idLevel0)
        
        if (idLevel0 not in ids):
            elements.append({
                "data": {
                    "id": idLevel0,
                    "label": field,
                    "level": 0,
                    "field": field
                    
                },
                "position": {
                    "x": 0.0,
                    "y": 0.0,
                    "locked": "true"
                },
                "type": "node"
            })
            ids.append(idLevel0)

        for subfield in tree[jobId][field]:
            print("\t"+subfield)
            idLevel1 = subfield
            
            label = tree[jobId][field][subfield]
            ["label"]
            print("\t"+ label["label"])
            if idLevel1 not in ids:
                # add node            
                elements.append({
                    "data": {
                        "id": idLevel1,
                        "label": label["label"],
                        "level": 1,
                        "field": field
                    },
                    "position": {
                        "x": 0.0,
                        "y": 0.0,
                        "locked": "true"
                    },
                    "type": "node"
                })
                # add edge
                elements.append({
                    "data": {
                        "source": idLevel0,
                        "target": idLevel1,
                        "id": idLevel0+"-"+idLevel1
                    },
                    "type": "edge"
                })
                ids.append(idLevel1)

            for subsubfield in tree[jobId][field][subfield]["children"]:
                idLevel2 = subsubfield
                print("\t\t"+idLevel2)
                label = tree[jobId][field][subfield]["label"]
                print("\t\t"+label)

                if idLevel2 not in ids:
                    # add node
                    elements.append({
                        "data": {
                            "id": idLevel2,
                            "label": label,
                            "level": 2,
                            "field": field
                        },
                        "position": {
                            "x": 0.0,
                            "y": 0.0,
                            "locked": "true"
                        },
                        "type": "node"
                    })
                    # add edge
                    elements.append({
                        "data": {
                            "source": idLevel1,
                            "target": idLevel2,
                            "id": idLevel1+"-"+idLevel2
                        },
                        "type": "edge"
                    })
                    ids.append(idLevel2)

                for leaf in tree[jobId][field][subfield]["children"][subsubfield]["children"]:
                    print("\t\t\t"+leaf)
                    idLevel3 = leaf
                    
                    label = tree[jobId][field][subfield]["children"][subsubfield]["children"][leaf]["label"]
                    print("\t\t\t"+label[1:50])
                    if idLevel3 not in ids:
                        # add node
                        elements.append({
                            "data": {
                                "id": idLevel3,
                                "label": label,
                                "level": 3,
                                "field": field,
                                "profile": profiles[idLevel3]
                            },
                            "position": {
                                "x": 0.0,
                                "y": 0.0,
                                "locked": "true"
                            },
                            "type": "node"
                        })
                        # add edges
                        elements.append({
                            "data": {
                                "source": idLevel2,
                                "target": idLevel3,
                                "id": idLevel2+"-"+idLevel3
                            },
                            "type": "edge"
                            })
                        ids.append(idLevel3)

                    
    print(elements)
    with open("germanElements.json", "w") as outfile:
        json.dump(elements, outfile, indent=4)
    outfile.close()
    quit()
    
    
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
#print(elements)

#with open("mathTargetsElementsScrabbed.json", "w") as outfile:
#    json.dump(elements, outfile, indent=4)
#outfile.close() 
#print(correct)

#print(elements)