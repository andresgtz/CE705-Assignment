#!/usr/bin/env python3

#-------------------------------------------------------------------------------
# Title: solar.py
# Author: Andres Gutierrez Castano
# PRID: GUTI01304
# Lecturer: Adrian F. Clark
#
# Purpose: This program was developed as the final assignment for the
#	   course CE705: Programming in Python. This task summarizes the
#	   majority of the topics covered in  class. 
#
# Programming Language: Python v3.4.2
#
# Program Description: The following program calculates the amount of 
#	electricity by solar panels. The program reads input from a file
#	provided by the	terminal which contains two numbers, the first one is an
#	integer starting from 0 that indicates the number of the day in which
#	the measure was taken,and the second one is a float containing the 
#	electrical meausurement. It is important to state that the file is
#	missing some inputs, so this had to be generated. As well the file
#	contains comments that should be ignored.
#
# Code Libraries used:
# 	sys: This library was used to manage the argumentes provided by the 
#   	     user in the terminal.
#
#	math: This library was used to apply functions like sine, square root
#             power functions and other math related functions.
#
#	matplotlib (pyplot): This library was used to 2D plot the data 
#			     generated by the program.
#
#	numpy: This library was used to create a linespace (array) that helped
#	       with the plot of the function created to fit data.
#
#
# Function used to fit data:
#	f(x) = 7 * sin(.5*x) + 7
#
#	This function was used to fit the data because it fitted in a reasonable
#	way to the data's behavior. I agree that it is not the most accurate
#	function for this data.
#
# Files used:
#	In order to test the program the text file called generation.dat
#	was used. This file was provided by the lecturer.
#
# Github repository:
#	https://github.com/andresgtz/CE705-Assignment 
#-------------------------------------------------------------------------------

import sys, math, matplotlib.pyplot as plt, numpy as np

# Definition of function mean, this function calculates the mean value in
# a dictionary given as a parameter.

def mean(d):
	avg = 0
	for key,value in d.items():
		avg += value
	return avg / len(d)

#Definition of function sd, this function calculates the standard deviation
# in a dictionary providing as parameters the dictionary and its mean(avg) value

def sd(d, avg):
	s = 0
	for key,value in d.items():
		s += pow(value - avg,2)
	return math.sqrt(s/len(d))

# Definition of function RMSE, this function calculates the root mean square
# error between two lists of values with equal sizes.

def RMSE(l1,l2):
	result = 0
	if(len(l1) == len(l2)):
		for i in range(0,len(l1)):
			result += math.pow((l1[i] - l2[i]),2)
		result = result/len(l1)
	return math.sqrt(result)
#-------------------------------------------------------------------------------
# This section verifies if the user provides the file name via terminal, 
# if it is not provided, the correct way of using the program will be printed.
#-------------------------------------------------------------------------------

if(len(sys.argv) < 2):
	print("Usage: python3 solar.py <filename>",file=sys.stderr)
	exit(1)

# Dictionary declaration, this dictionary holds the sanitized input from the
# file provided in the terminal.
dicReadings = {} 

# Use try-except to open the file in order to protect it from abnormal 
# situations.

try:
	# Opens the file provided by the terminal with reading mode and names
	# the file stream as f
	with open(sys.argv[1],'r') as f:
		# Iterates the file reading line by line
		for line in f:
			# Conditional used to ignore comments and lines smaller
			# than 2 in length.
			if ('#' not in line and len(line) > 1):
				# use temporal array to split the
				# line to get each column, strips \n as well.
				line = line.rstrip()
				temp = line.split(' ') 
				# First column is the day number and 
				# second the recording.
				dicReadings[int(temp[0])] = float(temp[1])

# When there is a problem with the file, the except is executed.	
except:
	# Prints File Problem to the terminal and exits with a status 2.
	print("File Problem", file=sys.stderr)
	exit(2)

#-------------------------------------------------------------------------------
# This sections calculates the amounts generated per day
# by iterating through the dictionary that holds the sanitized input. 
# When the key is equal to the iterator it means that the data exists, therefore
# the calculation of the amount generated is the substraction between the days.
#
# When the key and the iterator have different values, the calculation considers
# the mean amount generated by last value and the first value of the gap 
# and writes this value to all the days in the gap.
#
# ex: if the dictionary holds values until the day 125 and it skips to 129
#     the calculation of the generated values in the gap between 125 and 129
#     is calculated by substracting the measure of the day 125 from the measure
#     of 129 and then diving it by the difference of days. This part of the code
#     is shown from lines 101 to 103.
#-------------------------------------------------------------------------------


genElec = {}
it = 1
for key in list(dicReadings.keys())[1:]:
	if(key == it):
		genElec[it] = dicReadings[it] - dicReadings[it-1]
	
	# In this case there is no measure for the day so we find an avg for 
	# the amount generated
	else:
		for i in range(it,key+1):
			genElec[i] = ((dicReadings[key] - dicReadings[it-1])/ 
					(key - (it - 1)))
		it = key	
	it += 1

#Print mean amount generated per day
print("\nMean amount generated:")
print(mean(genElec))

#Print min amount generated and day/s
print("\nMinimum amount generated: (day, amount)")
minValue = min(genElec.values())
for key,value in genElec.items():
	if(minValue == value):
		print(key, value)

#Print max amount generated and day/s
print("\nMaximum amount generated: (day, amount)")
maxValue = max(genElec.values())
for key,value in genElec.items():
	if(maxValue == value):
		print(key,value)

#-------------------------------------------------------------------------------
# In this section the program splits the genElec dictionary into chunks 
# of 30 days and calculate mean and std dev per chunk. 
#-------------------------------------------------------------------------------

# Initializes new list that will contain dictionaries (chunks) of 30 days
listGen = []
# Initilizes new dictionary that will contain 30 days of amounts, this 
# dictionary will be re initilized every time it is appended to listGen.
d= {}
# c is a counting variable that will keep track of how many days have been
# added to d.
c=0

for key,value in genElec.items():
	d[key] = value
	c += 1
	# When c is equal to 30 the dictionary that holds the chunk of 30 days
	# will be appended to listGen and the values of d and c reinitiliazed.
	if(c == 30):
		listGen.append(d)
		d={}
		c=0
	# This if adds the last chunk to listGen in the case that not all chunks
	# have exactly 30 days.
	elif(key == len(genElec)):
		listGen.append(d)


#-------------------------------------------------------------------------------
# In this section the program prints the
# mean and standard deviation of each chunk of 30 days.
#-------------------------------------------------------------------------------

print("\n--------Mean and Std.Deviation per chunk of 30 data--------")
c = 1
meanChunks = []
sdChunks = []
for i in listGen:
	print("\nChunk %d" % c)
	print("Mean: %f" % mean(i))
	meanChunks.append(mean(i))	
	print("Standard Deviation: %f" % sd(i,mean(i)))
	sdChunks.append(sd(i,mean(i)))
	c += 1

#-------------------------------------------------------------------------------
# In this section the program plots the mean values of the chunks, as well as
# the mean value plus one standar deviation, the mean value minus one standard
# deviation, and a function that fits to the data.
#-------------------------------------------------------------------------------

# PyPlot definitions
plt.grid(True)
plt.xlabel('Chunk')
plt.ylabel('Mean Amount Generated')


#Plot mean amount for each 30 day chunk	
plt.plot(list(range(1,c)),meanChunks, color = 'k')

#Plot mean amount plus one std deviation
meanPlusSD = []
for i in range(0,len(meanChunks)):
	meanPlusSD.append(meanChunks[i] + sdChunks[i])
plt.plot(list(range(1,c)),meanPlusSD, color = 'r')

#Plot mean amount minus one std deviation
meanMinusSD = []
for i in range(0,len(meanChunks)):
	meanMinusSD.append(meanChunks[i] - sdChunks[i])
plt.plot(list(range(1,c)),meanMinusSD, color = 'r')

#Plot function that fits to data (sine)
x = np.linspace(-7,50)

#Save values in a list for later calculation of RMSE
funValues = []
for i in range(1,len(meanChunks)+1):
	funValues.append(7*np.sin(.5*i) + 7)
		
plt.plot(7*np.sin(.5*x) + 7, color = 'g')
plt.show()

#-------------------------------------------------------------------------------
# At last, this section of the code calculates the Root Mean squared error 
# between the mean per chunks (meanChunks) and the values provided by the
# fitted function (funValues)
#-------------------------------------------------------------------------------

# Root mean square error calculation
print("------Calculation of RMSE------")
print(RMSE(meanChunks,funValues))
