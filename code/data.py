#Data Definition#

n = 10                                                                  #Number of Visit Points
vp = [i for i in range (n+1) if i != 0]                                 #List of Visit Points (no depots)
nodes = [0] + vp + [n + 1]                                              #List of all Nodes incl. depots 
arcs = [(i,j) for i in nodes for j in nodes if i != j]                  #Every Possible Arc 
psync = {#(3,4),#Schulart 1 - Gymnasium Synchronisation#
        #(3,6),
        #(3,7),
        #(3,8),
        #(4,3),
        (4,6),
        (4,7),
        (4,8),
        #(6,3),
        (6,4),
        (6,7),
        (6,8),
        #(8,3),
        (8,4),
        (8,6),
        (8,7),
        (2,5),#Schulart 2 - Grundschule Synchronisation#
        (5,2)
        #(1,10),#Schulart 3 - Mittelschule Synchronisation wird aktuell nicht ausgeführt#
        #(10,1),
        }
#Times Windows {a;b}:
a = {0:0,   1:70,  2:70,  3:50,  4:50,  5:70,  6:50,  7:50,  8:50,  9:35,  10:40,  11:0}                #begin of Starting the service times for each node                                  
b = {0:300, 1:140, 2:190, 3:180, 4:180, 5:190, 6:180, 7:180, 8:180, 9:260, 10:280, 11:300}              #end of Starting the Service times for each node

#Service Times (S): 
s = {0:0, 1:10, 2:20, 3:30, 4:20, 5:30, 6:30, 7:50 ,8:60 ,9:20 ,10:40, 11:0}                            #Service Times for each VP

#Vehicles k: 
vehicles = [1,2,3,4,5]

#Coordinates
X = [55, 10, 80, 85, 65, 5 , 80 ,50, 55, 145,140, 55]                                                   #Fixed X Coordinates
Y = [70, 35, 5 , 105,95, 100,60 ,85, 25, 80, 115, 70]                                                   #Fixed Y Coordinates
#VP  D   1   2   3   4   5   6   7   8   9   10   D
#Negative Preferences: 
prefs_3 = {(0,1): 0,
           (0,2): 0,
           (0,3): 0,
           (0,4): 0,
           (0,5): 0,
           (0,6): 0,
           (1,1): 2, 
           (1,2): 30, 
           (1,3): 4,
           (1,4): 60,
           (1,5): 25,
           (1,6): 20,
           (2,1): 7, 
           (2,2): 80,
           (2,3): 23,
           (2,4): 40,
           (2,5): 5,
           (2,6): 35,
           (3,1): 40, 
           (3,2): 60,         
           (3,3): 9,
           (3,4): 25,
           (3,5): 12,
           (3,6): 30,
           (4,1): 20,
           (4,2): 40,
           (4,3): 60,
           (4,4): 12,
           (4,5): 15,
           (4,6): 15,
           (5,1): 30,
           (5,2): 80,
           (5,3): 10,
           (5,4): 15,
           (5,5): 5,
           (5,6): 80,
           (6,1): 10,
           (6,2): 40,
           (6,3): 20,
           (6,4): 30,
           (6,5): 12,
           (6,6): 30,
           (7,1): 15,
           (7,2): 80,
           (7,3): 70,
           (7,4): 60,
           (7,5): 20,
           (7,6): 85,
           (8,1): 15,
           (8,2): 25,
           (8,3): 10,
           (8,4): 2,
           (8,5): 25,
           (8,6): 10,
           (9,1): 4,
           (9,2): 3,
           (9,3): 6,
           (9,4): 10,
           (9,5): 15,
           (9,6): 20,
           (10,1): 20,
           (10,2): 15,
           (10,3): 25,
           (10,4): 60,
           (10,5): 50,
           (10,6): 70,
           (11,1): 0,
           (11,2): 0,
           (11,3): 0,
           (11,4): 0,
           (11,5): 0,
           (11,6): 0,
           }