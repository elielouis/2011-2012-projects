import turtle
import time
import math
import random


points = []
for i in xrange(random.randint(10,10)):
    points.append([random.randint(-300, 300), random.randint(-300,300)])
    


# Binominal theorem
def binominal(n, i):
    return (math.factorial(n))/(math.factorial(i)*math.factorial(n-i))

# The B function
def B(points, t, index):
    value = 0
    n = len(points)-1
    for i in xrange(n+1):
        toadd = binominal(n, i)
        toadd *= t**i
        toadd *= (1-t)**(n-i)
        toadd *= points[i][index]
        value += toadd

    return value 

#Get ready to put the points
turtle.pencolor((1.0, 0.0, 0.0))
turtle.width(10)

#Put the points
for j in points:
    turtle.up()
    turtle.setpos(j[0], j[1])
    turtle.down()
    turtle.dot()

#Put back the original settings
turtle.width(1)
turtle.pencolor((0.0, 0.0, 0.0))
turtle.up()
turtle.setpos(points[0][0], points[0][1])
turtle.down()
turtle.speed(0)

#Finally, draw the curve!
t = 0.000
while t < 1.00:
    t += 0.01
    turtle.setpos(int(B(points, t, 0)), int(B(points, t, 1)))

raw_input()
