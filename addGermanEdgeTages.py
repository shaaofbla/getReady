import json

with open('germanElements.json', 'r') as file:
    elements = json.load(file)
file.close()

fields = {
    'D': 'Schreiben',
    'C': 'Sprechen', 
    'B': 'Lesen', 
    'A': 'Hören'
    }

for i, element in enumerate(elements):
    if element['type'] == "edge":

        if len(element['data']['source']) > 3:

            if "1" == element['data']['source'][2]:
                elements[i]['data']['field'] = "Hören"
            elif "2" == element['data']['source'][2]:
                elements[i]['data']['field'] = "Lesen"
            elif "3" == element['data']['source'][2]:
                elements[i]['data']['field'] = "Sprechen"
            elif "4" == element['data']['source'][2]:
                elements[i]['data']['field'] = "Schreiben"
        elif element['data']['source'] == "Hr":
            elements[i]['data']['field'] = "Hören"
        elif element['data']['source'] == "Ls":
            elements[i]['data']['field'] = "Lesen"
        elif element['data']['source'] == "Sr   ":
            elements[i]['data']['field'] = "Sprechen"
        elif element['data']['source'] == "Sh":
            elements[i]['data']['field'] = "Schreiben"
        else:
            print("error")
            print(element)

        l=len(element['data']['target'])
        #print(l)
        if (l == 7):
            elements[i]['data']['nodeLevel'] = 1
        elif (l==9):
            elements[i]['data']['nodeLevel'] = 2
        elif (l==10):
            targetLevel = element['data']['target'][9]
            elements[i]['data']['targetLevel'] = targetLevel
            elements[i]['data']['nodeLevel'] = 3
    elif element['type'] == "node":
        print(element['data']['field'])
        #print(elements[i])
    #else:
     #   print("error")
#print(elements)
with open("germanElements.json", "w") as outfile:
    json.dump(elements, outfile, indent=4)
outfile.close()