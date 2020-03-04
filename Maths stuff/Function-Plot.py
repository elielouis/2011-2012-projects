import turtle
import time
import math
import random



replace_list = [
"cos",
"hypot",
"sin",
"tan",
"factorial",
"exp",
"log",
"pow",
"sqrt",
"acos",
"asin",
"atan",
"atan2",
"degrees",
"radians",
"pi"]


def f(function, z):
    for j in replace_list:
        function = function.replace(j, "math." + j)
    
    function = function.replace("^", "**")
    function = function.replace("[", "(")
    function = function.replace("]", ")")
    function = function.replace("{", "(")
    function = function.replace("}", ")")
    function = function.replace("z", "(" + str(z) + ")")
    try:
        y = eval(function)
        return y
    except Exception, e:
        print e
        return 0


function = raw_input("Enter the function: ")
div = input("Division: ")


f_range=300
turtle.pencolor((0.0, 0.0, 0.0))

turtle.penup()
turtle.goto(-f_range, 0)
turtle.pendown()
turtle.goto(f_range, 0)
turtle.penup()
turtle.goto(0, 500)
turtle.pendown()
turtle.goto(0, -500)
turtle.penup()
turtle.goto(-f_range, f(function, -f_range)/div)
turtle.pendown()

for j in range(-f_range+1, f_range+1):
    turtle.setpos(j, f(function, j)/div)
raw_input()
