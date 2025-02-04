import json
import pandas as pd
import plotly.express as px
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


file_path = os.path.join(BASE_DIR,'data', 'germanElements.json')
with open(file_path, 'r') as file:
    elements = json.load(file) 
file.close()

file_path = os.path.join(BASE_DIR,'data', 'jobIdstoJobNames.json')
with open(file_path, 'r') as file:
    profilesLabels = json.load(file)
file.close()

germanTargets = {}

for element in elements:
    id = element['data']['id']
    if "profile" in element['data']:
        for target in element['data']['profile']:
            if target not in germanTargets:
                germanTargets[target] = [id]
            else:
                germanTargets[target].append(id)

data = {"jobId": [], "nTargetsGerman": [], "nTargetsMath": [], "jobName": [], "Level": [], "nTargetsGerman_Sprechen": [], "nTargetsGerman_Schreiben": [], "nTargetsGerman_Hören": [], "nTargetsGerman_Lesen": []}

for jobId in germanTargets:
    print(jobId)
    print(len(germanTargets[jobId]))
    data["jobId"].append(jobId)
    data["nTargetsGerman"].append(len(germanTargets[jobId]))
    data["jobName"].append(profilesLabels[jobId])
    if "EBA" in profilesLabels[jobId]:
        data["Level"].append("EBA")
    elif "EFZ" in profilesLabels[jobId]:
        data["Level"].append("EFZ")
    elif "BM" in profilesLabels[jobId]:
        data["Level"].append("BM")
    else:
        data["Level"].append("Other")
        print(data["jobName"])

    Sprechen = 0
    Schreiben = 0
    Hören = 0
    Lesen = 0

    for target in germanTargets[jobId]:
        print(target[2])

        if target[2] == "3":
            Sprechen = Sprechen + 1
        elif target[2] == "4":
            Schreiben = Schreiben + 1
        elif target[2] == "1":
            Hören = Hören + 1
        elif target[2] == "2":
            Lesen = Lesen + 1
    
    data["nTargetsGerman_Sprechen"].append(Sprechen)
    data["nTargetsGerman_Schreiben"].append(Schreiben)
    data["nTargetsGerman_Hören"].append(Hören)  
    data["nTargetsGerman_Lesen"].append(Lesen)  
        
print(data) 



#print(data)
    
mathTargets = {}

with open('mathElements.json', 'r') as file:
    elements = json.load(file)  
file.close()

for element in elements:
    id = element['data']['id']
    if "profile" in element['data']:
        for target in element['data']['profile']:
            if target not in mathTargets:
                mathTargets[target] = [id]
            else:
                mathTargets[target].append(id)

data["nTargetsMath"] = [0]*len(data["jobId"])

for jobId in mathTargets:
    print(jobId)
    print(len(mathTargets[jobId]))
    if jobId in data["jobId"]:
        index = data["jobId"].index(jobId)
        data["nTargetsMath"][index] = len(mathTargets[jobId])

print(data)

with open("statData.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
outfile.close()

df = pd.DataFrame(data)
print(df.shape)
#fig = px.line_polar(df.loc("JBCoif030"), r=["nTargetsGerman_Sprechen", "nTargetsGerman_Schreiben", "nTargetsGerman_Hören", "nTargetsGerman_Lesen"], theta=["Sprechen", "Schreiben", "Hören", "Lesen"], line_close=True)
#fig.show()            

#quit()

fig = px.scatter(df, x="nTargetsGerman", y="nTargetsMath", hover_data=["jobName"], color="Level")
fig.show()