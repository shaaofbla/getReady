import json
import pandas as pd
import plotly.express as px


with open('germanElements.json', 'r') as file:
    elements = json.load(file) 

file.close()

with open('jobIdstoJobNames.json', 'r') as file:
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

data = {"jobId": [], "nTargetsGerman": [], "nTargetsMath": [], "jobName": []}

for jobId in germanTargets:
    print(jobId)
    print(len(germanTargets[jobId]))
    data["jobId"].append(jobId)
    data["nTargetsGerman"].append(len(germanTargets[jobId]))
    data["jobName"].append(profilesLabels[jobId])

print(data)
    
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

df = pd.DataFrame(data)

fig = px.scatter(df, x="nTargetsGerman", y="nTargetsMath", hover_data=["jobName"])
fig.show()