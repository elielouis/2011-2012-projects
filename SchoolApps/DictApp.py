import os
import random
from ctypes import *
import sys



def ChangeColor(newcolor):
        windll.Kernel32.GetStdHandle.restype = c_ulong
        h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
        windll.Kernel32.SetConsoleTextAttribute(h, newcolor)


def GetWordList(file):
	#Get the words and their values from the text file
	lines = open(file).readlines()
	random.shuffle(lines)
	words = [i.rstrip() for i in lines]
	return words


def InputEqualsValue(times, word, value):
	value = value.split()
	if len(value) == times:
		for i in value:
			if i != word:
				return False
		return True
	else:
		return False


def PrintStats(words_written):
        #Prints the stats on the screen
    green = 2
    blue = 3
    ChangeColor(green) 
    OtherPrint("Number of words written: ")
    ChangeColor(blue)
    OtherPrint(str(words_written))

	


def OtherPrint(chars):
    sys.stdout.write(chars)



def main():
	words = GetWordList("wordlist.txt")
	times = 3
	words_written = 0
	for word in words:
		answer = ''
		PrintStats(words_written)
		print "\n" * 2
		while not InputEqualsValue(times, word, answer):
			ChangeColor(14)
			
			OtherPrint("Please write ")
			ChangeColor(11)
			OtherPrint("{0} ".format(word))
			ChangeColor(14)
			OtherPrint("{0} times:".format(times))
			ChangeColor(10)
			answer = raw_input("\n=> ")
			print "\n" * 2
		words_written += 1
		os.system('cls')


	os.system("cls")
	print "Training finished!"
	PrintStats(words_written)
	raw_input()




if __name__ == "__main__":
	main()
