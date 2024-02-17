import Utility.GridTools as GridTools
import Utility.Mario.Behavior as Behavior
import Utility.Mario.Fitness as Fitness
import numpy as np
import matplotlib.pyplot as plt

leiniency = {}
linearity = {}
leiniency_small = {}
linearity_small = {}
completable = {}
completable_small = {}
for level_number in range(200):
    with open("/home/nisargparikh/Desktop/CS 7170/Warmup/Generated_Levels/mario_"+str(level_number)+".txt") as file:
        level = file.readlines() 
    

    if level_number < 100:
        leiniency[level_number] = Behavior.percent_leniency(GridTools.rows_into_columns(level))
        linearity[level_number] = Behavior.percent_linearity(GridTools.rows_into_columns(level))
    else:
        leiniency_small[level_number] = Behavior.percent_leniency(GridTools.rows_into_columns(level))
        linearity_small[level_number] = Behavior.percent_linearity(GridTools.rows_into_columns(level))


matrix = [[np.nan for _ in range(10)] for __ in range(10)]

linearity_leiniency = {}

for x in range(100):
    for y in range(100):
        linearity_leiniency[x,y] = (linearity,leiniency)

plt.clf()
plt.scatter(linearity.values(),leiniency.values(),linewidth = 1.5)
plt.xlabel("% Linearity")
plt.ylabel("% Leniency")
plt.locator_params(nbins=10)
plt.title("Big Level Leniency vs Linearity")
plt.savefig("Big_Level_Leiniency_vs_Linearity.png")

plt.clf()
plt.scatter(linearity_small.values(),leiniency_small.values(),linewidth = 1.5)
plt.xlabel("% Linearity")
plt.ylabel("% Leniency")
plt.locator_params(nbins=10)
plt.title("Small Level Leniency vs Linearity")
plt.savefig("Small_Level_Leiniency_vs_Linearity.png")


print("Linearity Big Min:",min(linearity,key=linearity.get))
print("Linearity Big Max:",max(linearity,key=linearity.get))
print("Leniency Big Min:",min(leiniency,key=leiniency.get))
print("Leniency Big Max:",max(leiniency,key=leiniency.get))
print("Linearity Small Min",min(linearity_small,key=linearity_small.get))
print("Linearity Small Max",max(linearity_small,key=linearity_small.get))
print("Leniency Small Min",min(leiniency_small,key=leiniency_small.get))
print("Leniency Small Max",max(leiniency_small,key=leiniency_small.get))

