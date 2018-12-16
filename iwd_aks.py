from BankParseUpdated import inputMatrix
#from libraryParse import list_size
end_node=0
node_length=len(inputMatrix)
soil_iwd =0.0
v_iwd  =100
a_vel = 1
alpha = []
#undiscovered = 0, visited =1, discovered =2
status = [-1]*9
final_path = []
cost_path =[]
fan_in = []
fan_out =[]

for i in range(0,node_length):
    indegree=0;    
    for j in range(0,node_length):
        if inputMatrix[j][i]==1:
            indegree+=1
    fan_in.append(indegree)
#print("Indegree")

#calculating outdegree in out
for i in range(0,node_length):
    outdegree=0;    
    for j in range(0,node_length):
        if inputMatrix[i][j]==1:
            outdegree=outdegree+1;
    out.append(outdegree)
#print("Outdegree")

#calculating cyclomatic complexity
cyclomatic_complexity  =[]
for i in range(0,node_length):
    cc_value = 0
    for j in range(i,node_length):
        cc_value += fan_out[j]
    cyclomatic_complexity.append(cc_value)
#print(cyclomatic_complexity)

#creating list of nodes in neighbourhood for every vertex
neighbourhood = []
for i in range(0, node_length):
    adjacent_nodes =[]
    for j in range(0,node_length):
        if inputMatrix[i][j]==1:
            adjacent_nodes.append(j)
    neighbourhood.append(adjacent_nodes)
#print(neighbourhood)

#calculating subgraph
def DFSNodeCalculator(i,visited,count):
    if(visited[i]==0):
        visited[i]=1
        for j in range(0,node_length):
            if(visited[j]==0 and inputMatrix[i][j]==1):
                count=1+DFSNodeCalculator(j,visited,count)
                
    return count
subgraph=[]
visited=[]
count=0
for i in range(0,node_length):
    for j in range(0,node_length):
        visited.append(0)
    subgraph.append(DFSNodeCalculator(i,visited,count))
    del visited[:]
    count=0
print ("Subgraph")
print (subgraph)


def check_status(neighbourhood_list,status):
    unvisited = []
    for i in neighbourhood_list:
        if status[i] == -1:
            unvisited.append(i)
    return unvisited



def checkAllVisited(node,alpha):
    for i in neighbour[node]:
        if i not in alpha:
            return False
    return True



def backtrack(alpha,status):
    n = len(alpha)
    remove_elements = []
    for i in range(0,n):
        if status[alpha[n-1-i]] != 0:
            remove_elements.append(alpha[n-1-i])
        else if status[alpha[n-1-i]]==0 :
            i = alpha[n-1-i]
            del alpha[n-1-i]
            break
    new_alpha = []
    for i in alpha:
        if i not in remove_elements:
            new_alpha.append(i)     
    return new_alpha,i


def findBacktrackedCost(cost_dict,alpha):
    key = str(alpha[0])
    for i in range(1,len(alpha)):
        key = key + "-" + str(alpha[i])
    return cost_dict[key]


cost_dict={}
def writeCost(path,cost):
    key  = str(path[0])
    for i in range(1,len(path)):
        key  = key+"-"+str(i)
    cost_dict[key] = cost


soil = [0.0]*node_length
soil_at_edges = [[0.0 for x in range(0,node_length)] for y in range(0,node_length)]

status[i] = 1
alpha.append(i)
decisionFactor = [[0.0 for x in range(0,node_length)] for y in range(0,node_length)]
velocity = [[0.0 for x in range(0,node_length)] for y in range(0,node_length)]
timeTaken = [[0.0 for x in range(0,node_length)] for y in range(0,node_length)]
leaves = 0
for i in range(0,node_length):
    if(fan_out[i]==0):
        leaves +=1

i=0
path = []
cost = 0

while(sum(status)!= 2*node_length-leaves):
    path.append(i)
    
    while(fan_out[i]!=0):
        if(fan_out[i]>1):
            soil[i] = soil_iwd + cyclomatic_complexity[i] + 1
        else:
            soil[i] = soil_iwd + cyclomatic_complexity[i] + 0
        
        if(len(neighbourhood[i]==1)):
            next_node = neighbourhood[i]
            soil_at_edge[i][next_node] = (fan_in[i] + fan_out[next_node])/(subgraph[next_node]+1)
            
        else:
            unvisited = check_status(neighbourhood[i],status)
            if(len(unvisited)>1):
                min_decision_factor = 1000000
                for node in unvisited:
                    soil_at_edge[i][node] = (fan_in[i] + fan_out[node])/(subgraph[node] +1)
                    decisionFactor[i][node] =  soil_at_edge[i][node] /(cyclomaticyclomatic_complexity[node]+ len(neighbourhood[i]-node))
                    if decision_factor[i][node]<min_decision_factor:
                        next_node = node
            else:
                next_node = unvisited[0]
            
        status[next_node]= 1
        alpha.append(next_node)
        
        velocity[i][next_node] = vel_iwd + (a_vel/(soil[i]+soil_at_edge[i][next_node] )
        vel_iwd = velocity[i][next_node]
        dist_iwd = len(alpha)-1
        timetaken = dist_iwd/ vel_iwd
        soil_iwd = soil[i]/( timetaken + vel_iwd)
        soil[i] -= soil_iwd
        path.append(next_node)
        cost += soil[i] + soil[i][next_node]
        writeCost(path,cost)
        prev_node = i
        i = next_node
        
        if(checkAllVisited(prev_node,alpha)):
            status[prev_node] = 2
        else:
            status[prev_node] = 0
        
    final_path.append(path)
    cost_path.append(cost)
    alpha,i = backtrack(alpha,status)
    cost = findBacktrackedCost(cost_dict,alpha)


finalCostDict ={}       
def printCostPath(final_path,cost_path):
    for i in range(0,len(final_path)):
        key = ""
        for j in final_path[i):
            key += str(j)+"-"
        print(key + ":",cost_path[i])
        finalCostDict[key] = cost_path[i]







    