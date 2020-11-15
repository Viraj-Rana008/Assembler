# ---------------------------------------------------- #
# Yeh 3 function comment handle karte hai
# ---------------------------------------------------- #

# file me se comment hata rha hu.
def removecomment(lines):
	# yeh function comments remove karta hai
	# * comments remove karne se emptyline string aur last me blank spaces
	# 	generate hote hai.
	# * blank spaces stripFinalInput function remove karta hai
	# * empty line string removeemptylines function remove karta hai
	for i in range(0,len(lines)):
		if (lines[i].find("//")==-1):
			pass
		else:
			lines[i]=lines[i][:lines[i].find("//")]
	pass

def removeemptylines(lines):
	# yeh function empty lines remove kar deta hai..
	# full line comment aur purposely empty line dono remove ho jati hai
	while ("" in lines):
		lines.remove("")
	pass

def stripFinalInput(lines):
	# Yeh funciton removeemptylines function ne jo outout
	# diya tha usme se last ke blank spaces remove kar deta hai
	# from every line
	for i in range(0,len(lines)):
		lines[i]=lines[i].strip()
	pass

# ---------------------------------------------------- #
# Yeh wala function start ke Error implement karta hai
# ---------------------------------------------------- #

def checkStart(startline):
	startline=startline.split(" ")
	# yeh function check karta hai ki start ki assumptions satisfy ho
	if (len(startline)>2):
		raise InvalidStartError("There are more than 2 arguments with start")
	elif (startline[0]!="START"):
		raise StartNotFoundError("Cannot find the start keyword")
	elif (len(startline)==2):
		if (isNumber(startline[1])==False):
			raise InvalidStartError("The address cannot be resolved to an int")
	pass


# ---------------------------------------------------- #
# 
# ---------------------------------------------------- #








def duplicateData(data,dataTable):
	for i in range(0,len(dataTable)):
		if (data==dataTable[i][0]):
			return True
	return False

def labelValue(label,labelTable):
	for i in range(0,len(labelTable)):
		if (label==labelTable[i][0]):
			return labelTable[i][1]

def dataValue(data,dataTable):
	for i in range(0,len(dataTable)):
		if (data==dataTable[i][0]):
			return dataTable[i][1]


def mcprint(code):
	for i in range(0, len(code)):
		for j in range(0,len(code[i])):
			if (j==len(code[i])-1):
				print(code[i][j])
			else:
				print(code[i][j],end=" ")


def printlist(lines):
	for i in lines:
		print(i)
	pass

def isNumber(s):
    for i in range(len(s)): 
        if (s[i].isdigit()!=True): 
            return False
    return True
    pass
  
def labelAddress(label,variableTable,startAddress,labelTable):
	# return label address in dec
	for i in range(0,len(variableTable)):
		if (label==variableTable[i][0]):
			return variableTable[i][2]-1+startAddress
	pass

def variableAddress(variable,variableTable,dataStartAddress):
	# return variable address in dec
	for i in range(0,len(variableTable)):
		if (variable==variableTable[i][0]):
			return dataStartAddress+i
	return -1
	pass

def decToBinary(n):
	# pass n as str or int
	# return type is str
	n= int (n)
	return bin(n).replace("0b", "")
	pass


def checkLiteral(literal):
	if (literal[0]=='='):
		return True
	else:
		return False


def literalValue(literal):
	literal=literal[1:]
	literal=decToBinary(literal)
	while (len(literal)<8):
		literal='0'+ str(literal)
	return literal

def dataValueInBin(data):
	data=decToBinary(data)
	while (len(data)<12):
		data='0'+ str(data)
	return data


opcodeTableOrig=[["CLA","0000"],
				 ["LAC","0001"],
				 ["SAC","0010"],
				 ["ADD","0011"],
				 ["SUB","0100"],
				 ["BRZ","0101"],
				 ["BRN","0110"],
				 ["BRP","0111"],
				 ["INP","1000"],
				 ["DSP","1001"],
				 ["MUL","1010"],
				 ["DIV","1011"],
				 ["STP","1100"]]
