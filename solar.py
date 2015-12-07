""" DESCRIPCION DEL PROGRAMA, PURPOSE, MIS DATOS"""

import sys, string, math

# Verify if the user gives the file name via terminal, if not print the correct
# way to use the program.

def mean(d):
	avg = 0
	for key,value in d.items():
		avg += value
	return avg / len(d)

def sd(d, avg):
	s = 0
	for key,value in d.items():
		s += pow(value - avg,2)
	return math.sqrt(s/len(d))

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
	else:
		for i in range(it,key+1):
			genElec[i] = (dicReadings[key] - dicReadings[it-1])/ (key - (it - 1))
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

#Split into chunks of 30 days and calculate mean and std dev per chunk
listGen = []
d= {}
c=0
for key,value in genElec.items():
	d[key] = value
	c += 1
	if(c == 30):
		listGen.append(d)
		d={}
		c=0
	if(key == len(genElec)):
		listGen.append(d)

#print mean and stdeviation per group of 30:
print("\n--------Mean and Std.Deviation pero chunk of 30 data--------")
c = 1
for i in listGen:
	print("\nChunk %d" % c)
	print("Mean: %f" % mean(i))
	print("Standard Deviation: %f" % sd(i,mean(i)))
	c += 1
#for i in listGen:
#	print("\n",i)	
