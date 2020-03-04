import os
import random
from ctypes import *
import sys



def ChangeColor(newcolor):
        windll.Kernel32.GetStdHandle.restype = c_ulong
        h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
        windll.Kernel32.SetConsoleTextAttribute(h, newcolor)

def RemoveUselessChars(sentence):
        sentence = sentence.replace(",", "")
        sentence = sentence.replace(".", "")
        sentence = sentence.replace(";", "")
        sentence = sentence.replace(":", "")
        return sentence

def GetWordList(file):
	#Get the words and their values from the text file
	lines = open(file).readlines()
	random.shuffle(lines)
	words = dict([RemoveUselessChars(i.rstrip()).lower().split("//") for i in lines])
	return words

def GetMinimum(sentence):
	#Using in comparing
	sentencelength = len(sentence)
	return sentencelength / 2 + 1

def InputEqualsValue(words, word, value):
	#Compares
	sentence = words[word].split(" ")
	value    = value.split(" ")	
	minimum  = GetMinimum(sentence)
	correct  = 0

	for word in sentence:
		if word in value:
			correct += 1
			value.remove(word)

	if correct >= minimum:
		return True

	return False

def OtherPrint(chars):
        sys.stdout.write(chars)

def PrintStats(stats):
        #Prints the stats on the screen
        green = 2
        blue = 3

	if (stats["correct"] + stats["incorrect"]) == 0:
                ChangeColor(blue)
		print "No stats yet"
		return 

	correctpercentage = str(float(stats["correct"]) / (stats["correct"] + stats["incorrect"])  * 100) + "%"
        ChangeColor(green) 
	OtherPrint("Correct Answers: ")
	ChangeColor(blue)
	OtherPrint(str(stats["correct"]) +'\n')
        ChangeColor(green)
        OtherPrint("Wrong answers: ")
        ChangeColor(blue)
        OtherPrint(str(stats["incorrect"]) + "\n")
        ChangeColor(green)
        OtherPrint("Success Percentage: ")
        ChangeColor(blue)
        OtherPrint(str(correctpercentage))


def main():
	words = GetWordList("meanings.txt")
	stats = {}
	stats["correct"] = 0
	stats["incorrect"] = 0
	for word in words:
		os.system("cls")
		PrintStats(stats)
		print "\n" * 2
		ChangeColor(14)
		answer = raw_input("What is the meaning of {0} ?\n=> ".format(word)).lower()
                answer = RemoveUselessChars(answer)
		if InputEqualsValue(words, word, answer):
			stats["correct"] += 1
		else:
                        print "\n" * 2
                        ChangeColor(12)
                        OtherPrint("Wrong! The right answer is:\n")
                        ChangeColor(14)
                        OtherPrint(words[word])
                        raw_input()
			stats["incorrect"] += 1

	os.system("cls")
	print "Game over!"
	print
	PrintStats(stats)
	raw_input()




if __name__ == "__main__":
	main()
