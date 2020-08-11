import random

f = open("stupid.cell", "w")
f.write("This file contains cell data for the StupidModel.\n")
f.write("The data specifies the rate of food production for each cell.\n")
f.write("x" + '\t' + "y" + '\t' + "prod" + '\n')
for y in range(112):
    for x in range(250):
        f.write(str(x) + '\t'
                + str(y) + '\t'
                + str(random.random()*0.02) + '\n')
f.close()
