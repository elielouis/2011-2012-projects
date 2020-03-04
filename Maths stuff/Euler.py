import math

replace_list = [
"cos",
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

jmp_div = 1000000

def f(function, x, y):
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


def solve(derivativeFunction, initialX, initialY, objectiveX):
    y = float(initialY)
    x = float(initialX)
    objectiveX = float(objectiveX)
    h = objectiveX/float(jmp_div)
    while 1:
        if x <= (objectiveX-h):
            slope = f(derivativeFunction, x, y)
            x += h
            y += slope * h
            #print "x = " + str(x) + " y = " + str(y) + " objectivex = " + str(objectiveX)
        else:
            break
    return y

function = "1+z-y"
initialX = 0
initialY = 1
objectiveX = 5
print solve(function, initialX, initialY, objectiveX)
