import math

h = 10**(-5)

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
x = input("Enter x: ")
print ( f(function, x+h) - f(function, x) ) / h
input()
