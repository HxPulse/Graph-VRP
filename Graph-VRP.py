import math

#########################################################################################################################################

# Functions used to gather the data stored in the txt files

#########################################################################################################################################

def gatherData():
    # Transforms the txt file into a Python table 
    file = open('Cities_5000.txt', "r")          # Cities_10000.txt for the 10k file
    list = []
    for line in file:
        list2 = []
        for word in line.split():
            list2.append(word)
        list.append(list2) 
    file.close()
    return list

def gatherData2():
    # Transforms the txt file into a Python table
    file = open('VRP_tempDB.txt', "r")
    list = []
    for line in file:
        list2 = []
        for word in line.split():
            list2.append(word)
        list.append(list2) 
    file.close()
    return list

def gatherData3():
    # Transforms the txt file into a Python table
    file = open('Cities_5000coord.txt', "r")        # Cities_10000coord.txt for the 10k file
    list = []
    for line in file:
        list2 = []
        for word in line.split():
            list2.append(word)
        list.append(list2) 
    file.close()
    return list



#########################################################################################################################################

# Functions used as tools for all the following methods

#########################################################################################################################################

def shortestPath(a):
    # Takes a city and finds the shortest path from this city to all the other using Dijkstra.
    file = gatherData()
    while file[0][0] != 'Edges':        # Reading the file and removing the unnecessary data.
        file.pop(0)
    file.pop(0)                         # Dijkstra algorithm adapted to python
    Z = []                              # Z = X - {s}
    for i in range(4978):               # 9495 if you take the file containing 10'000 cities
        if i == a:
            continue
        else:
            Z.append(i)

    lambdas = Z.copy()                  # Since Z = X - {s}, we're missing 1 lambda edge      
    lambdas.append(0)
    
    paths = [[] for i in range(len(lambdas))]         # In the paths table, we store at index x the shortest path found to go from our city to x
    
    print("Current target: City #" + str(a))
    for i in range(len(lambdas)):         # For i in Z do
                                                                    
        check = False
        
        for city in file:
        
            if (int(city[0]) == i and int(city[1]) == a) or (int(city[0]) == a and int(city[1]) == i):
                lambdas[i] = float(city[2])            # If (s, i) belongs to U, do lambda(i) = I((s, i)) 
                paths[i].append(a)
                paths[i].append(i)
                check = True

        if not check:                   # Otherwise lambda(i) = inf
            lambdas[i] = 10000          # We're here using inf = 10000 for simplicity, the biggest distance between two cities in France being at most 1000kms, this won't cause any issue   
                                        
    lambdas[a] = 0                      # lambda(s) = 0
    
    while Z != []:      # While Z != empty set, do
        
        mini = 100000        # Take x belonging to Z so that lambda(x) = min{lambda(j), j in Z}
        for i in Z:
            if lambdas[i] < mini:
                mini = lambdas[i]
                indexI = i
        
        vertex = Z.index(indexI)
        Z.pop(vertex)           # Z = Z - {x}
        
        for city in file:
            if (int(city[0]) != indexI and int(city[1]) != indexI):         # For i in Gamma+(x) and Z, do
                continue  
            
            # We are here dividing the test using 2 if because we're going through the file checking the links between two cities, and each line contains two cities (x->y and y->x)
            
            if int(city[0]) == indexI:                             # If the city is found first in the file line, we check the second city
                if int(city[1]) in Z and lambdas[indexI] + float(city[2]) < lambdas[int(city[1])]:      # If lambda(x) + I(x, i) < lambda(i), do lambda(i) = lambda(x) + I(x, i)  
                    lambdas[int(city[1])] = lambdas[indexI] + float(city[2])              
                    new_path = paths[indexI].copy()                                                  
                    paths[int(city[1])] = new_path
                    paths[int(city[1])].append(int(city[1]))

                     
            if int(city[1]) == indexI:                              # If the city is found second in the file line, we check the first city    
                if int(city[0]) in Z and lambdas[indexI] + float(city[2]) < lambdas[int(city[0])]:       
                    lambdas[int(city[0])] = lambdas[indexI] + float(city[2])
                    new_path = paths[indexI].copy()                 # We store the new parth by copying the previous one until the city we are currently checking
                    paths[int(city[0])] = new_path                  # And we change the path in the path table, adding the city we've just checked 
                    paths[int(city[0])].append(int(city[0]))
                 
    open("VRP_tempDB.txt", "w").close()      # Removing everything inside the file before writing in it  
    file2 = open('VRP_tempDB.txt', 'a')          
    for i in range(len(lambdas)):
        file2.write(str(lambdas[i]) + ' ' + str(paths[i]) + '\n')
    file2.close()
    
    return("City #" + str(a) + " done")

def asTheCrowFlies(a, b, coords):
    # Takes two cities and the coords file and returns the "as the crow flies" distance between these cities
    if float(coords[a][2]) == float(coords[b][2]) and float(coords[a][3]) == float(coords[b][3]):
        return 0            # Some cities are extremely close to one and other and therefore have the same coords in the file, that causes an issue with the calculations underneath
    delta = float(coords[a][2]) - float(coords[b][2])
    return(100 * (math.acos(
        math.sin(float(coords[a][3])) * math.sin(float(coords[b][3])) 
        + math.cos(float(coords[a][3])) * math.cos(float(coords[b][3])) * math.cos(delta))))


    
#########################################################################################################################################

# Dijkstra & A* implementations

#########################################################################################################################################

def dijkstra(a, b):
    # Takes two cities and finds the shortest path between these two cities using Dijkstra.
    
    # Unlike the previous function, this one only checks two cities instead of one with all the others
    # The main difference between this function and the one above can be found where 3 # are marked
    file = gatherData()
    while file[0][0] != 'Edges':
        file.pop(0)                     # Reading the file and removing useless information
    file.pop(0)                         
    Z = []                              # Z = X - {s}
    for i in range(4978):               # 9495 if you take the file containing 10'000 cities
        if i == a:
            continue
        else:
            Z.append(i)             

    lambdas = Z.copy()                  # Since Z = X - {s}, we're missing 1 lambda vertex              
    lambdas.append(0)
    
    paths = [[] for i in range(len(lambdas))]      # In the paths table, we store at index x the shortest path found to go from our city to x
    
    print("Current target: City #" + str(a) + ". Aiming for City #" + str(b) + "\n")
    print("Processing start links...")
    print("\n")
    for i in range(len(lambdas)):         # For i in Z, do
                                                                                      
        check = False
        
        for city in file:
        
            if (int(city[0]) == i and int(city[1]) == a) or (int(city[0]) == a and int(city[1]) == i):
                lambdas[i] = float(city[2])
                paths[i].append(a)                         # If (s, i) belongs to U, do lambda(i) = I((s, i)) 
                paths[i].append(i)
                check = True
                print("City #" + str(i) + " is linked to our start.")

        if not check:                       # Otherwise lambda(i) = inf
            lambdas[i] = 10000              # We're here using inf = 10000 for simplicity, the biggest distance between two cities in France being at most 1000kms, this won't cause any issue
            
    lambdas[a] = 0                          # lambda(s) = 0
    
    print("\n")
    print("Links done. Processing the next step...")
    print("\n")
    
    found_b = False             ### The boolean found_b seeks for the goal city, if it's the case, we get out of the algorithm asap. 
                                ### Hence the difference with the previous function.
                                
    while not found_b:          # While Z != empty set, do
        
        mini = 100000           # Take x in Z so that lambda(x) = min{lambda(j), j in Z}
        for i in Z:
            if lambdas[i] < mini:
                mini = lambdas[i]
                indexI = i
        
        vertex = Z.index(indexI)
        Z.pop(vertex)               # Z = Z - {x}
        if indexI == b:             # If the city is the goal city, we can get out of the algorithm, the solution has just been found
            found_b = True
            
        print("\n")
        print(" ======================================== ")
        print("Went through City #" + str(indexI) + " successfully. Update Log:")
        print("\n")
        
        for city in file:
            if (int(city[0]) != indexI and int(city[1]) != indexI):         # For i in Gamma+(x) and Z, do
                continue                        
            
            # We are here dividing the test using 2 if because we're going through the file checking the links between two cities, and each line contains two cities (x->y and y->x)
            
            if int(city[0]) == indexI:
                if int(city[1]) in Z and lambdas[indexI] + float(city[2]) < lambdas[int(city[1])]:            # If the city is found first in the file line, we check the second city
                    temp = lambdas[int(city[1])]
                    lambdas[int(city[1])] = lambdas[indexI] + float(city[2])                  # If lambda(x) + I(x, i) < lambda(i), do lambda(i) = lambda(x) + I(x, i)
                    new_path = paths[indexI].copy()
                    paths[int(city[1])] = new_path
                    paths[int(city[1])].append(int(city[1]))
                    print("New Path: City #" + city[1] + " is linked to City #" + city[0]) 
                    print("New Distance: " + str(temp) + " ---> " + str(lambdas[int(city[1])]) + "kms" + "\n")      
                  
                    
            if int(city[1]) == indexI:                         # If the city is found second in the file line, we check the first city     
                if int(city[0]) in Z and lambdas[indexI] + float(city[2]) < lambdas[int(city[0])]:
                    temp = lambdas[int(city[0])]
                    lambdas[int(city[0])] = lambdas[indexI] + float(city[2])
                    new_path = paths[indexI].copy()                # We keep track of the previous path by copying it until the city we're at
                    paths[int(city[0])] = new_path                 # And we change this path in the table of paths, by adding the city we just went through
                    paths[int(city[0])].append(int(city[0]))
                    print("New Path: City #" + city[0] + " is linked to City #" + city[1])
                    print("New Distance: " + str(temp) + " ---> " + str(lambdas[int(city[0])]) + "kms" + "\n")      
                    
                    
    open("dijkstra.txt", "w").close()      # Removing everything in the file in order to write in it                        
    file2 = open('dijkstra.txt', 'a')          
    for i in range(len(lambdas)):
        file2.write(str(lambdas[i]) + ' ' + str(paths[i]) + '\n')
    file2.close()
    
    return("City #" + str(a) + " is " + str(lambdas[b]) + "kms apart from City #" + str(b))

def aStar(a, b):
    file = gatherData3()
    while file[0][0] != 'Vertices':
        file.pop(0)
    file.pop(0)                         # Going through the file and removing unnecessary data
    
    coords = []
    
    while file[0][0] != 'Edges':
        
        coords.append(file[0]) 
        file.pop(0)
    file.pop(0)
    
    open = []                               # Array of visited but unexpanded vertices
    close = []                              # Array of visited and expanded vertices
    goal = [2000 for i in range(4978)]      # Array of distances from starting point g(x))
    final = [2000 for i in range(4978)]     # Array of distances from ending point, (f(x) = g(x) + asTheCrowFlies(x, fin))
    path = []        
 
    open.append(a)
    goal[a] = 0
    final[a] = goal[a] + asTheCrowFlies(a, b, coords)    # Values initialization
    final[b] = 0
    
    while open != []:                       # While open isn't empty
        openMin = goal[open[0]] + asTheCrowFlies(open[0], b, coords)
        closestCity = open[0]               
        for i in open:
            if goal[i] + asTheCrowFlies(i, b, coords) < openMin:
                openMin = asTheCrowFlies(i, b, coords)           # closestCity = city x from open with smallest f(x)
                closestCity = i
                
        if closestCity == b:        # If this city is the goal, we break
            break
        
        open.pop(open.index(closestCity))       # Removing closestCity from open
        close.append(closestCity)               # Adding it to close
        child = []

        for city in file:
                if int(city[0]) == closestCity and int(city[1]) not in child:
                    child.append(int(city[1]))                         # Searching for all closestCity successors

                if int(city[1]) == closestCity and int(city[0]) not in child:
                    child.append(int(city[0]))
        
        for successor in child:              # child = array of successors of closestCity
            
            cost = goal[closestCity] + asTheCrowFlies(closestCity, successor, coords)        # cost = distance with closestCity added with distance from closestCity at start
            
            if successor in open and cost < goal[successor]:
                open.pop(open.index(successor))             # If the successor is already in open, we remove it since there's a new path that's more efficient
                
            if successor in close and cost < goal[successor]:
                close.pop(close.index(successor))           # If the successor is already in close, we remove it aswell
                
            if successor not in open and successor not in close:
                open.append(successor)
                goal[successor] = cost      # Otherwise, we've found a more interesting city so we update the goal and final tables
                final[successor] = goal[successor] + asTheCrowFlies(successor, b, coords)
                path.append(successor)
    
    return final[b]



#########################################################################################################################################

# VRP Computing

#########################################################################################################################################

def VRP_BestAverageCity():
    
    # Everyday, a VRP must visit a randomly chosen big city (over 200k inhabitants). 
    # From the 500 cities in the txt file, in which one should the VRP live to minimize his travels ? What would be the average distance of his travels ?

    cities200k = [200, 379, 1176, 1265, 1435, 1472, 2031, 2710, 3369, 3546, 3857] # id of the 11 cities having more than 200k inhabitants
    avgdistmin = 760.42     # Since we're in Python, the algorithm is extremely time consuming, we use these variables so we can "pause" the computing and make it run on multiple days.
    bestCity = 128         # We're using these to remember the best city found so far.
    for i in range(126, 130):
        shortestPath(i)
        file = gatherData2()
        avgdistance = 0
        not_linked = False
        
        for j in cities200k:    # Outbound distance computing 
            if not_linked:
                open("VRP_tempDB.txt", "w").close()
                break
            
            if float(file[j][0]) == 10000.0:
                not_linked = True
            avgdistance += float(file[j][0])
        
        if not_linked:
            print('not linked')
            open("VRP_tempDB.txt", "w").close()
            continue
        
        avgdistance /= 6 # Average distance + outbound-inbound
        
        if avgdistance < avgdistmin:
            avgdistmin = avgdistance
            bestCity = i
        
        print(bestCity, avgdistmin)
        open("VRP_tempDB.txt", "w").close()

    return("The most optimized city is #" + str(bestCity) + " with an average distance (outbound only) of " + str(avgdistmin) + "kms")
        
def VRP_BestPath(cities, distance):
    # We take a starting city and we look at which city is the closest,
    # We add to the distance variable the aStar between these two cities, then we remove the starting city from the array 
    # Repeat recursively until the array is empty.
    closestCity = cities[1]
    closestDist = aStar(cities[0], cities[1])       # Our base minimum is the distance with the second city in the array
                                                    # (the first one being the starting city)
    
    if len(cities) == 2:
        distance += aStar(cities[0], cities[1])
        return distance                             # If the array only contains two cities, we're done
    
    for j in range(2, len(cities)):
        distj = aStar(cities[0], cities[j])
        if distj < closestCity:                     # Otherwise, we search for the closest city
            closestCity = cities[j]
            closestDist = distj
            
            
    cities.pop(cities.index(closestCity))        
    cities[0] = closestCity                         # We remove and change the starting city for the next iteration
    distance += closestDist                         # We add the distance computed
    
    return(VRP_BestPath(cities, distance))                    # Redo with the new starting city

def VRP_BestPathMain():
    # Another VRP must go in all cities having over x inhabitants by visiting them one by one without going twice through the same city and coming back in the end to the first one.
    # Figure out automatically a path minimizing the total distance done (with x = 200000, 150000 and 100000).
      
    inhabitants = input('1 for cities with over 100k inhabitants || 2 for cities with over 200k inhabitants')   
    cities200k = [200, 379, 1176, 1265, 1435, 1472, 2031, 2710, 3369, 3546, 3857]  # id of cities having over 200k inhabitants
    cities100k = [200, 365, 379, 491, 656, 825, 1054, 1100, 1176, 1265, 1435, 1472, 1615, 1691, 1869, 2031, 2141, 2198, 2321, 2412, 2603, 2710, 3172, 3336, 3369, 3497, 3546, 3566, 3676, 3782, 3857, 3908, 3940, 4242, 4370, 4584, 4789, 4818, 4825, 4964] # id des cities de plus de 100k habitants
    
    if inhabitants == 1:
        cities = cities100k
    elif inhabitants == 2:         # We select the array corresponding to the amount of inhabitants asked
        cities = cities200k
    else:
        return ("Please input 1 or 2")
    
    bestStart = 1e12
    bestStartid = cities[0]
    
    for i in range(len(cities)):        # For the starting cities, we ony care about cities we have to visit
        
        thisStart = (VRP_BestPath(cities, 0))      # One by one, for each starting city, we look at the closest city. Repeating this process for every city in the previous function
        
        if thisStart < bestStart:
            bestStart = thisStart           # If we find a shorter total distance, we raplce the saved distance until we keep one
            bestStartid = cities[0]        # mémoire la ville de départ utilisée.
            
        city = cities.pop(0)               # For each loop, we take the first element of the array and we put it at the end.
        cities.append(city)
        
    return ("The best starting city seems to be " + str(bestStartid) + " with a total distance of " + str(bestStart))
       