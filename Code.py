from Errors import *
from functions import *
import random

fileName=input("Enter the file name with extension=")

with open(fileName) as f:
    lines = [line.rstrip() for line in f]

# Raise an error if the input file is empty
if (len(lines)==0):
	raise EmptyFileError("Input file is Empty")



# file me se comment hata rha hu.
def commentHandling(lines):
	removecomment(lines)
	removeemptylines(lines)
	stripFinalInput(lines)
	pass


# printing orginal program input without comments and empty line
print("Input after removing blank spaces from last")
print("---------------")
printlist(lines)
print("---------------")


# ---------------------------------------------------- #
# yha tak input bilkul set hai.... now I have to deal with start and stop first
# umm, i think stop already ho chuka hai sirf start ko dekhna hai...
# and try karna hai ki niche ke fucntion na change karne pade..
# ---------------------------------------------------- #


# yeh function check karta hai ki start ki assumptions satisfy ho
checkStart(lines[0])

# yeh function startAddress ko value assign karta hai
# cannot be transfered to functions.py as it uses global startAddress
startAddress=0
def startAddressIni(startline):
	global startAddress
	startline=startline.split(" ")
	if (len(startline)==1):
		pass
	else:
		startAddress=startline[1]
startAddressIni(lines[0])

# printing start address
print("---------------")
print("startAddress="+str(startAddress))
print("---------------")

# removing start wali line. that line cannot be converted 
# as their is no start opcode
lines=lines[1:]


labelTable=[]
# label table=[labelKaNaam LabelkaLineNo]
def labelTableIni(lines,labelTable):
	# yeh functio label table ko initialize karta hai..
	# [label] opcode [operand]: [label] CLA or [label] !=CLA operand
	# agar label aeyega toh line ki len 2 ya 3 hi hogi
	# for conditions see if-else comments:

	for i in range(0,len(lines)):
		currentLine=lines[i].split(" ")
		if (len(currentLine)==1):
			# agar len==1 hai then it cannot be label
			pass
		elif (len(currentLine)==2):
			# handle CLA wala case i.e,
			# agar Label CLA hai toh append warna
			# opcode operand rha hoga---ignore
			if (currentLine[1]=="CLA" or currentLine[1]=="STP"):
				labelTable.append([currentLine[0],i+1])
			else:
				pass
		elif (len(currentLine)==3):
			# label opcode operand wala case where opcode!=CLA
			# in that case label hoga
			labelTable.append([currentLine[0],i+1])
		else:
			# agar len >3 ya <1 hai toh operand jyada hue
			# honge ya kuch galat likh diya hoga;
			raise InvalidLineError("Line galat hai..maybe ek se jyda opr hai")
		pass
labelTableIni(lines,labelTable)


# printing label table
print("---------------")
print("Label Table")
printlist(labelTable)
print("---------------")


# Helper function 
def checkLabel(label,labelTable):
	# yeh function check karta hai ki 
	# 'label'(parameter wala) koi label toh nhi hai
	# if yes --> then true
	# if no --> then false
	for i in range(0,len(labelTable)):
		if (label==labelTable[i][0]):
			return True
	return False
	pass


# Helper function 
def bicode(opcode,opcodeTableOrig):
	# yeh opcode ke corresponding 4 digit bicode return karta hai
	# agar opcode galat hai--> uske sath ka bicode nhi mila 
	# --> "" return karta hai
	for i in range(0,len(opcodeTableOrig)):
		if (opcodeTableOrig[i][0]==opcode):
			return opcodeTableOrig[i][1]
	return ""
	pass


opcodeTable=[]
# opcodeTable=[opcode(naam) lineno(i+1) bicode(from origTable) opnd(if !=CLA)]
def opcodeTableIni(lines,opcodeTable,labelTable,opcodeTableOrig):
	k=0
	# add how function works
	for i in range(0,len(lines)):
		currentLine=lines[i].split(" ")

		if (len(currentLine)==1):
			if (currentLine[0]=="CLA" or currentLine[0]=="STP"):
				opcodeTable.append([currentLine[0],i+1,bicode(currentLine[0],opcodeTableOrig),"--"])
				k+=1
			#elif (currentLine[0]=="STP"):
			#	break
			else:
				raise InsufficeintOperandError("opcode !=CLA and operand specify nhi kara")
		elif (len(currentLine)==2):
			flag=checkLabel(currentLine[0],labelTable)
			if (flag==True):
				opcodeTable.append([currentLine[1],i+1,bicode(currentLine[1],opcodeTableOrig),"--"])
			else:
				opcodeTable.append([ currentLine[0],i+1,bicode(currentLine[0],opcodeTableOrig),currentLine[1] ])
			k+=1
		elif (len(currentLine)==3):
			flag=checkLabel(currentLine[0],labelTable)
			if (flag and currentLine[1]=="CLA"):
				opcodeTable.append(["CLA",i+1,bicode("CLA",opcodeTableOrig),"--"])
			else:
				opcodeTable.append([ currentLine[1],i+1,bicode(currentLine[1],opcodeTableOrig),currentLine[2] ])
			k+=1
		else:
			raise ExtraOperandError("len >3 aise kaise....")

		# bicode opcode ke corresponding bicode return karta hai
		# agar opcode nhi mila toh "" return karta hai => if bicode==""
		# matlab woh opcode original table me nhi mila.
		if (opcodeTable[k-1][2]==""):
			raise InvalidOpcodeError("Opcode ke correcponding bicode nhi mil rha")
		pass
opcodeTableIni(lines,opcodeTable,labelTable,opcodeTableOrig)

print("---------------")
print("opcode Table")
printlist(opcodeTable)
print("---------------")


# Helper function
def validVariable(variable):
	# check variable ka naam --> function ki job
	# if it starts with digit -->return False --> raise Error
	# if it is not alphanumeric -->return False --> raise Error
	# --> a21as is a valid name here
	if (variable[0].isdigit()==True):
		return False
	if (variable.isalnum()==False):
		return False
	return True
	pass

# Helper function
def checkValidLiteral(operand):
	# operand me se number extract karta hai(literal wala case)
	# agar number float hai toh error
	# agar sirf '=' hai toh error
	# agar aisa kuch '=as22' hai toh error --> agar =ke baad number nhi hai toh
	# return -->operand
	if (len(operand)==1):
		raise NoLiteralError("'=' hai par literal hi nhi hai")
	
	operand=operand[1:]
	if ("." in operand):
		raise InvalidLiteralError("literal float hai--- int chahiye")
	if (not isNumber(operand)):
		raise InvalidLiteralError("literal kuch alag hi hai--- int chahiye")
	return operand
	pass


def duplicateVariable(variable,variabletable):
	for i in range(0,len(variabletable)):
		if (variable==variabletable[i][0]):
			return True
	return False


literalTable=[]
variableTable=[]
# literalTable = [literal(no in str) lineNo]
# variabletable = [operand(variablekanaam) linoNo value]
def literalVariableTableIni(opcodeTable,literalTable,variableTable):
	# just iterate over opcodetable instead of whole file
	# beacuse every line contains a opcode for sure
	# yeh function literal aur variable table dono ek sath 
	# initialize kar deta hai
	for i in range(0,len(opcodeTable)):
		operand=opcodeTable[i][3]

		# check if there is duplicate variable --> yes -->error
		# if no operand --> CLA or STP --> continue
		if (operand=="--"):
			continue
		elif (operand[0]=="="):
			# if value is literal
			# checkValidLiteral apne aap error raise kar deta hai and
			# agar koi error nhi hai toh literal return kar deta hai
			literal=checkValidLiteral(operand)
			literalTable.append([literal,opcodeTable[i][1]])
		else:
			# if value is not lieral --> variable
			if (duplicateVariable(operand,variableTable)):
				pass
			else:
				variableTable.append([operand,opcodeTable[i][1],0])
				if (validVariable(operand)==False):
					raise invalidVariableError("Variable ka naam galat hai -- see assumptions")
	pass
literalVariableTableIni(opcodeTable,literalTable,variableTable)

print("---------------")
print("literal Table")
printlist(literalTable)
print("---------------")

dataTable=[]
# dataTable = [variable(name) value]
def duplicateData(data,dataTable):
	for i in range(0,len(dataTable)):
		if (data==dataTable[i][0]):
			return True
	return False

def dataTableIni(dataTable,variableTable):
	# yeh function dataTable create karta hai by iterating over variableTable
	# value random manlo abhi ke liye;
	for i in range(0,len(variableTable)):
		if (duplicateData(variableTable[i][0],dataTable)):
			pass
		if (checkLabel(variableTable[i][0],labelTable)):
			pass
		else:
			dataTable.append([variableTable[i][0],random.randint(0,10*i)])
	pass
dataTableIni(dataTable,variableTable)


def variableTableReini(variableTable,labelTable,dataTable):
	for i in range(0,len(variableTable)):
		if ( checkLabel(variableTable[i][0],labelTable) ):
			variableTable[i][2]=labelValue(variableTable[i][0],labelTable)
		else:
			variableTable[i][2]=dataValue(variableTable[i][0],dataTable)
variableTableReini(variableTable,labelTable,dataTable)


print("---------------")
print("variable Table")
printlist(variableTable)
print("---------------")

print("---------------")
print("dataTable:")
printlist(dataTable)
print("---------------")


# ---------------------------------------------------- #
# yha tak sari table ban chuki hai including niche ka .data wala part
# ---------------------------------------------------- #

machine1=[]
machine2=[]
# machine1=[address opcode operand(either operand add or label add)]
# machine me data wala part me variable ke sath uski value prit kar do
# machine2 me variable ke sath value ki binary value print kar do
startAddress=int(startAddress)
dataStartAddress=int(startAddress)+len(opcodeTable)


def labelInBinary(label,variableTable,startAddress,labelTable):
	# return label address in bin in 8 bits
	labelAdd=labelAddress(label,variableTable,startAddress,labelTable)
	labelAdd=decToBinary(labelAdd)
	while (len(labelAdd)<8):
		labelAdd='0'+str(labelAdd)
	return labelAdd
	pass

def variableInBinary(variable,variableTable,dataStartAddress):
	# return variable address in bin in 8 bits
	variableAdd=variableAddress(variable,variableTable,dataStartAddress)
	if (variableAdd==-1):
		return -1

	variableAdd=decToBinary(variableAdd)
	while (len(variableAdd)<8):
		variableAdd='0'+ str(variableAdd)
	return variableAdd
	pass

def addressInBin(address):
	address=decToBinary(address)
	while (len(address)<8):
		address='0'+ str(address)
	return address
	pass

def machine1Ini(machine1,opcodeTable,labelTable,variableTable,startAddress,dataStartAddress):
	address=startAddress
	for i in range(0,len(opcodeTable)):
		currentAdd=addressInBin(address+i)
		if ( checkLabel(opcodeTable[i][3],labelTable) ):
			labelInBin=labelInBinary(opcodeTable[i][3],variableTable,startAddress,labelTable)
			machine1.append([currentAdd,opcodeTable[i][2],labelInBin])
		elif ( checkLiteral(opcodeTable[i][3]) ):
			value=literalValue(opcodeTable[i][3])
			machine1.append([currentAdd,opcodeTable[i][2],value])
		else:
			variableAddress=variableInBinary(opcodeTable[i][3],variableTable,dataStartAddress)
			if (variableAddress==-1):
				machine1.append([currentAdd,opcodeTable[i][2],"00000000"])
			else:
				machine1.append([currentAdd,opcodeTable[i][2],variableAddress])
	
	machine1.append([".DATA"])
	for i in range(0,len(dataTable)):
		currentAdd=addressInBin(dataStartAddress+i)
		valueInBin=decToBinary(dataTable[i][1])
		machine1.append([currentAdd,dataTable[i][1]])
	pass
machine1Ini(machine1,opcodeTable,labelTable,variableTable,startAddress,dataStartAddress)

print("---------------")
print("machine1:")
mcprint(machine1)
print("---------------")

def machine2Ini(machine2,opcodeTable,labelTable,variableTable,startAddress,dataStartAddress):
	address=startAddress
	for i in range(0,len(opcodeTable)):
		currentAdd=addressInBin(address+i)
		if ( checkLabel(opcodeTable[i][3],labelTable) ):
			labelInBin=labelInBinary(opcodeTable[i][3],variableTable,startAddress,labelTable)
			machine2.append([currentAdd,opcodeTable[i][2],labelInBin])
		elif ( checkLiteral(opcodeTable[i][3]) ):
			value=literalValue(opcodeTable[i][3])
			machine2.append([currentAdd,opcodeTable[i][2],value])
		else:
			variableAddress=variableInBinary(opcodeTable[i][3],variableTable,dataStartAddress)
			if (variableAddress==-1):
				machine2.append([currentAdd,opcodeTable[i][2],"00000000"])
			else:
				machine2.append([currentAdd,opcodeTable[i][2],variableAddress])
	
	machine2.append([".DATA"])
	for i in range(0,len(dataTable)):
		currentAdd=addressInBin(dataStartAddress+i)
		machine2.append([currentAdd,dataValueInBin(dataTable[i][1])])
	pass
machine2Ini(machine2,opcodeTable,labelTable,variableTable,startAddress,dataStartAddress)

print("---------------")
print("machine2:")
mcprint(machine2)
print("---------------")
