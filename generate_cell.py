import random

f = open("stupid.cell", "w")
for y in range(112):
    for x in range(250):
        f.write(str(x) + " "
                + str(y) + " "
                + str(random.random()*0.02) + '\n')
f.close()
