from gurobipy import Model, quicksum, GRB
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import data 
from color import Color

#Assign Data from data file
nodes =     data.nodes
vehicles =  data.vehicles 
vp =        data.vp 
psync =     data.psync
n =         data.n
a =         data.a
b =         data.b
s =         data.s
X =         data.X
Y =         data.Y
arcs =      data.arcs
prefs_3 =   data.prefs_3


#Travel times:                                    
duration = {(i,j): np.hypot(X[i]-X[j], Y[i]-Y[j]) * 0.5 for i in nodes for j in nodes if i != j}


#---------Problem Definition----------#
model = Model('VRPTWSyn')
model.ModelSense = GRB.MINIMIZE #Gurobi minimizes normally so this step is theoretically unecessary

arc_var = [(i,j,k) for i in nodes for j in nodes for k in vehicles if i != j]
arc_time = [(i,k) for i in nodes for k in vehicles]

#Decision Variables: 
x = model.addVars(arc_var, vtype=GRB.BINARY, name='x')
t = model.addVars(arc_time, vtype=GRB.CONTINUOUS, name='t')
w = model.addVar(vtype=GRB.CONTINUOUS, name='w')


#---------Objective Functions----------#

#Single Objective Optimization#
#--1--#
#model.setObjective(quicksum(duration[i,j]*x[i,j,k] for i,j,k in arc_var))
#--2--#
#model.setObjective(quicksum(prefs_3[i,k] * x[i,j,k] for k in vehicles for (i,j) in arcs))
#--3--#
#model.setObjective(w)

#Multi Objective Optimization HIERARCHICAL METHOD#
#--1--#
model.setObjectiveN(quicksum(duration[i,j]*x[i,j,k] for i,j,k in arc_var),0 , priority=3)
#--2--#
model.setObjectiveN(quicksum(prefs_3[i,k] * x[i,j,k] for k in vehicles for (i,j) in arcs),1,priority=1)
#--3--#
model.setObjectiveN(w,2,priority=2)

#Multi Objective Optimization BLENDED METHOD#
#--1--#
#model.setObjectiveN(quicksum(duration[i,j]*x[i,j,k] for i,j,k in arc_var), 0, priority=0, weight=1)
#--2--#
#model.setObjectiveN(quicksum(prefs_3[i,k] * x[i,j,k] for k in vehicles for (i,j) in arcs), 1, priority=0, weight=-3)
#--3--#
#model.setObjectiveN(w, 2, priority=0, weight=3)


#---------Constraints----------#
#--1--#
model.addConstrs(quicksum(x[i,j,k] for j in nodes for k in vehicles if i!=j) == 1 for i in vp)

#--2--#
model.addConstrs(quicksum(x[0,j,k] for j in nodes if j != 0) == 1 for k in vehicles)
model.addConstrs(quicksum(x[j,(n+1),k] for j in nodes if j != (n+1)) == 1 for k in vehicles)

#--3--#
model.addConstrs(quicksum(x[i,j,k] for j in nodes if j != i) - quicksum(x[j,i,k] for j in nodes if j != i) == 0 for i in vp for k in vehicles)

#--4--#
model.addConstrs((t[i,k] + (duration[i,j] + s[i])*x[i,j,k]) <= (t[j,k] + b[i]*(1 - x[i,j,k])) for i in nodes for j in nodes for k in vehicles if i != j)

#--5--#
model.addConstrs((a[i]*quicksum(x[i,j,k] for j in nodes if i != j)) <= t[i,k] for i in vp for k in vehicles)
model.addConstrs(t[i,k] <= b[i]*quicksum(x[i,j,k] for j in nodes if i != j) for k in vehicles for i in vp)

#--6--#
model.addConstrs(a[i] <= t[i,k] for k in vehicles for i in nodes if i == 0 or i == (n+1))
model.addConstrs(t[i,k] <= b[i] for k in vehicles for i in nodes if i == 0 or i == (n+1))

#--7--#
model.addConstrs(quicksum(t[i,k] for k in vehicles) == quicksum(t[j,k] for k in vehicles) for j in nodes for i in nodes if (i,j) in psync)

#--8--#
model.addConstrs(quicksum(s[i]*x[i,j,k] for i in nodes for j in nodes if i != j) - quicksum(s[i]*x[i,j,l] for i in nodes for j in nodes if i != j) <= w \
    for k in vehicles for l in vehicles if k != l)

#--9--#
model.addConstr(w >= 0)
#Die anderen Nebenbedinungen müssen nicht programmiert werden, weil sie durch die Entscheidungsvariablen bereits festgelegt werden


#---------Optimizing the Model----------#
model.optimize()

#Printing the Variables
print("Objective Value: " ,str(round(model.ObjVal, 2)))
for v in model.getVars():
    if v.x > 0.9: 
        print(str(v.VarName)+"="+str(v.x))


#---------Routes for the Graphic Illustration---------#
routes = [ ]
truck = [ ]
K = vehicles
N = nodes
for k in vehicles: 
    for i in nodes: 
        if i != 0 and x[0,i,k].x>0.9:
            aux = [0,i]
            while i != n+1: 
                j = i
                for h in nodes:
                    if j != h and x[j,h,k].x>0.9:
                        aux.append(h)
                        i = h
            routes.append(aux)
            truck.append(k)


#---------Times for the Graphical Illustration----------#
times = list()
for k in range(len(routes)):
    help = []
    for j in range(len(routes[k])):
        l = k + 1
        #print(k, routes[k][j], ": ", t[routes[k][j],l].x)
        help.append(t[routes[k][j],l].x)
    times.append(help)
#print(times)


#---------Graphic Illustration (Matplotlib)----------#pip ins
plt.figure(figsize=(12,5))
plt.scatter(X,Y, color="blue")
plt.scatter(X[0], Y[0], color='red', marker='D')
plt.scatter(X[11], Y[11], color='red', marker='D') #muss manuell angepasst werden falls wir n verändern (n+1 liefert einen Fehler)

#Routes: 
for r in range(len(routes)):
    for n in range(len(routes[r]) - 1):
        i = routes[r][n]
        j = routes[r][n+1]
        plt.plot([X[i], X[j]],[Y[i], Y[j]], color=Color[r], alpha = 0.3)

#Time when the Vehicle starts the Serivce at each Visit-Point
for r in range(len(times)):
    for n in range(len(times[r])):
        i = routes[r][n]
        if i == 11 or i == 0:
            continue
        else: 
            plt.annotate('$t_{%d}=%d$\n'%(i,times[r][n]),(X[i]+1,Y[i]))

#Legend
patch = [mpatches.Patch(color=Color[n], label="Vehicle " + str(truck[n])) for n in range(len(truck))]
plt.legend(handles=patch,loc='best')

#Time Windows for each Visit-Point
plt.annotate("\nDC|$t_{%d}$=(%d$,%d$)" %(0, a[0], b[0]), (X[0]-1,Y[0]-5.5))
for i in vp: 
    plt.annotate('\n$t_{%d}$ = (%d$,%d$)' %(i, a[i], b[i]), (X[i]+1, Y[i]))

plt.xlabel("DistanceX")
plt.ylabel("DistanceY")
plt.title("VRPTWSyn\n Hierarchical Method (3,1,2) ", fontsize=10)
plt.show()

