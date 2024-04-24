#STUDENT NAME: Diogo Almeida
#STUDENT NUMBER: 108902

#DISCUSSED TPI-1 WITH: (names and numbers):
#Hugo Correia 108215
#https://www.tutorialspoint.com/python_data_structure/python_binary_search_tree.htm
#https://medium.com/@rinu.gour123/heuristic-search-in-artificial-intelligence-python-3087ecfece4d

from tree_search import *
import math

class OrderDelivery(SearchDomain):

    def __init__(self,connections, coordinates):
        self.connections = connections
        self.coordinates = coordinates

    def actions(self,state):
        city = state[0]
        actlist = []
        for (C1,C2,D) in self.connections:
            if (C1==city):
                actlist += [(C1,C2)]
            elif (C2==city):
               actlist += [(C2,C1)]
        return actlist 

    def result(self, state, action):
        current_city, cities_to_visit = state
        (C1, C2) = action
        if C1 == current_city:
            new_city = C2
        else:
            new_city = C1
        new_cities_to_visit = []
        for city in cities_to_visit:
            if city != new_city:
                new_cities_to_visit.append(city)
        new_state = (new_city, new_cities_to_visit)
        return new_state

    def satisfies(self, state, goal):
        if state[1]==[]:
            if goal == state[0]:
                return True
            else:
                return False
        return False


    def cost(self, state, action):
        current_city, cities_to_visit = state
        (C1, C2) = action
        if C1 == current_city:
            for (city1, city2, distance) in self.connections:
                if city1 == C1 and city2 == C2:
                    return distance
        elif C2 == current_city:
            for (city1, city2, distance) in self.connections:
                if city1 == C2 and city2 == C1:
                    return distance
        return 0


    def heuristic(self, state, goal):
        cidades = [state[0]]
        cidades.extend(state[1])
        cidades.append(goal)
        distancias = []
        total_distancias = 0
        for i in range(len(cidades)-1):
            distancia = math.dist(self.coordinates[cidades[i]], self.coordinates[cidades[i+1]])
            distancias.append(distancia)
        for n in range(len(distancias)):
            total_distancias += sum(distancias[n:])
        return total_distancias



class MyNode(SearchNode):

    def __init__(self,state,parent,depth=None,cost=None,heuristic=None,eval=None):
        super().__init__(state,parent)
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        if eval == None:
            self.eval = self.cost + self.heuristic
        else:
            self.eval = eval

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',maxsize=None):
        super().__init__(problem,strategy)
        self.problem = problem
        root = MyNode(problem.initial, None, 0, 0, 0)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.non_terminals = 0
        self.maxsize = maxsize
        self.terminals = 1
        self.marked_nodes = []


    def astar_add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key=self.sort_nodes)

    def search2(self):
        while self.open_nodes != []:
            self.terminals = len(self.open_nodes)
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                return self.get_path(node)
            self.non_terminals += 1
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    new_depth = node.depth + 1
                    new_cost = node.cost + self.problem.domain.cost(node.state,a)
                    new_heuristic = self.problem.domain.heuristic(newstate,self.problem.goal)
                    newnode = MyNode(newstate,node,new_depth,new_cost,new_heuristic)
                    lnewnodes.append(newnode)
            self.manage_memory()
            self.add_to_open(lnewnodes)
        return None

    def manage_memory(self):
        if self.strategy == 'A*' and self.maxsize is not None:
            total_tree_size = self.non_terminals+len(self.open_nodes)
            while total_tree_size > self.maxsize:

                for i in range(len(self.open_nodes)-1,-1,-1):
                    if self.open_nodes[i] not in self.marked_nodes:
                        self.marked_nodes.append(self.open_nodes[i])
                        atual_node = self.open_nodes[i]
                        break

                siblings = []
                for node in self.open_nodes:
                    if node.parent == atual_node.parent:
                        siblings.append(node)
                
                all_marked = True
                for node in siblings:
                    if node not in self.marked_nodes:
                        all_marked = False
                if all_marked:
                    for node in siblings:
                        if node in self.open_nodes:
                            self.open_nodes.remove(node)       
                    self.non_terminals -= 1
                    atual_node.parent.eval = min(node.eval for node in siblings)
                    total_tree_size= len(self.open_nodes)+self.non_terminals
                    
                            
                

    def sort_nodes(self, node):
        return(node.eval,node.state)

def orderdelivery_search(domain, city, targets, strategy='breadth', maxsize=None):
    p = SearchProblem(domain, (city,targets), city)
    t = MyTree(p, strategy, maxsize)
    path = t.search2()
    path_final = []
    for city, citys in path:
        path_final.append(city)
    return (t,path_final)










