## Index
# 11 - Importing Libraries
# 19 - Defining Classes
# 32 - Defining Function
# 658 - Initializing the Variables
# 680 - Intermediate Calculations
# 695 - Creating Initial World
# 711 - Starting the Interaction Process
# 754 - Plotting the Results

# Importing Libraries
import numpy as np
import matplotlib.pyplot as plt
import time

## Time Taken for Simulation
Start_Time = time.time()

## Defining Classes
class Agent:
    def __init__(self, id, Category, Home, Work, Time_Till_Isolation, Immunity, Time_Till_Recovery, Infection_Status, Vaccination_Status):
        self.id = id
        self.Category = Category  # Categories (MH, SE, CE, ST, HW, SP)
        self.Home = Home  # (i,j)
        self.Work = Work  # (i, j)
        self.Time_Till_Isolation = Time_Till_Isolation  # (default = 3)
        self.Immunity = Immunity
        self.Time_Till_Recovery = Time_Till_Recovery # (default = 3)
        self.Infection_Status = Infection_Status # (default = 0[Non-Infected], 1[Infected], 2[Isolation], 3[Death])
        self.Vaccination_Status = Vaccination_Status # (default = 0[Non-Vaccinated], 1[Partially Vaccinated], 2[Completely Vaccinated])

## Defining Functions

def Home_Loc(N, Grid):
    Home_loc = []
    for i in range(N):
        loc = np.random.randint(1, Grid + 1, size=2)
        loc = np.split(loc, 2)
        temp = [loc[0][0], loc[1][0]]
        if temp not in Home_loc:
            Home_loc.append(temp)   
    
    return Home_loc

def Work_Loc(N, Home):
    Work_loc = []
    count = 0
    while count < N:
        loc = np.random.randint(1, Grid + 1, size=2)
        loc = np.split(loc, 2)
        temp = [loc[0][0], loc[1][0]]
        if temp not in Home:
            if temp not in Work_loc:
                Work_loc.append(temp)
            count += 1

    return Work_loc

def Agent_init(n):
    Array = np.array([])
    for i in range(n):
        Category = np.random.randint(6)
        Home = np.random.choice(len(Home_Locations))
        Home = Home_Locations[Home]
        if Category > 1:
            Work = np.random.choice(len(Work_Locations))
            Work = Work_Locations[Work]
        else:
            Work = None
        temp = Agent(i, Category, Home, Work, 
                     Time_Till_Isolation = TTI, 
                     Immunity = 1, 
                     Time_Till_Recovery = TTR, 
                     Infection_Status = 0, 
                     Vaccination_Status = 0)
        Array = np.append(Array, temp)
    
    return Array

def Neighbour(x):
    m1 = [x[0] - 1, x[1] - 1]
    m2 = [x[0], x[1] - 1]
    m3 = [x[0] + 1, x[1] - 1]
    m4 = [x[0] - 1, x[1]]
    m5 = [x[0] + 1, x[1]]
    m6 = [x[0] - 1, x[1] + 1]
    m7 = [x[0], x[1]]
    m8 = [x[0] + 1, x[1] + 1]
    temp = [m1, m2, m3, m4, m5, m6, m7, m8]
    return temp

def Distance(a, b):
    dist = np.square(a.Home[0] - b.Home[0]) + np.square(a.Home[1] - b.Home[1])
    temp = np.sqrt(dist) # * Grid
    return temp

def Probability(x):
    temp = np.random.randint(1, 10000)
    #print(temp)
    if temp < x:
        return True
    else: 
        return False

def Uni_Prob_Interaction(a, b):
    if a.Home == b.Home:
        return p_high
    elif a.Home in Neighbour(b.Home):
        return p_medium

def Uni_Str_Interaction(A1, A2):
    if A1.Home == A2.Home:
        if A2.Vaccination_Status == 0:
            return s_high * A2.Immunity
        elif A2.Vaccination_Status == 1:
            return s_high * A2.Immunity * 0.5
        else:
            return 0

def Recovery_Death(A1):
    temp = np.random.randint(1, 10000)
    
    if temp < 9900:
        A1.Infection_Status = 0
        A1.Immunity = A1.Immunity * Recovery_Constant
        A1.Time_Till_Isolation = TTI
        A1.Time_Till_Recovery = TTR
        
    else: 
        A1.Infection_Status = 3

def Initial_Infected(N):
    select = np.random.choice(Population_Size, size = N)
    for i in select:
        Population[i].Infection_Status = 1

def POI(A1, A2):
    if A1.Work == A2.Work and A1.Work != None:
        return p_high
    temp = Uni_Prob_Interaction(A1, A2)
    if temp != None:
        return temp
    else:
        dist = Distance(A1, A2)
        if dist < 5:
            return P_Matrix[A1.Category][A2.Category] / dist
        else:
            return p_low / dist

def SOI(A1, A2):
    temp = Uni_Str_Interaction(A1, A2)
    if temp != None:
        return temp * A2.Immunity
    else:
        return S_Matrix[A1.Category][A2.Category] * A2.Immunity
    

## Initailizing Variables

#Categories: 0 = MH, 1 = SE, 2 = CE, 3 = ST, 4 = HW, 5 = SP

Grid = 20
Population_Size = 1000
Initial_Infected_Population = 1

TTI = 3    # Time Till Isolation
TTR = 10   # Time Till Recovery

Strength = 1000    # Co-efficient of Strength of Interaction
Probab = 1500      # Co-efficient of Probability of Interaction

Recovery_Constant = 0.5   # Degree of Change in Immunity After Recovering from the infection 

Total_Simulation_Time = 100

Vaccination_StartTime = 50
Daily_Vaccination = 50


## Intermediate Calculations

s_high = Strength
s_medium = Strength * (2/3)
s_low = Strength * (1/3)

p_high = Probab
p_medium = Probab * (2/3)
p_low = Probab * (1/3)

P_Matrix = [[p_low, p_medium, p_low,  p_medium, p_low, p_medium],
            [p_medium, p_low, p_medium,  p_medium, p_medium, p_low],
            [p_low, p_medium, p_low,  p_medium, p_low, p_low],
            [p_medium, p_medium, p_medium,  p_low, p_medium, p_low],
            [p_low, p_medium, p_low,  p_medium, p_medium, p_low],
            [p_medium, p_low, p_low,  p_low, p_low, p_low]]

S_Matrix = [[s_low, s_low, s_low, s_high, s_medium, s_medium],
            [s_low, s_low, s_low, s_high, s_medium, s_low],
            [s_low, s_low, s_low, s_high, s_low, s_low],
            [s_high, s_high, s_high, s_medium, s_medium, s_medium],
            [s_medium, s_medium, s_low, s_medium, s_low, s_low],
            [s_medium, s_low, s_low, s_high, s_low, s_low]]

day = 0

Daily_Count = [[day, Initial_Infected_Population]]


## Creating the Initial World

Home_Ratio = int(Grid * Grid * 0.8)          # Ratio of Homes in the Given Area
Home_Locations = Home_Loc(Home_Ratio, Grid)

Work_Ratio = int(Grid * Grid * 0.2)         # Ratio of Work Locations in the Given Area
Work_Locations = Work_Loc(Work_Ratio, Home_Locations)

Population = Agent_init(Population_Size)    # Initailize the Agents in the Population

Initial_Infected(Initial_Infected_Population)   # Number of Infected Agents at the Start of Simulation


## Starting the Interaction Process

while day < Total_Simulation_Time:
    day += 1
    # Introducing Vaccination
    if day > Vaccination_StartTime:
        vaccinate = np.random.choice(Population, Daily_Vaccination)
        for x in vaccinate:
            if x.Vaccination_Status == 0:
                x.Vaccination_Status = 1
                x.Immunity = x.Immunity * 0.5
            elif x.Vaccination_Status == 1:
                x.Vaccination_Status = 2
                x.Immunity = 0

    Infected = []      # Temporary list for Infected Population
    Non_Infected = []  # Temporary list for Non-Infected Population

    for y in Population:          # Seggregating the Population into temporary list
        if y.Infection_Status == 0:
            Non_Infected.append(y)
        elif y.Infection_Status == 1:
            Infected.append(y)
        elif y.Infection_Status == 2:
            y.Time_Till_Recovery -= 1    # Recovery Time Calculation
            if y.Time_Till_Recovery == 0:
                Recovery_Death(y)

    for i in Infected:          # Actual Interaction
        for j in Non_Infected:
            if Probability(POI(i, j)) is True:
                if Probability(SOI(i, j)) is True:
                    j.Infection_Status = 1
        
        i.Time_Till_Isolation -= 1      # Isolation Time Calculation
        if i.Time_Till_Isolation == 0:
            i.Infection_Status = 2
    
    Daily_Count.append([day, len(Infected)])   # Daily count of Number of Infected Agents
    
# Time Taken for Simulation
End_Time = time.time()
print("Time Taken for Simulation = ", End_Time - Start_Time)

#print(Daily_Count)


## Plotting the Results

plt.figure(dpi = 100)

count = []
infected = []
for i in Daily_Count:
    count.append(i[0])
    infected.append(i[1])

plt.plot(np.array(count),np.array(infected))

plt.title('Curve of Growth of Infection w.r.t. Time')
plt.xlabel('Number of Days')
plt.ylabel('Total Number of Infected Agents')


plt.show()

    
