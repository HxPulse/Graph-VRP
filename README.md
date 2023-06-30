# Graph-VRP
Python implementations of Dijkstra and A* algorithms to solve VRP-related problems

# What's VRP ?

VRP stands for Vehicle Routing Problem, you may find all the information you need here : https://en.wikipedia.org/wiki/Vehicle_routing_problem

# What's the goal ?

We're here into optimization. Indeed, by using algorithms such as Dijkstra or A*, we want to find the shortest path between several cities. This repository contains all the tools to do so.

# What are the Datas ?

We're using real life data of the largest french cities. The data itself is a graph made from 2 files : 
- Cities_X.txt contains the ids and names of the X largest cities (the vertices).
- Cities_Xcoord.txt contains the ids and 2D cartesians coordinates of the X largest cities (the vertices).
- In a second part, both files also have data of all the edges of the graph, that means, the ids of the cities linked to each other with their respective distance (because one city is only linked to a few others).
- In this project, X = 5000 or 10000

# Dijkstra & A*

These are graph algorithms made to find the shortest path between two vertices (the least amount of edges to go from one vertex to another, if the edges have different values, then the lowest value)

More info about :
    - Dijkstra : https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#:~:text=Dijkstra's%20algorithm%20(%2F%CB%88da%C9%AA,Dijkstra's%20algorithm
    - A* : https://en.wikipedia.org/wiki/A*_search_algorithm

All functions in the python file briefly explain their utility and behavior.
