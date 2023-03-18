import pandas as pd
import graphviz as gv
from io import StringIO

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
        self.pickedMutexes = []
        self.currentValue = 0
        self.currentDuration = duration
        
    def checkActivity(self, withAlreadyRunning=True):
        # check if activity is already running or (if all incoming semaphores are active and all mutexes are free)
        if withAlreadyRunning and (self.currentValue > 0 or self.checkAllIncomingSemaphores()):
            # pick mutexes
            if self.checkAllMutexes():
                self.runActivity()
        elif not withAlreadyRunning and self.checkAllIncomingSemaphores():
            # pick mutexes
            if self.checkAllMutexes():
                self.runActivity(withAlreadyRunning)
        
    def runActivity(self, withAlreadyRunning=True):
        if withAlreadyRunning:
            self.currentValue = 1
            if self.currentDuration > 0:
                self.currentDuration -= 1
            else:
                self.currentValue = 0
                self.currentDuration = self.duration
                self.releaseSemaphores()
                self.releaseMutexes()
                self.activateOutgoingSemaphores()
        else:
            if self.currentValue <= 0:
                self.currentValue = 1
                if self.currentDuration > 0:
                    self.currentDuration -= 1
                else:
                    # possibility, if there is an activity with duration 0
                    self.currentValue = 0
                    self.currentDuration = self.duration
                    self.releaseSemaphores()
                    self.releaseMutexes()
                    self.activateOutgoingSemaphores()
            
    
    def checkAllIncomingSemaphores(self):
        # check if all incoming semaphores are active
        flag = True
        semaphoresIN = self.semaphoresIN.copy()
        
        while flag and len(semaphoresIN) != 0:
            semaphoreIN = semaphoresIN.pop(0)
            # if there is a group, check if one of the semaphores is active
            if len(semaphoreIN.groupWith) != 0:
                if semaphoreIN.currentValue <= 0:
                    for groupSemaphore in semaphoreIN.groupWith:
                        if groupSemaphore.currentValue > 0:
                            break
                        
                        if groupSemaphore == semaphoreIN.groupWith[-1]:
                            flag = False
                            break
                if flag:
                    for groupSemaphore in semaphoreIN.groupWith:
                        semaphoresIN.remove(groupSemaphore)
            elif semaphoreIN.currentValue == 0:
                flag = False
                break
        
        return flag

    def checkAllMutexes(self):
        # TODO: check if all incoming mutexes are free or picked by this activity
        for mutex in self.mutexes:
            if mutex.pickedBy != None and mutex.pickedBy != self:
                return False
        
        for mutex in self.mutexes:
            if mutex not in self.pickedMutexes:
                self.pickMutex(mutex)
        # return true if all mutexes could be picked
        return True
    
    def releaseSemaphores(self):
        for semaphoreIN in self.semaphoresIN:
                semaphoreIN.currentValue = 0
    
    def releaseMutexes(self):
        for mutex in self.pickedMutexes:
            mutex.pickedBy = None
        self.pickedMutexes = []
            
    def pickMutex(self, mutex):
        self.pickedMutexes.append(mutex)
        mutex.pickedBy = self
    
    def activateOutgoingSemaphores(self):
        for semaphoreOUT in self.semaphoresOUT:
            semaphoreOUT.currentValue = 1

class Mutex:
    def __init__(self, ID, name, activities):
        self.ID = ID
        self.name = name
        self.activities = activities
        self.pickedBy = None

class Semaphore:
    def __init__(self, ID, name, groupWith, initialValue, activityIN, activityOUT):
        self.ID = ID
        self.name = name
        self.groupWith = groupWith
        self.initialValue = initialValue
        self.activityIN = activityIN
        self.activityOUT = activityOUT
        self.currentValue = 0

tasks_IDs = []
tasks = []

activities_IDs = []
activities = []

semaphore_IDs = []
semaphores = []

mutex_IDs = []
mutexs = []

historyOfDigraphs = []
cursor = 0

def openFromCSV(content=None, Path=None):
    # content for real use, Path for testing and development
    
    erasePreviousData()

    if content != None:
        df = pd.read_csv(StringIO(content), sep=',')
    else:
        df = pd.read_csv(Path, sep=',')

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

    for index, row in df.iterrows():
        # first: instantiation of objects
        if row["Task_ID"] not in tasks_IDs:
            tasks_IDs.append(row["Task_ID"])
            tasks.append(Task(row["Task_ID"], row["Task_Name"], []))
        
        if row["Activity_ID"] not in activities_IDs:
            activities_IDs.append(row["Activity_ID"])
            activities.append(Activity(row["Activity_ID"], row["Activity_Name"], row["Activity_Duration"], [], row["Predecessor_Semaphore_ID"], [], []))
            print(row["Predecessor_Semaphore_ID"])
        
        # semaphoren anhand der VorgängerID erstellen, nicht anhand der herausgehenden ID
        for index, semaphore_ID in enumerate(row["Semaphore_ID"]):
            if semaphore_ID != "None" and semaphore_ID not in semaphore_IDs:
                semaphore_IDs.append(semaphore_ID)
                semaphores.append(Semaphore(semaphore_ID, row["Semaphore_Name"][index], [], int(row["Semaphore_Initial_Value"][index]), [], []))
            
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
                    print(semaphore_id)
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
                    print(semaphore_ids)
            
            # if end equals ']' -> end of or)
            
            # else -> and
            else:
                activity.semaphoresIN.append(semaphores[semaphore_IDs.index(semaphore_id)])
                semaphores[semaphore_IDs.index(semaphore_id)].activityIN = activity
                print(semaphore_id)
                
def erasePreviousData():
    global activities, activities_IDs, tasks, tasks_IDs, semaphores, semaphore_IDs, mutexs, mutex_IDs, dot, cursor, historyOfDigraphs
    activities = []
    activities_IDs = []
    tasks = []
    tasks_IDs = []
    semaphores = []
    semaphore_IDs = []
    mutexs = []
    mutex_IDs = []
    dot = None
    cursor = 0
    historyOfDigraphs = []

# mmaybe pass ID of activity, semaphore that you want to color for the animation

ACTIVITY_RUNNING = 'green'
SEMAPHORE_ACTIVE = 'red'

def createRects(color, inverseColor):
    for activity in activities:
        fillcolor = 'transparent'
        fontcolor = inverseColor
        if activity.currentValue > 0:
            fillcolor = ACTIVITY_RUNNING
            fontcolor = 'black'
        dot.node("Activity"+str(activity.ID), shape='record', style='rounded,filled', label='{'+activity.parentTask.name+'|'+activity.name+'}', color=inverseColor, fontcolor=fontcolor, fillcolor=fillcolor)
        
def createMutexs(color, inverseColor):
    fillcolor = 'transparent'
    for mutex in mutexs:
        dot.node("Mutex"+str(mutex.ID), shape='polygon', sides='5', label=mutex.name, color=inverseColor, fontcolor=inverseColor, fillcolor=fillcolor)
        for activity in mutex.activities:
            dot.edge("Mutex"+str(mutex.ID), "Activity"+str(activity.ID), arrowhead='none', style='dashed', splines='polyline', color=inverseColor)
        
def createSemaphores(color, inverseColor):
    global dummyCounter
    
    # add color just like in createRects
    
    semaphores_buf = semaphores.copy()
    while len(semaphores_buf) != 0:
        
        semaphore = semaphores_buf.pop(0)
        
        color = inverseColor
        if semaphore.currentValue > 0:
            color = SEMAPHORE_ACTIVE
            
        # if semaphore has groupWith, connect those semaphores together. Those will then be erased from the list
        if len(semaphore.groupWith) != 0:
            
            # draw semaphores
            middleDummyName = "Dummy" + str(dummyCounter)
            dot.node(middleDummyName, shape='point', width="0.01", height="0.01", color=color)
            dummyCounter += 1
            
            # first the semaphore itself
            if semaphore.initialValue > 0:
                    # this is the edge with a point in the middle
                    dot.node("Dummy" + str(dummyCounter), shape='point', width="0.01", height="0.01", color=color)
                    dot.edge("Activity"+str(semaphore.activityOUT.ID), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline', color=color)
                    dot.edge("Dummy" + str(dummyCounter), middleDummyName, label=semaphore.name, arrowhead='none', splines='polyline', color=color, fontcolor=inverseColor)
                    dummyCounter += 1
                    
                    # this is this init-thing (edge with point at the end)
                    dot.node("Dummy" + str(dummyCounter), shape='point', xlabel=(lambda valorem: '' if valorem == 1 else str(valorem))(semaphore.initialValue), color=color, fontcolor=inverseColor)
                    dot.edge("Dummy" + str(dummyCounter-1), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline', color=color)
                    dummyCounter += 1
            else:
                dot.edge("Activity"+str(semaphore.activityOUT.ID), middleDummyName, label=semaphore.name, arrowhead='none', splines='polyline', color=color, fontcolor=inverseColor)
            
            # after the groupSemaphores
            colorOfLastSemaphore = color
            for groupSemaphore in semaphore.groupWith:
                if groupSemaphore.currentValue > 0:
                    color = SEMAPHORE_ACTIVE
                    colorOfLastSemaphore = SEMAPHORE_ACTIVE
                else:
                    color = inverseColor
                
                if groupSemaphore.initialValue > 0:
                    # this is the edge with a point in the middle
                    dot.node("Dummy" + str(dummyCounter), shape='point', width="0.01", height="0.01", color=color)
                    dot.edge("Activity"+str(groupSemaphore.activityOUT.ID), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline', color=color)
                    dot.edge("Dummy" + str(dummyCounter), middleDummyName, label=groupSemaphore.name, arrowhead='none', splines='polyline', color=color, fontcolor=inverseColor)
                    dummyCounter += 1
                    
                    # this is this init-thing (edge with point at the end)
                    dot.node("Dummy" + str(dummyCounter), shape='point', xlabel=(lambda valorem: '' if valorem == 1 else str(valorem))(groupSemaphore.initialValue), color=color, fontcolor=inverseColor)
                    dot.edge("Dummy" + str(dummyCounter-1), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline', color=color)
                    dummyCounter += 1
                else:
                    dot.edge("Activity"+str(groupSemaphore.activityOUT.ID), middleDummyName, label=groupSemaphore.name, arrowhead='none', splines='polyline', color=color, fontcolor=inverseColor)
                
                semaphores_buf.remove(groupSemaphore)
                
            dot.node(middleDummyName, shape='point', width="0.01", height="0.01", color=colorOfLastSemaphore)
            dot.edge(middleDummyName, "Activity"+str(semaphore.activityIN.ID), arrowhead='normal', splines='polyline', color=colorOfLastSemaphore)
            
        else:
            # if semaphore is leading to the same task where it came from, use another arrowhead
            if semaphore.activityIN.parentTask.ID == semaphore.activityOUT.parentTask.ID:
                # if semaphore has an initial value, connect an edge to the semaphore
                if semaphore.initialValue > 0:
                    dot.node("Dummy" + str(dummyCounter), shape='point', width="0.01", height="0.01", color=color)
                    dot.edge("Activity"+str(semaphore.activityOUT.ID), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline', color=color)
                    dot.edge("Dummy" + str(dummyCounter), "Activity"+str(semaphore.activityIN.ID), label=semaphore.name, arrowhead='onormal', splines='polyline', color=color, fontcolor=inverseColor)
                    dummyCounter += 1
                    dot.node("Dummy" + str(dummyCounter), shape='point', xlabel=(lambda valorem: '' if valorem == 1 else str(valorem))(semaphore.initialValue), color=color, fontcolor=inverseColor)
                    dot.edge("Dummy" + str(dummyCounter-1), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline', color=color)
                    dummyCounter += 1
                else:
                    dot.edge("Activity"+str(semaphore.activityOUT.ID), "Activity"+str(semaphore.activityIN.ID), label=semaphore.name, arrowhead='onormal', splines='polyline', color=color, fontcolor=inverseColor)
            else:
                if semaphore.initialValue > 0:
                    dot.node("Dummy" + str(dummyCounter), shape='point', width="0.01", height="0.01", color=color)
                    dot.edge("Activity"+str(semaphore.activityOUT.ID), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline', color=color)
                    dot.edge("Dummy" + str(dummyCounter), "Activity"+str(semaphore.activityIN.ID), label=semaphore.name, splines='polyline', color=color, fontcolor=inverseColor)
                    dummyCounter += 1
                    dot.node("Dummy" + str(dummyCounter), shape='point', xlabel=(lambda valorem: '' if valorem == 1 else str(valorem))(semaphore.initialValue), color=color, fontcolor=inverseColor)
                    dot.edge("Dummy" + str(dummyCounter-1), "Dummy" + str(dummyCounter), arrowhead='none', splines='polyline', color=color)
                    dummyCounter += 1
                else:
                    dot.edge("Activity"+str(semaphore.activityOUT.ID), "Activity"+str(semaphore.activityIN.ID), label=semaphore.name, splines='polyline', color=color, fontcolor=inverseColor)

def getNextFrame():
    # try to initialize semaphores
    startPoints = getAllStartPoints()
    
    for startPoint in startPoints:
        if startPoint.currentValue <= 0:
            startPoint.currentValue = 1
            startPoint.initialValue -= 1
            
    # activities sorted by ID
    activitiesSorted = sorted(activities, key=lambda activity: activity.ID)
    
    for activity in activitiesSorted:
        activity.checkActivity()

    for activity in activitiesSorted[:-1]:
        activity.checkActivity(False)

def getAllStartPoints():
    # get all activities that have no predecessor
    startPoints = []
    for semaphore in semaphores:
        if semaphore.initialValue > 0:
            startPoints.append(semaphore)
            
    return startPoints

# just a helper method
# def createNextImage(color='white', inverseColor='black', display=False):
#     getNextFrame()
#     return getCurrentImage(color, inverseColor, display)
    
def initGlobals():
    global dot
    dot = gv.Digraph(comment='Flowchart')
    dot.graph_attr.update(bgcolor='transparent')
    global dummyCounter
    dummyCounter = 0
    
# def getCurrentImage(color='white', inverseColor='black', display=False):
#     global dot
#     global dummyCounter
    
#     initGlobals()
    
#     createRects(color, inverseColor)
#     createMutexs(color, inverseColor)
#     createSemaphores(color, inverseColor)
    
#     # only for testing and development
#     if display:
#         dot.view()
#     return dot.pipe(format='svg')

def getImage(color='white', inverseColor='black', step=0, display=False):
    # macro method to generate an image, no matter if backward, forward or current
    global historyOfDigraphs
    global cursor
    global dot
    global dummyCounter
    
    #check if first image is requested
    if dot == None:
        initGlobals()
        
        createRects(color, inverseColor)
        createMutexs(color, inverseColor)
        createSemaphores(color, inverseColor)
        historyOfDigraphs.append(dot)
        
    if cursor+step <= len(historyOfDigraphs)-1 and cursor+step >= 0:
        dot = historyOfDigraphs[cursor+step]
    elif cursor+step < 0:
        dot = historyOfDigraphs[0]
    elif cursor+step > len(historyOfDigraphs)-1:
        for _ in range(cursor+step - (len(historyOfDigraphs)-1)):
            getNextFrame()
            
            initGlobals()
    
            createRects(color, inverseColor)
            createMutexs(color, inverseColor)
            createSemaphores(color, inverseColor)
            historyOfDigraphs.append(dot)
    
    cursor = (lambda x: 0 if x < 0 else x)(cursor+step)
    
    if dot != None:
        if display:
            dot.view()
        return dot.pipe(format='svg')