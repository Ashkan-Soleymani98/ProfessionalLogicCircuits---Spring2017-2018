file = open("RTL.txt", "r")
fileo = open("RTL_Verilog.v", "w")

fileName = file.readline().split(";")

fileName = fileName[1].replace("\n", "")
inputs = file.readline()
outputs = file.readline()
regs = file.readline()
states = file.readline()
if len(states.split(';')) == 1:
    states = ''
else:
    states = states.split(';')[1]

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
states = states.replace("\n", "")
# print(inputs)
# print(outputs)
# print(regs)
# print(states)

conditions = list()
registerAssignments = list()

for line in file:
    # print(line)
    # print(line.split( ";"))
    # line.replace('<-', '<=')
    tmp = line.split(";")
    conditions.append(tmp[0].replace("\n",""))
    registerAssignments.append(tmp[1].replace("\n",""))

# print(conditions)
# print(registerAssignments)
verilogCode = str()
# print(verilogCode)
inputs = inputs.split(",")
outputs = outputs.split(",")
regs = regs.split(",")
states = states.split(",")
verilogCode += "module " + fileName
pins = list()
pins.extend(["input wire " + inputs[i] for i in range(len(inputs))])
pins.extend(["input wire clock"])
pins.extend(['output reg ' + outputs[i] for i in range(len(outputs))])
for i in range(len(pins)):
    verilogCode += ("(" if i == 0 else "") + pins[i] + (", " if i != len(pins) - 1 else ");\n")

for i in range(len(regs)):
    verilogCode += "reg " + regs[i] + ';\n';

for i in range(len(states)):
    verilogCode += ("reg " if i == 0 else "") + states[i] + (", " if i != len(states) - 1 else ";\n")

verilogCode += "always@(posedge clock)\nbegin\n"
for i in range(len(conditions)):
    verilogCode += "\tif " + conditions[i] + "\n"
    verilogCode += "\tbegin\n"
    for k in registerAssignments[i].split(","):
        if str(k) != "":
            verilogCode += "\t\t" + str(k) + ";\n"
    verilogCode += "\tend\n"
verilogCode += "end\n"
verilogCode += "endmodule\n"

verilogCode = verilogCode.replace("<-", "<=")
print(verilogCode)
fileo.write(verilogCode)