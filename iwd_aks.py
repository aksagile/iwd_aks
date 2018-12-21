#from BankParseUpdated import inputMatrix
#from libraryParse import list_size
inputMatrix = [[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
               [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
               [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
               [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
#parent=[]
node_length=len(inputMatrix)
#or i in range(0,node_length):
#    allParents = []
#    for j in range(0,node_length):
#        if(inputMatrix[j][i]==1):
#            allParents.append(j)
#    parent.append(allParents)
#print(parent)
end_node=0

soil_iwd =0.0
vel_iwd  =100
a_vel = 1
alpha = []
#undiscovered = 0, visited =1, discovered =2
status = [-1]*node_length
final_path = {}
final_paths = []
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
#print(fan_in)

#calculating outdegree in out
for i in range(0,node_length):
    outdegree=0;    
    for j in range(0,node_length):
        if inputMatrix[i][j]==1:
            outdegree=outdegree+1
    fan_out.append(outdegree)
#print(fan_out)

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
#print ("Subgraph")
#print (subgraph)


def check_status(neighbourhood_list,status):
    unvisited = []
    #unvisited2 =[]
    for ele in neighbourhood_list:
        if status[ele] == -1:
            unvisited.append(ele)
    #print("..........status checked..............")
    #print(unvisited,"\n")
    if(len(unvisited)==0):
        for ele in neighbourhood_list:
            if status[ele] == 1:
                unvisited.append(ele)
    return unvisited



def checkAllVisited(node,status):
    for i in neighbourhood[node]:
        if status[i]==-1:
            #print("...checking all visted.....false\n",)
            return False
    #print("...checking all visted.....true\n",)
    return True



def backtrack(a,o):
    if len(a)==1 or len(a)==0:
        ele = -1
        return {"a":a,"ele":-1,"bool":o} 
    elif status[a[len(a)-1]] == 0:
       ele = a[len(a)-1]
       o = True
       return {"a":a,"ele":ele,"bool":o}
    else:
        #status[]
        status[a[-1]] = 1
        a.pop()
        return backtrack(a,o)
            
                
    

cost_dict={}

#def findBacktrackedCost(cost_dict,alpha):
#    key = str(alpha[0])
#    for i in range(1,len(alpha)):
#        key = key + "-" + str(alpha[i])
#    return cost_dict[key]



def writeCost(a,c):
    key  = str(a[0])
    for i in range(1,len(a)):
        key  = key+"-"+str(a[i])
    #print("........written cost updated..........")
    cost_dict[key] = c


soil = [0.0]*node_length
soilUpdation = [0.0]* node_length
soil_at_edge = [[0.0 for x in range(0,node_length)] for y in range(0,node_length)]


decisionFactor = [[0.0 for x in range(0,node_length)] for y in range(0,node_length)]
velocity = [[0.0 for x in range(0,node_length)] for y in range(0,node_length)]
timeTaken = [[0.0 for x in range(0,node_length)] for y in range(0,node_length)]
leaves = 0
for i in range(0,node_length):
    if(fan_out[i]==0):
        leaves +=1
        
#print(leaves)

i=0
path = []
cost = 0
costNode = [0.0]*node_length
status[i] = 1
alpha.append(i)
counter = 0
visited =[]
k=0
veliwd_dict = {}
while(sum(status)<= 2*node_length - leaves):
    #path.append(i)
    
    path =alpha
    #print(".....path.......\n",path)
    #print("....counter.....\n",counter)
    while(fan_out[i]!=0):
        if counter == 0:
            if(fan_out[i]>1):
               soil[i] = soil_iwd + cyclomatic_complexity[i] + 1
            else:
               soil[i] = soil_iwd + cyclomatic_complexity[i] + 0 
        else:
            if soil[i] == 0:
                indx = alpha.index(i)
                if(fan_out[i]>1):
                    soil[i] = soilUpdation[alpha[indx-1]] + cyclomatic_complexity[i] + 1
                else:
                    soil[i] = soilUpdation[alpha[indx-1]] + cyclomatic_complexity[i] + 0
            else:
                soil[i] = soil[i] + soilUpdation[i]
        unvisited = check_status(neighbourhood[i],status)
        if(len(unvisited)==1):
            next_node = unvisited[0]
            soil_at_edge[i][next_node] = (fan_in[i] + fan_out[next_node])/(subgraph[next_node]+1)
            
        else:
            min_decision_factor = 1000000
            for node in unvisited:
                soil_at_edge[i][node] = (fan_in[i] + fan_out[node])/(subgraph[node] +1)
                decisionFactor[i][node] =  soil_at_edge[i][node] /(cyclomatic_complexity[node]+ node_length-1-node)
                if decisionFactor[i][node]<min_decision_factor:
                    min_decision_factor = decisionFactor[i][node]
                    next_node = node

            
        status[next_node]= 1
        if next_node not in alpha:
            alpha.append(next_node)
        if counter>1 and fan_out[next_node]>1:
            velocity[i][next_node] = veliwd_dict[next_node] + (a_vel/(soil[i]+soil_at_edge[i][next_node]))
            
        else:
            velocity[i][next_node] = vel_iwd + (a_vel/(soil[i]+soil_at_edge[i][next_node]))
        vel_iwd = velocity[i][next_node]
        veliwd_dict[next_node] = vel_iwd
        dist_iwd = len(alpha)-1
        timetaken = dist_iwd/ vel_iwd
        soil_iwd = soil[i]/( timetaken + vel_iwd)
        soilUpdation[i] = soil_iwd
        soil[i] = soil[i] - soil_iwd
        #path.append(next_node)
        cost = cost + soil[i] + soil_at_edge[i][next_node]
        costNode[next_node]  = cost
        #writeCost(alpha,cost)
        prev_node = i
        if(subgraph[next_node]!=0):
            i = next_node
        else:
            #print("..........leaf is found.........")
            #print(".....alpha......",alpha)
            path = alpha.copy()
            
            #print("...........alpha in final path...........")
            final_path[k] = path
            #print(final_path)
            k=k+1
            break
        #print("...prev node..........",prev_node,"\ncounter....",counter)
        #print("...next node..........",next_node,"\ncounter....",counter)
        
        if(checkAllVisited(prev_node,status)):
            status[prev_node] = 2
        else:
            status[prev_node] = 0
    #if alpha not in final_path:    
    #    final_path.append(alpha)
    #print("..........finalpath......\n",final_path)
    #final_paths.append(path)
    cost_path.append(cost)
    writeCost(alpha,cost)
    counter = counter+1
    #alpha.pop()
    value ={}
    value = backtrack(alpha,False)
    #print("...info from backtrack..........",value["bool"])
    alpha = value["a"]
    #print(".....alpha from backtrack.........\n",alpha)
    i  = value["ele"]
    #print(" .....decision node......\n",i)
    over = value["bool"]
    if(over == False):
        break
    #cost = findBacktrackedCost(cost_dict,alpha)
    cost = costNode[i]
    #counter += 1
    #print(counter)

print("..$$finalPath$$...\n",final_path,"\n")
print("....cost_path.......\n",cost_path,"\n")
finalCostDict ={}       
def printCostPath(final_path,cost_path):
    for i in range(0,len(final_path)):
        key = ""
        for j in final_path[i]:
            key += str(j)+"-"
        #print("...printing value...........of dict\n")
        #print(key + ":",cost_path[i])
        key+=">"
        finalCostDict[key] = cost_path[i]
        
printCostPath(final_path,cost_path)
print("\n")
print("......final cost dict......\n")
print("..........path      ->        cost..........")

print(finalCostDict)







    