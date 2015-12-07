""" DESCRIPCION DEL PROGRAMA, PURPOSE, MIS DATOS"""

import sys, string

# Verify if the user gives the file name via terminal, if not print the correct
# way to use the program.

if(len(sys.argv) < 2):
	print("Usage: solar.py <filename>",file=sys.stderr)
	exit(1)

dicReadings = {} 

#Use try-except to open the file in order to protect it.
try:
	with open(sys.argv[1],'r') as f:
		for line in f:
			#Ignore commented lines
			if ('#' not in line and len(line) > 1):
				#use temporal array to split line to get each column
				line = line.rstrip()
				temp = line.split(' ') 
				#First column is the day number and second the recording
				dicReadings[int(temp[0])] = float(temp[1])
	
		
except:
	print("File Problem", file=sys.stderr)
	exit(2)

		
#Calculate amounts generated per day
genElec = {}
it = 1
for key in list(dicReadings.keys())[1:]:
	if(key == it):
		genElec[it] = dicReadings[it] - dicReadings[it-1]
	#In this case there is no measure for the day so we find an avg for the amount generated
	elif(it != key):
		for i in range(it,key):
			genElec[i] = (dicReadings[key] - dicReadings[it-1])/ (key - (it - 1))
		it = key	
	it += 1


#Print mean amount generated per day
print("\nMean amount generated:")
mean = 0
for key,value in genElec.items():
	mean += value	
mean = mean / max(genElec.keys())	
print(mean)

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
