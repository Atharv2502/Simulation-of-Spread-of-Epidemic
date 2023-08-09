# Importing Libraries
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt

# Defining Variables

Grid = 10          # Size of the Grid

Population = 1000

p_high = 30        # Strength of Interaction
p_medium = 20
p_low = 10

high = 15          # Probability of Interaction
medium = 10
low = 5

# Home : Work ratio = 9 : 1

Day = 0
Simulation_Time = 25

# Database
Categories = ["MH", "SE", "CE", "ST", "HW", "SP"]
Agents = []
Non_Infected = []
Infected = []
Recovered = []
Death = []
Daily_Count = []

# Defining Classes

class Agent:
    def __init__(self, id, Category, Home, Work, Time_Till_Isolation):
        self.id = id
        self.Category = Category  # Categories (MH, SE, CE, ST, HW, SP)
        self.Home = Home  # (i,j)
        self.Work = Work  # (i, j)
        self.Time_Till_Isolation = Time_Till_Isolation  # (default time = 3)

# Defining Functions

def Agent_init(n, lis):
    for i in range(n):
        cat = np.random.choice(Categories)
        Home = np.random.choice(len(Home_Locations))
        Home = Home_Locations[Home]
        Work = np.random.choice(len(Work_Locations))
        Work = Work_Locations[Work]
        temp = Agent(i, cat, Home, Work, Time_Till_Isolation = 3)
        lis.append(temp)

def Home_loc(N):
    Home_loc = []
    for i in range(N):
        loc = np.random.randint(1, Grid + 1, size=2)
        loc = np.split(loc, 2)
        temp = [loc[0][0], loc[1][0]]
        if temp not in Home_loc:
            Home_loc.append(temp)

    return Home_loc

def Work_loc(N, Home):
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
    temp = np.sqrt(dist)
    return temp

def Probability(x):
    temp = np.random.randint(1, 100)
    #print(temp)
    if temp < x:
        return True
    else: 
        return False

def Uni_Prob_Interaction(a, b):
    if a.Home == b.Home:
        return high
    elif a.Home in Neighbour(b.Home):
        return medium
    
def Uni_Str_Interaction(a, b):
    if a.Home == b.Home:
        return p_high

def Choice(a, b):
    if a.Category == "MH" and b.Category == "MH":
        return 'AA'
    elif a.Category == "MH" and b.Category == "SE":
        return 'AB'
    elif a.Category == "MH" and b.Category == "CE":
        return 'AC'
    elif a.Category == "MH" and b.Category == "HW":
        return 'AD'
    elif a.Category == "MH" and b.Category == "ST":
        return 'AE'
    elif a.Category == "MH" and b.Category == "SP":
        return 'AF'
    elif a.Category == "SE" and b.Category == "MH":
        return 'AB'
    elif a.Category == "SE" and b.Category == "SE":
        return 'BB'
    elif a.Category == "SE" and b.Category == "CE":
        return 'BC'
    elif a.Category == "SE" and b.Category == "HW":
        return 'BD'
    elif a.Category == "SE" and b.Category == "ST":
        return 'BE'
    elif a.Category == "SE" and b.Category == "SP":
        return 'BF'
    elif a.Category == "CE" and b.Category == "MH":
        return 'AC'
    elif a.Category == "CE" and b.Category == "SE":
        return 'BC'
    elif a.Category == "CE" and b.Category == "CE":
        return 'CC'
    elif a.Category == "CE" and b.Category == "HW":
        return 'CD'
    elif a.Category == "CE" and b.Category == "ST":
        return 'CE'
    elif a.Category == "CE" and b.Category == "SP":
        return 'CF'
    elif a.Category == "HW" and b.Category == "MH":
        return 'AD'
    elif a.Category == "HW" and b.Category == "SE":
        return 'BD'
    elif a.Category == "HW" and b.Category == "CE":
        return 'CD'
    elif a.Category == "HW" and b.Category == "HW":
        return 'DD'
    elif a.Category == "HW" and b.Category == "ST":
        return 'DE'
    elif a.Category == "HW" and b.Category == "SP":
        return 'DF'
    elif a.Category == "ST" and b.Category == "MH":
        return 'AE'
    elif a.Category == "ST" and b.Category == "SE":
        return 'BE'
    elif a.Category == "ST" and b.Category == "CE":
        return 'CE'
    elif a.Category == "ST" and b.Category == "HW":
        return 'DE'
    elif a.Category == "ST" and b.Category == "ST":
        return 'EE'
    elif a.Category == "ST" and b.Category == "SP":
        return 'EF'
    elif a.Category == "SP" and b.Category == "MH":
        return 'AF'
    elif a.Category == "SP" and b.Category == "SE":
        return 'BF'
    elif a.Category == "SP" and b.Category == "CE":
        return 'CF'
    elif a.Category == "SP" and b.Category == "HW":
        return 'DF'
    elif a.Category == "SP" and b.Category == "ST":
        return 'EF'
    elif a.Category == "SP" and b.Category == "SP":
        return 'FF'

def Distance_Factor(type, A1, A2):
    dist = Distance(A1, A2)
    temp = int(type / dist)
    return temp

def Probability_of_Interaction(A1, A2):
    choice = Choice(A1, A2)

    if choice == 'AA':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return Distance_Factor(low, A1, A2)
        
    elif choice == 'AB':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            if Distance(A1, A2) < 2:
                return Distance_Factor(medium, A1, A2)
            else:
                return Distance_Factor(low, A1, A2)
            
    elif choice == 'AC':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return Distance_Factor(low, A1, A2)
        
    elif choice == 'AD':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            if Distance(A1, A2) < 2:
                return Distance_Factor(medium, A1, A2)
            else:
                return Distance_Factor(low, A1, A2)
            
    elif choice == 'AE':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return Distance_Factor(low, A1, A2)
        
    elif choice == 'AF':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            if Distance(A1, A2) < 2:
                return Distance_Factor(medium, A1, A2)
            else:
                return Distance_Factor(low, A1, A2)
    
    elif choice == 'BB':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return Distance_Factor(low, A1, A2)
        
    elif choice == 'BC':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            if Distance(A1, A2) < 2:
                return Distance_Factor(medium, A1, A2)
            else:
                return Distance_Factor(low, A1, A2)
            
    elif choice == 'BD':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            if Distance(A1, A2) < 2:
                return Distance_Factor(medium, A1, A2)
            else:
                return Distance_Factor(low, A1, A2)
            
    elif choice == 'BE':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            if Distance(A1, A2) < 2:
                return Distance_Factor(medium, A1, A2)
            else:
                return Distance_Factor(low, A1, A2)
            
    elif choice == 'BF':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return Distance_Factor(low, A1, A2)
    
    elif choice == 'CC':
        temp = Uni_Prob_Interaction(A1, A2)
        if A1.Work == A2.Work:
            return high
        elif temp != None:
            return temp
        else:
            return Distance_Factor(low, A1, A2)
        
    elif choice == 'CD':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            if Distance(A1, A2) < 2:
                return Distance_Factor(medium, A1, A2)
            else:
                return Distance_Factor(low, A1, A2)
            
    elif choice == 'CE':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return Distance_Factor(low, A1, A2)
        
    elif choice == 'CF':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return Distance_Factor(low, A1, A2)
        
    elif choice == 'DD':
        temp = Uni_Prob_Interaction(A1, A2)
        if A1.Work == A2.Work:
            return high
        elif temp != None:
            return temp
        else:
            return Distance_Factor(low, A1, A2)
    
    elif choice == 'DE':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            if Distance(A1, A2) < 2:
                return Distance_Factor(medium, A1, A2)
            else:
                return Distance_Factor(low, A1, A2)
            
    elif choice == 'DF':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return Distance_Factor(low, A1, A2)
    
    elif choice == 'EE':
        temp = Uni_Prob_Interaction(A1, A2)
        if A1.Work == A2.Work:
            return high
        elif temp != None:
            return temp
        else:
            if Distance(A1, A2) < 2:
                return Distance_Factor(medium, A1, A2)
            else:
                return Distance_Factor(low, A1, A2)
    
    elif choice == 'EF':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return Distance_Factor(low, A1, A2)
        
    elif choice == 'FF':
        temp = Uni_Prob_Interaction(A1, A2)
        if temp != None:
            return temp
        elif A1.Work == A2.Work:
            return medium
        else:
            return Distance_Factor(low, A1, A2)

def Strength_of_Interaction(A1, A2):
    choice = Choice(A1, A2)

    if choice == 'AA':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_low
        
    elif choice == 'AB':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_low
            
    elif choice == 'AC':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_low
        
    elif choice == 'AD':
        return p_high
            
    elif choice == 'AE':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_medium
        
    elif choice == 'AF':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_medium
    
    elif choice == 'BB':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_low
        
    elif choice == 'BC':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_low
            
    elif choice == 'BD':
            return p_high
            
    elif choice == 'BE':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_medium
            
    elif choice == 'BF':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_low
    
    elif choice == 'CC':
        temp = Uni_Str_Interaction(A1, A2)
        if A1.Work == A2.Work:
            return p_high
        elif temp != None:
            return temp
        else:
            return p_low
        
    elif choice == 'CD':
        return p_high
            
    elif choice == 'CE':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_low
        
    elif choice == 'CF':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_low
        
    elif choice == 'DD':
        temp = Uni_Str_Interaction(A1, A2)
        if A1.Work == A2.Work:
            return p_high
        elif temp != None:
            return temp
        else:
            return p_low
    
    elif choice == 'DE':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_medium
            
    elif choice == 'DF':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_medium
    
    elif choice == 'EE':
        temp = Uni_Str_Interaction(A1, A2)
        if A1.Work == A2.Work:
            return p_high
        elif temp != None:
            return temp
        else:
            return p_medium
    
    elif choice == 'EF':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_low
        
    elif choice == 'FF':
        temp = Uni_Str_Interaction(A1, A2)
        if temp != None:
            return temp
        else:
            return p_low

def Recovery_Death(a, Rcvry, Death):
    temp = np.random.randint(1, 100)
    if temp < 90:
        Rcvry.append(a)
    else: 
        Death.append(a)

def Check_Index(x, lis):
    for i in range(len(lis)):
        if lis[i] == x:
            return i


N1 = int(Grid * Grid * 0.9) #Number of Homes
Home_Locations = Home_loc(N1)
N2 = int(Grid * Grid * 0.1) # Number of Workplaces
Work_Locations = Work_loc(N2, Home_Locations)

Agent_init(Population, Non_Infected)

select = np.random.choice(len(Non_Infected), size = 1)
select = np.sort(select)[::-1]
for i in select:
    if i not in Infected:
        Infected.append(Non_Infected[i])
        Non_Infected.pop(i)


Daily_Count.append([Day, len(Infected), len(Non_Infected), len(Recovered), len(Death)])
while Day < Simulation_Time:
    Daily_Infected = []
    for i in Infected:
        for j in Non_Infected:
            if Probability(Probability_of_Interaction(i, j)) is True:
                if Probability(Strength_of_Interaction(i, j)) is True:
                    Daily_Infected.append(j)
                    curr = Check_Index(j, Non_Infected)
                    Non_Infected.pop(curr)
        i.Time_Till_Isolation -= 1
        if i.Time_Till_Isolation == 0:
            buff = Check_Index(i, Infected)
            Infected.pop(buff)
            Recovery_Death(i, Recovered, Death)
    for k in Daily_Infected:
        Infected.append(k)
    Day += 1
    Daily_Count.append([Day, len(Infected), len(Non_Infected), len(Recovered), len(Death)])

print(Daily_Count)


plt.figure(dpi=100)

# Creating an array from the list
count = []
infected = []
for i in Daily_Count:
    count.append(i[0]) 
    infected.append(i[1])
    print("(", i[0], " - ", i[1], ")", end=" ")

x = np.array(count)
y = np.array(infected)

# print(x)
# print(y)

# Plotting Numpy array
plt.plot(x,y)

# Adding details to the plot
plt.title('Plot NumPy array')
plt.xlabel('count')
plt.ylabel('infected')

# Displaying the plot
plt.show()