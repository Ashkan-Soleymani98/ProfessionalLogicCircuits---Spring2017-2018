
maxStates = 12
maxBoxes = 12
maxRegisters = 12

nextBoxTrue = [-1] * maxBoxes
nextBoxFalse = [-1] * maxBoxes
conditionString = [''] * maxBoxes
conditions = [''] * maxBoxes
stateOfBox = [-1] * maxBoxes
boxType = ['NA'] * maxBoxes

registerNames = []
boxRegisterAssignments = [''] * maxBoxes
blockRegisterAssignments = [[] for i in range(maxStates)]
blockNextState = [[] for i in range(maxStates)]

file = open("ASM.txt", "r")
outputFile = open("ASM_Verilog.v", "w")

numOfBoxes = 0


def BFS(node, stateID):

    # print(node)
    stateOfBox[node] = stateID

    x = int(nextBoxTrue[node])
    y = int(nextBoxFalse[node])
    # print(x + 5)
    # print(boxType[x])
    # print('============================')
    if x != -1 and boxType[x] != 'NA' and boxType[x] != 'SB':
        # print('BFS on X')
        BFS(x, stateID)

    if y != -1 and boxType[y] != 'NA' and boxType[y] != 'SB':
        # print('BFS on Y')
        BFS(y, stateID)


def ConditionFinderBFS(node, currentConditions):
    # print(str(node) + ' $$$$ ' + str(currentConditions))
    conditions[node] = currentConditions
    conditionTrue = currentConditions
    conditionFalse = currentConditions
    if boxType[node] == 'DB':
        if currentConditions == '':
            conditionTrue = conditionString[node]
            conditionFalse = '(!' + conditionString[node] +')'
        else:
            conditionTrue = '(' + conditionTrue + ' && ' + conditionString[node] + ')'
            conditionFalse = '(' + conditionFalse + ' && !' + conditionString[node] + ')'

    x = int(nextBoxTrue[node])
    y = int(nextBoxFalse[node])

    if x != -1 and boxType[x] != 'NA':
        if boxType[x] != 'SB':
            ConditionFinderBFS(x, conditionTrue)

    if y != -1 and boxType[y] != 'NA':
        if boxType[y] != 'SB':
            ConditionFinderBFS(y, conditionFalse)

fileName = file.readline().split(";")
fileName = fileName[1].replace("\n", "")

inputs = file.readline()
outputs = file.readline()
regs = file.readline()

if len(regs.split(';')) == 1:
    regs = ''
else:
    regs = regs.split(';')[1]

if len(inputs.split(';')) == 1:
    inputs = ''
else:
    inputs = inputs.split(';')[1]

if len(outputs.split(';')) == 1:
    outputs = ''
else:
    outputs = outputs.split(';')[1]
inputs = inputs.replace("\n", "")
outputs = outputs.replace("\n", "")
regs = regs.replace("\n", "")
# print(inputs + '\n' + outputs)


for line in file:
    numOfBoxes += 1
    # print('+++++++++++++++++++++++++++++++')
    # print(line[0:len(line)-1])
    id = line.split("(")[0]
    id = int(id)
    typo = line.replace(')', '(')
    type = typo.split('(')[1]
    boxType[id] = type

    if type == 'DB':
        conditionString[id] = line.split(';')[1].split('?')[0]
        nextBoxTrue[id]    = line.split('?')[1].split(';')[0]
        tmp = line.split('?')[1].split(';')[1]
        nextBoxFalse[id]     = (tmp)[0:len(tmp)-1]

    if type == 'SB' or type == 'CB':
        tmp = line.split(',')
        #print(tmp[len(tmp)-1].split('=')[1])
        nextBoxTrue[id] = int(tmp[len(tmp)-1].split('=')[1])
        nextBoxFalse[id] = int(tmp[len(tmp)-1].split('=')[1])
        #print(str(nextBoxTrue[id]) + ' ' + str(nextBoxFalse[id]))
        # assignments = line.split(':')[1].split(',')
        # assignments = assignments[0:len(assignments)-1]
        tmp = line.replace(',out=', ',;')
        #print(tmp.split(':'))
        if len(tmp.split(';')) > 2:
            #print(tmp.split(':')[1])
            assignments = tmp.split(';')[1]
            boxRegisterAssignments[id] =  assignments[0:len(assignments)-1]
            #print(boxRegisterAssignments[id])

stateID = 1
for i in range(maxBoxes):
    if boxType[i] == 'SB':
        BFS(i, stateID)
        ConditionFinderBFS(i, '')
        stateID += 1
numOfStates = stateID

# for i in range(numOfBoxes):
#     print("=============\n")
#     print(str(i) + ':   ' + conditions[i])
#     print(nextBoxTrue[i])
#     print(nextBoxFalse[i])
#     print("=============\n")

# for i in range(numOfBoxes):
#     print(str(i) + ':   ' + conditionString[i])
#
for i in range(numOfBoxes+1):
    if boxType[i] != 'NA':
        print('=====================\n Box number ' + str(i) +
              ' :\n state = ' + str(stateOfBox[i]) +
              ' \n operations done in this box:\n ' +
              conditions[i] + ' : ' + str(boxRegisterAssignments[i]))

        blockRegisterAssignments[stateOfBox[i]].append([boxRegisterAssignments[i]])
        if boxType[i] == 'DB':

            if boxType[int(nextBoxTrue[i])] == 'SB':
                tmp = conditionString[i]
                if len(conditions[i]) > 0:
                    tmp = '(' + tmp + ' && ' + conditions[i] + ')'
                blockNextState[stateOfBox[i]].append(tmp + ' ==> ' + str(stateOfBox[int(nextBoxTrue[i])]))

            if boxType[int(nextBoxFalse[i])] == 'SB':
                tmp = '(!' + conditionString[i] +')'
                if len(conditions[i]) > 0:
                    tmp = '(' + tmp + ' && ' + conditions[i] + ')'
                blockNextState[stateOfBox[i]].append(tmp + ' ==> ' + str(stateOfBox[int(nextBoxFalse[i])]) )

        if boxType[i] == 'CB' or boxType[i] == 'SB':
            if boxType[int(nextBoxTrue[i])] == 'SB':
                blockNextState[stateOfBox[i]].append(conditions[i] + ' ==> ' + str(stateOfBox[int(nextBoxTrue[i])]))




# print('=====================\n')


# for i in range(numOfStates-1):
#     print('----------------------\n StateNumber ' + str(i+1) +
#           '\n' + str(blockNextState[i+1]) + '\n-------------------------\n')

numOfStates = stateID - 1

verilogCode = str()
# print(verilogCode)
inputs = inputs.split(",")
outputs = outputs.split(",")
regs = regs.split(",")
verilogCode += "module " + fileName
pins = list()
pins.extend(["input wire " + inputs[i] for i in range(len(inputs))])
pins.extend(["input wire clock"])
pins.extend(['output reg ' + outputs[i] for i in range(len(outputs))])
for i in range(len(pins)):
    verilogCode += ("(" if i == 0 else "") + pins[i] + (", " if i != len(pins) - 1 else ");\n")

for i in range(len(regs)):
    verilogCode += "reg " + regs[i] + ';\n';

firstBox = None
for i in range(maxBoxes):
    if boxType[i] != 'NA':
        firstBox = i
        break

verilogCode += "integer blockNum = " + str(firstBox) + ", nextBlock;\n"
verilogCode += "always@(posedge clock)\nbegin\n"
if firstBox is not None:
    for i in range(numOfStates):
        verilogCode += "\t" + ("if" if i == 0 else "else if") + "(blockNum == " + str(i + 1) + ")\n"
        verilogCode += "\tbegin\n"
        counter = 0
        for j in range(maxBoxes):
            if boxType[j] != 'NA' and stateOfBox[j] == i + 1 and (len(boxRegisterAssignments[j]) > 1):
                if conditions[j] != " " and conditions[j] != '':
                    verilogCode += "\t\t" + "if " + conditions[j] + "\n"
                    verilogCode += "\t\tbegin\n"
                    for k in boxRegisterAssignments[j].split(","):
                        if str(k) != "":
                            verilogCode += "\t\t\t" + str(k) + ";\n"
                    verilogCode += "\t\tend\n"
                    counter += 1
                elif str(boxRegisterAssignments[j]) != " ":
                    for k in boxRegisterAssignments[j].split(","):
                        if str(k) != " " and str(k) != "":
                            verilogCode += "\t\t" + str(k) + ";\n"

        # verilogCode += str(blockNextState[i+1]) + "\n"
        for j in blockNextState[i+1]:
            condition = j.split(' ==> ')[0]
            nextState = j.split(' ==> ')[1]
            # print(j + ' 55555555555555555  ' + str(blockNextState[i+1][1]))
            if j != blockNextState[i+1][0]:
                verilogCode += "\t\telse if"
            else:
                verilogCode += "\t\tif"
            verilogCode += condition + "\n"
            # verilogCode += "\t\tbegin\n"
            verilogCode += "\t\t\tblockNum <= " + nextState +";\n"

        verilogCode += "\tend\n"
    # verilogCode += '\n\tblockNum = nextBlock;\n'
verilogCode += "end\n"
verilogCode += "endmodule\n"

print(conditions)
print("\n\n~~~~~~~~.:verilogCode:.~~~~~~~\n\n")
print(verilogCode)
outputFile.write(verilogCode)