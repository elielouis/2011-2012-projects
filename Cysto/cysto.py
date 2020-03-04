import random


Numbers= {
2 : "half",
3 : "third",
4 : "quarter",
5 : "fifth",
6 : "sixth",
7 : "seventh",
8 : "eighth",
9 : "ninth" ,
10 : "tenth"  
}

BaseString = "What is the number that is {0} ?"

def GenerateSentence(nb):
	global BaseString
	string = ""
	ordNumber = random.randint(0, 100)
	totalNumber = ordNumber
	for i in xrange(nb):
		rand = random.randint(2, 10)
		totalNumber *= rand
		strNum = Numbers[rand]
		string += "one {0} of ".format(strNum)
	string += "{0}".format(totalNumber)
	string = BaseString.format(string)
	return ordNumber, string


def GetNbInput():
	while 1:
		try:
			x = input("How many numbers?\n=> ")
			return x
		except:
			pass

def main():
	number = GetNbInput()
	solution, string,  = GenerateSentence(number)
	open("solution.txt", "w")
	filex = open("solution.txt", "a")
	filex.write(string)
	filex.write('\n')
	filex.write("{0}".format(solution))


if __name__ == "__main__":
	main()