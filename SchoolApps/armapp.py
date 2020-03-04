from colorama import Fore, Back, Style, init
import random
import os

init()


def GetCalc(difficulty):
	operation = random.randint(1, 3)
	if operation == 1:
		# Operation : +
		maximum   = 10 ** difficulty
		firstnum  = random.randint(1, maximum)
		secondnum = random.randint(1, maximum)
		strcalc   = "{0} + {1}".format(firstnum, secondnum)
		return firstnum+secondnum, strcalc

	if operation == 2:
		#Opertion : -

		maximum   = 10 ** difficulty
		firstnum  = random.randint(1, maximum)
		secondnum = random.randint(1, maximum)
		if firstnum > secondnum:
			strcalc   = "{0} - {1}".format(firstnum, secondnum)
			return firstnum-secondnum, strcalc
		else:
			strcalc   = "{0} - {1}".format(secondnum,firstnum)
			return secondnum-firstnum, strcalc

	if operation == 3:
		#Operation : *

		if difficulty == 1:
			firstnum  = random.randint(1, 10)
			secondnum = random.randint(1, 10)
		elif difficulty == 2:
			maximum   = 10 ** difficulty
			firstnum  = random.randint(1, 20)
			secondnum = random.randint(1, 20)

		elif difficulty <= 4 and difficulty > 2:
			maximum   = 10 ** difficulty
			firstnum  = random.randint(1, maximum)
			secondnum = random.randint(1, 20)

                else:
                        maximum   = 10 ** difficulty
			firstnum  = random.randint(1, maximum)
			secondnum = random.randint(1, maximum/100)
		strcalc   = "{0} * {1}".format(firstnum, secondnum)

		return firstnum*secondnum, strcalc	


def PrintStats(stats):
    #Prints the stats on the screen

	if (stats["correct"] + stats["incorrect"]) == 0:
		print  Fore.CYAN + "No stats yet"
		return 

	correctpercentage = str(float(stats["correct"]) / (stats["correct"] + stats["incorrect"])  * 100) + "%"
	print Fore.GREEN + "Correct Answers: " + Fore.CYAN + str(stats["correct"])
	print Fore.GREEN + "Wrong answers: " + Fore.CYAN + str(stats["incorrect"])
	print Fore.GREEN + "Success Percentage: " + Fore.CYAN + str(correctpercentage)




def main():
	stats = {}
	stats["correct"] = 0
	stats["incorrect"] = 0
	print Fore.RED + "Difficulty: "
	difficulty = input(Fore.YELLOW)
	while 1:
		os.system("cls")
		PrintStats(stats)
		print "\n" * 2
		operation = GetCalc(difficulty)
		userinput = raw_input(Fore.GREEN + operation[1] + " = ")
		print ""
		
		try:
			userinput = int(userinput)
		except:
			stats["incorrect"] += 1
			print Fore.RED + "Incorrect answer, the right answer was {0}".format(operation[0])
			raw_input()
			continue
		

		if userinput == operation[0]:
			stats["correct"] += 1
		else:
			stats["incorrect"] += 1
			print Fore.RED + "Incorrect answer, the right answer was {0}".format(operation[0])
			raw_input()

	print Fore.RESET + "Game over !"
	print "\n"
	PrintStats(stats)
	print Fore.RESET


if __name__ == "__main__":
	main()
