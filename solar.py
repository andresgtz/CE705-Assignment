""" DESCRIPCION DEL PROGRAMA, PURPOSE, MIS DATOS"""

import sys, string

# Verify if the user gives the file name via terminal, if not print the correct
# way to use the program.

if(len(sys.argv) < 2):
	print("Usage: solar.py <filename>",file=sys.stderr)
	exit(1)

genElec = dicReadings = {} 

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

		
#Fill in for the missing values
prevKey = next(iter(dicReadings))
it = 0 
for key in list(dicReadings):
	if(it not in list(dicReadings)):
		it_temp = it
		for i in range(it_temp,key):
			genElec[i] = (dicReadings[key] - dicReadings[prevKey])/(key-prevKey)
			it +=1
	else:		
		genElec[it] = dicReadings[key] - dicReadings[prevKey]
		it += 1	
	prevKey = key


#Print mean amount generated per day
mean = 0
for key,value in genElec.items():
	mean += value	
mean = mean / max(genElec.keys())	
print(mean)
		
