from flask import Flask, render_template
import os

from io import BytesIO
from PIL import Image

app = Flask(__name__)

class Task:
    def __init__(self, ID, name, activities):
        self.ID = ID
        self.name = name
        self.activities = activities

class Activity:
    def __init__(self, ID, name, duration, parentTask, semaphoresIN, semaphoresOUT, mutexes):
        self.ID = ID
        self.name = name
        self.duration = duration
        self.parentTask = parentTask
        self.semaphoresIN = semaphoresIN
        self.semaphoresOUT = semaphoresOUT
        self.mutexes = mutexes
        self.currentValue = 0
        self.currentDuration = duration

class Mutex:
    def __init__(self, ID, name, activities):
        self.ID = ID
        self.name = name
        self.activities = activities

class Semaphore:
    def __init__(self, ID, name, groupWith, initialValue, activityIN, activityOUT):
        self.ID = ID
        self.name = name
        self.groupWith = groupWith
        self.initialValue = initialValue
        self.activityIN = activityIN
        self.activityOUT = activityOUT
        self.currentValue = 0

dataFilePath = "src/frontend/dataTest2.csv"

data = []
linecells = []

import pandas as pd
df = pd.read_csv(dataFilePath, sep=',') 

# split seperated values into list elements
df["Semaphore_ID"] = df["Semaphore_ID"].astype(str)
df["Semaphore_ID"] = df["Semaphore_ID"].str.split(";")
df["Semaphore_Name"] = df["Semaphore_Name"].astype(str)
df["Semaphore_Name"] = df["Semaphore_Name"].str.split(";")
df["Semaphore_Initial_Value"] = df["Semaphore_Initial_Value"].astype(str)
df["Semaphore_Initial_Value"] = df["Semaphore_Initial_Value"].str.split(";")
df["Predecessor_Semaphore_ID"] = df["Predecessor_Semaphore_ID"].astype(str)
df["Predecessor_Semaphore_ID"] = df["Predecessor_Semaphore_ID"].str.split(";")
df["Mutex_ID"] = df["Mutex_ID"].astype(str)
df["Mutex_ID"] = df["Mutex_ID"].str.split(";")
df["Mutex_Name"] = df["Mutex_Name"].astype(str)
df["Mutex_Name"] = df["Mutex_Name"].str.split(";")


# only during the creation process of the tree
tasks_IDs = []
tasks = []

activities_IDs = []
activities = []

semaphore_IDs = []
semaphores = []

mutex_IDs = []
mutexs = []

for index, row in df.iterrows():
    # first: instantiation of objects
    if row["Task_ID"] not in tasks_IDs:
        tasks_IDs.append(row["Task_ID"])
        tasks.append(Task(row["Task_ID"], row["Task_Name"], []))
    
    if row["Activity_ID"] not in activities_IDs:
        activities_IDs.append(row["Activity_ID"])
        activities.append(Activity(row["Activity_ID"], row["Activity_Name"], row["Activity_Duration"], [], row["Predecessor_Semaphore_ID"], [], []))
    
    # semaphoren anhand der VorgängerID erstellen, nicht anhand der herausgehenden ID
    for index, semaphore_ID in enumerate(row["Semaphore_ID"]):
        if semaphore_ID != "None" and semaphore_ID not in semaphore_IDs:
            semaphore_IDs.append(semaphore_ID)
            semaphores.append(Semaphore(semaphore_ID, row["Semaphore_Name"][index], [], int(row["Semaphore_Initial_Value"][index]), None, None))
        
    for index, mutex_ID in enumerate(row["Mutex_ID"]):
        if mutex_ID != "None" and mutex_ID not in mutex_IDs:
            mutex_IDs.append(mutex_ID)
            mutexs.append(Mutex(mutex_ID, row["Mutex_Name"][index], []))
            
    # add semaphoreIN to activities and semaphores
    
    # secondly: linking of objects
    tasks[tasks_IDs.index(row["Task_ID"])].activities.append(activities[activities_IDs.index(row["Activity_ID"])])
    
    activities[activities_IDs.index(row["Activity_ID"])].parentTask = tasks[tasks_IDs.index(row["Task_ID"])]
    for semaphore_ID in row["Semaphore_ID"]:
        if semaphore_ID != "None":
            activities[activities_IDs.index(row["Activity_ID"])].semaphoresOUT.append(semaphores[semaphore_IDs.index(semaphore_ID)])
            semaphores[semaphore_IDs.index(semaphore_ID)].activityOUT = activities[activities_IDs.index(row["Activity_ID"])]
    for mutex_ID in row["Mutex_ID"]:
        if mutex_ID != "None":
            activities[activities_IDs.index(row["Activity_ID"])].mutexes.append(mutexs[mutex_IDs.index(mutex_ID)])
            mutexs[mutex_IDs.index(mutex_ID)].activities.append(activities[activities_IDs.index(row["Activity_ID"])])

# add semaphoreIN to activities and semaphores
for activity in activities:
    buf = activity.semaphoresIN
    activity.semaphoresIN = []
    while len(buf) > 0:
        semaphore_id = buf.pop(0)
        # if start equals '[' -> start of or)
        if semaphore_id[0] == '[':
            semaphore_id = semaphore_id[1:]
            
            if semaphore_id[-1] == ']':
                semaphore_id = semaphore_id[:-1]
                activity.semaphoresIN.append(semaphores[semaphore_IDs.index(semaphore_id)])
                semaphores[semaphore_IDs.index(semaphore_id)].activityIN = activity
            else:
                semaphore_ids = []
                while semaphore_id[-1] != ']':
                    semaphore_ids.append(semaphore_id)
                    semaphore_id = buf.pop(0)
                semaphore_ids.append(semaphore_id[:-1])
                for semaphore_id in semaphore_ids:
                    activity.semaphoresIN.append(semaphores[semaphore_IDs.index(semaphore_id)])
                    semaphores[semaphore_IDs.index(semaphore_id)].activityIN = activity
                    # set the groupWith value of the semaphores and add every semaphore to the group except for the current one
                    for semaphore in semaphore_ids:
                        if not semaphore == semaphore_id:
                            semaphores[semaphore_IDs.index(semaphore_id)].groupWith.append(semaphores[semaphore_IDs.index(semaphore)])
        
        # if end equals ']' -> end of or)
        
        # else -> and
        else:
            activity.semaphoresIN.append(semaphores[semaphore_IDs.index(semaphore_id)])
            semaphores[semaphore_IDs.index(semaphore_id)].activityIN = activity

import graphviz as gv
dot = gv.Digraph(comment='Flowchart')
dummyCounter = 0

def createRects():
    for activity in activities:
        color = 'white'
        if activity.currentValue > 0:
            color = 'green'
        dot.node(str(activity.ID), shape='record', style='rounded,filled', label='{'+activity.parentTask.name+'|'+activity.name+'}', fillcolor=color)
        
def createMutexs():
    for mutex in mutexs:
        dot.node(str(mutex.ID), shape='polygon', sides='5', label=mutex.name)
        for activity in mutex.activities:
            dot.edge(str(mutex.ID), str(activity.ID), arrowhead='none', style='dashed', splines='polyline')
        
def createSemaphores():
    global dummyCounter
    
    # add color just like in createRects
    
    semaphores_buf = semaphores.copy()
    while len(semaphores_buf) != 0:
        
        semaphore = semaphores_buf.pop(0)
        
        color = 'black'
        if semaphore.currentValue > 0:
            color = 'red'
            
        # if semaphore has groupWith, connect those semaphores together. Those will then be erased from the list
        if len(semaphore.groupWith) != 0:
            dot.node("Dummy" + str(dummyCounter), shape='point', width="0.01", height="0.01")
            middleDummy = "Dummy" + str(dummyCounter)
            
            # first the semaphore itself
            dot.edge(str(semaphore.activityOUT.ID), middleDummy, label=semaphore.name, arrowhead='none', splines='polyline')
            dot.edge(middleDummy, str(semaphore.activityIN.ID), arrowhead='normal', splines='polyline')
            dummyCounter += 1
            
            # after the groupSemaphores
            for groupSemaphore in semaphore.groupWith:
                dot.edge(str(groupSemaphore.activityOUT.ID), middleDummy, label=groupSemaphore.name, arrowhead='none', splines='polyline')
                semaphores_buf.remove(groupSemaphore)
        else:
            # if semaphore is leading to the same task where it came from, use another arrowhead
            if semaphore.activityIN.parentTask.ID == semaphore.activityOUT.parentTask.ID:
                # if semaphore has an initial value, connect an edge to the semaphore
                if semaphore.initialValue > 0:
                    dot.node("Dummy" + str(dummyCounter), shape='point', width="0.01", height="0.01")
                    dot.edge(str(semaphore.activityOUT.ID), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline', color=color)
                    dot.edge("Dummy" + str(dummyCounter), str(semaphore.activityIN.ID), label=semaphore.name, arrowhead='onormal', splines='polyline', color=color)
                    dummyCounter += 1
                    dot.node("Dummy" + str(dummyCounter), shape='point', xlabel=(lambda valorem: '' if valorem == 1 else str(valorem))(semaphore.initialValue))
                    dot.edge("Dummy" + str(dummyCounter-1), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline')
                    dummyCounter += 1
                else:
                    dot.edge(str(semaphore.activityOUT.ID), str(semaphore.activityIN.ID), label=semaphore.name, arrowhead='onormal', splines='polyline', color=color)
            else:
                if semaphore.initialValue > 0:
                    dot.node("Dummy" + str(dummyCounter), shape='point', width="0.01", height="0.01")
                    dot.edge(str(semaphore.activityOUT.ID), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline', color=color)
                    dot.edge("Dummy" + str(dummyCounter), str(semaphore.activityIN.ID), label=semaphore.name, splines='polyline', color=color)
                    dummyCounter += 1
                    dot.node("Dummy" + str(dummyCounter), shape='point', xlabel=(lambda valorem: '' if valorem == 1 else str(valorem))(semaphore.initialValue))
                    dot.edge("Dummy" + str(dummyCounter-1), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline')
                    dummyCounter += 1
                else:
                    dot.edge(str(semaphore.activityOUT.ID), str(semaphore.activityIN.ID), label=semaphore.name, splines='polyline', color=color)


historySemaphores = []

def getAllStartPoints():
    # get all activities that have no predecessor
    startPoints = []
    for semaphore in semaphores:
        if semaphore.initialValue > 0:
            startPoints.append(semaphore)
            
    return startPoints

def getActiveSemaphores():
    activeSemaphores = []
    for semaphore in semaphores:
        if semaphore.currentValue > 0:
            activeSemaphores.append(semaphore)
            
    return activeSemaphores

def getActiveActivities():
    activeActivities = []
    for activity in activities:
        if activity.currentValue > 0:
            activeActivities.append(activity)
            
    return activeActivities

def getNextFrame():
    # create a new image with highlighted nodes and edges (Tasks/Activities, Semaphores)
    startPoints = getAllStartPoints()
    
    # check if you can activate a new semaphore
    for startPoint in startPoints:
        if not startPoint.currentValue > 0:
            startPoint.currentValue = 1;
            startPoint.initialValue -= 1;
        # else: do nothing - wait for the semaphore to become free
        
    activeSemaphores = getActiveSemaphores()
        
    # check for the activities behind the active semaphores
    for activeSemaphore in activeSemaphores:
        # look, if the following activity is ready to run (all incoming semaphores == 1) or already running
        if not activeSemaphore.activityIN.currentValue > 0:
            # check if all incoming semaphores are active
            
            flag = True
            semaphoresIN = activeSemaphore.activityIN.semaphoresIN.copy()
            
            while flag and len(semaphoresIN) != 0:
                semaphoreIN = semaphoresIN.pop(0)
                # if there is a group, check if one of the semaphores is active
                if len(semaphoreIN.groupWith) != 0:
                    if not semaphoreIN.currentValue > 0:
                        for groupSemaphore in semaphoreIN.groupWith:
                            if groupSemaphore.currentValue > 0:
                                break
                            
                            if groupSemaphore == semaphoreIN.groupWith[-1]:
                                flag = False
                                break
                    if flag:
                        for groupSemaphore in semaphoreIN.groupWith:
                            semaphoresIN.delete(groupSemaphore)
                elif semaphoreIN.currentValue == 0:
                    flag = False
                    break
            
            if flag:
                activeSemaphore.activityIN.currentValue = 1
                
                
    activeActivities = getActiveActivities()
    
    for activeActivity in activeActivities:
        if activeActivity.currentDuration > 0: 
            activeActivity.currentDuration -= 1
        else:
            # next steps: activate all semaphores going out of the activity
            semaphoresIN = activeActivity.semaphoresIN
            for semaphoreIN in semaphoresIN:
                semaphoreIN.currentValue = 0
            activeActivity.currentValue = 0
            semaphoresOUT = activeActivity.semaphoresOUT
            for semaphoreOUT in semaphoresOUT:
                semaphoreOUT.currentValue = 1
                
            activeActivity.currentDuration = activeActivity.duration
            
    activeSemaphores = getActiveSemaphores()
        
    # check for the activities behind the active semaphores
    for activeSemaphore in activeSemaphores:
        # look, if the following activity is ready to run (all incoming semaphores == 1) or already running
        if not activeSemaphore.activityIN.currentValue > 0:
            # check if all incoming semaphores are active
            
            flag = True
            semaphoresIN = activeSemaphore.activityIN.semaphoresIN.copy()
            
            while flag and len(semaphoresIN) != 0:
                semaphoreIN = semaphoresIN.pop(0)
                # if there is a group, check if one of the semaphores is active
                if len(semaphoreIN.groupWith) != 0:
                    if not semaphoreIN.currentValue > 0:
                        for groupSemaphore in semaphoreIN.groupWith:
                            if groupSemaphore.currentValue > 0:
                                break
                            
                            if groupSemaphore == semaphoreIN.groupWith[-1]:
                                flag = False
                                break
                    if flag:
                        for groupSemaphore in semaphoreIN.groupWith:
                            semaphoresIN.delete(groupSemaphore)
                elif semaphoreIN.currentValue == 0:
                    flag = False
                    break
            
            if flag:
                activeSemaphore.activityIN.currentValue = 1
                

def saveInitialValuesSemaphores():
    # save the initial values of all semaphores
    for semaphore in semaphores:
        if semaphore.initialValue > 0:
            historySemaphores.append([semaphore.ID, semaphore.initialValue])

def reinitializeInitialValuesSemaphores():
    # set all semaphores back to their initial values
    for valorem in historySemaphores:
        semaphores[semaphore_IDs.index(valorem[0])].initialValue = valorem[1]

# just a helper method
def createNextFrame():
    getNextFrame()
    getCurrentImage()
    
@app.route("/next")
def getCurrentImage():
    global dot
    dot = gv.Digraph(format='jpg')
    global dummyCounter
    dummyCounter = 0
    
    createRects()
    createMutexs()
    createSemaphores()
    return(dot.render(view=False, filename=None, directory=None, outfile=None, format='jpg'))

@app.route("/")
def home():
    return render_template("./home.html")

if __name__ == "__main__":
    app.run(debug=True)