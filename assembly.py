

## A simulator for uPOWER ISA instructions 

from collections import OrderedDict

# .text 0x 0000 0000 0040 0000 - 0x 0000 0000 1000 0000
# .data 0x 0000 0000 1000 0000 onwards


# ALL THE SECTION ADDRESSES

text_base = 0x400000
data_base = 0x10000000
stack_ptr = 0x3FFFFFFFF0

###########################

# ALL Registers section

## Will be populated while making simulator
## 32 General purpose registers
CIA = text_base # Current instruction address stored here
NIA = text_base+4 # Next instruction address
SRPO = 0

#############################

# supposed to get filename as arguement from command line
filename = "something.s"  
myfile = open(filename,'r')
codeLines = myfile.readlines() # will contain instructions and nextline characters and stray things we dont need as well
finalLines =[] # This will contain all the instructions and labels without stray characters
label_lines = {} # this dictionary maps labels to addresses


# Parsing the lines 

for i in range(len(codeLines)):
    if (codeLines[i]=='\n' or not codeLines[i].strip()):
        continue
    finalLines.append(codeLines[i].strip())

#############################


# storing text code and data  code in different lists
textlines = []
datalines = []

if finalLines[0]==".text":
    for i in range(1,len(finalLines)):
        if finalLines[i]==".data":
            datalines = finalLines[i+1:]
            break
        textlines.append(finalLines[i]) 

elif finalLines[0]==".data":
    for i in range(1,len(finalLines)):
        if finalLines[i]==".text":
            textlines = finalLines[i+1:]
            break
        datalines.append(finalLines[i])

# successfully divided into data section and text section

# now scanning the text section
linenum = 0
for line in textlines:
    words = line.split()
    if len(words)==1 and words[0][len(words[0])-1]==':':
        label_lines[words[0][:len(words[0])-1]]=hex(text_base + linenum*4)
        continue
    linenum = linenum+1

# print(label_lines)
# Correctly mapped labels to address

# Now to scan the data section 
# DATA TYPES 

# word 4 bytes
# halfword 2 bytes
# float 4 bytes
# double 8 bytes
# ascii - number of characters
# asciiz - number of characters + 1
Static_memory = {}
static_curr = 0
for line in datalines:
    words = line.split()
    variable_name = words[0][0:len(words[0])-1]
    datatype = words[1][1:]
    
    # To include the complete string
    initialize=''
    for i in range(2,len(words)-1):
        initialize = initialize + words[i] + ' '
    initialize = initialize + words[len(words)-1]


    if datatype == 'word' : 
        label_lines[variable_name] = hex(data_base + static_curr)
        Static_memory[hex(data_base + static_curr)] = int(initialize)
        static_curr = static_curr + 4
    elif datatype == 'halfword' : 
        label_lines[variable_name] = hex(data_base + static_curr)
        Static_memory[hex(data_base + static_curr)] = int(initialize)
        static_curr = static_curr + 2
    elif datatype == 'float' : 
        label_lines[variable_name] = hex(data_base + static_curr)
        Static_memory[hex(data_base + static_curr)] = float(initialize)
        static_curr = static_curr + 4
    elif datatype == 'double' : 
        label_lines[variable_name] = hex(data_base + static_curr)
        Static_memory[hex(data_base + static_curr)] = double(initialize)
        static_curr = static_curr + 8
    elif datatype == 'ascii' : 
        label_lines[variable_name] = hex(data_base + static_curr)
        initialize = initialize[1:len(initialize)-1]
        Static_memory[hex(data_base + static_curr)] = initialize
        static_curr = static_curr + len(initialize)
        
    elif datatype == 'asciiz' : 
        label_lines[variable_name] = hex(data_base + static_curr)
        initialize = initialize[1:len(initialize)-1]
        Static_memory[hex(data_base + static_curr)] = initialize + '\0'
        static_curr = static_curr + len(initialize)+1




# ALL LABELS HAVE BEEN MAPPED TO THEIR ADDRESSES
# USEFUL RESULTS ARE label_lines


# NOW FOR SECOND PASS TO CONVERT TO OBJECT CODE
def getnumbers(r_num,registers):
    for r in registers:
            r_num.append(bin(int(r[1:]))[2:].zfill(5))

def collectbinary(binaryterms,binarycode):
    for k,b in binaryterms.items():
        binarycode = binarycode + str(b)
    return binarycode
    

for line in textlines:
    words = line.split()
    if len(words)==1 and words[0][len(words[0])-1]==':':
        continue
    binarycode = ''
    # THESE ARE ALU INSTRUCTIONS 
    if words[0]=="add":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(31)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers)
        print(r_num)
        binaryterms["rt"] = r_num[0]
        binaryterms["ra"] = r_num[1]
        binaryterms["rb"] = r_num[2]
        binaryterms["oe"] = '0'
        binaryterms["xo"] = bin(266)[2:].zfill(9)
        binaryterms["rc"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)

    if words[0]=="addi":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(14)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers[:len(registers)-1])
        print(r_num)
	
        binaryterms["rt"] = r_num[0]
        binaryterms["ra"] = r_num[1]
        binaryterms["si"] = bin(int(registers[2]))[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)
        print(binaryterms)

    if words[0]=="addis":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(15)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers[:len(registers)-1])
        print(r_num)
        binaryterms["rt"] = r_num[0]
        binaryterms["ra"] = r_num[1]
        binaryterms["si"] = bin(int(registers[2]))[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)
        print(binaryterms)

    if words[0]=="and":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(31)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers)
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["rb"] = r_num[2]
        binaryterms["xo"] = bin(28)[2:].zfill(10)
        binaryterms["rc"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)

    if words[0]=="andi":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(28)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers[:len(registers)-1])
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["ui"] = bin(0)[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)

    if words[0]=="extsw":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(31)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers[:len(registers)-1])
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["rb"] = '00000'
        binaryterms["xo"] = bin(986)[2:].zfill(10)
        binaryterms["rc"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)
    
    if words[0]=="nand":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(31)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers)
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["rb"] = r_num[2]
        binaryterms["xo"] = bin(476)[2:].zfill(10)
        binaryterms["rc"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)

    if words[0]=="or":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(31)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers)
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["rb"] = r_num[2]
        binaryterms["xo"] = bin(444)[2:].zfill(10)
        binaryterms["rc"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)

    if words[0]=="ori":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(24)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers[:len(registers)-1])
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["ui"] = bin(0)[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)

    if words[0]=="subf":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(31)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers)
        print(r_num)
        binaryterms["rt"] = r_num[0]
        binaryterms["ra"] = r_num[1]
        binaryterms["rb"] = r_num[2]
        binaryterms["oe"] = '0'
        binaryterms["xo"] = bin(40)[2:].zfill(9)
        binaryterms["rc"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)

    if words[0]=="xor":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(31)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers)
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["rb"] = r_num[2]
        binaryterms["xo"] = bin(316)[2:].zfill(10)
        binaryterms["rc"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)
    
    if words[0]=="xori":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(26)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers[:len(registers)-1])
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["ui"] = bin(0)[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)
    #############################################################
    
    if(words[0]=="ld"):
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(58)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        temp = temp[:len(temp)-1]
        a1 = temp.split(",")
        registers = []
        registers.append(a1[0])
        a2 = a1[1].split("(")
        registers.append(a2[1])
        offset = int(a2[0])
        r_num = []
        getnumbers(r_num,registers)
        binaryterms["rt"] = r_num[0]
        binaryterms["rs"] = r_num[1]
        binaryterms["ds"] = bin(offset)[2:].zfill(14)
        binaryterms["xo"] = "00"
        binarycode = collectbinary(binaryterms,binarycode)
      
    if(words[0]=="lwz"):
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(32)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        temp = temp[:len(temp)-1]
        a1 = temp.split(",")
        registers = []
        registers.append(a1[0])
        a2 = a1[1].split("(")
        registers.append(a2[1])
        offset = int(a2[0])
        r_num = []
        getnumbers(r_num,registers)
        binaryterms["rt"] = r_num[0]
        binaryterms["rs"] = r_num[1]
        binaryterms["ds"] = bin(offset)[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)
       
    if(words[0]=="std"):
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(62)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        temp = temp[:len(temp)-1]
        a1 = temp.split(",")
        registers = []
        registers.append(a1[0])
        a2 = a1[1].split("(")
        registers.append(a2[1])
        offset = int(a2[0])
        r_num = []
        getnumbers(r_num,registers)
        binaryterms["rt"] = r_num[0]
        binaryterms["rs"] = r_num[1]
        binaryterms["ds"] = bin(offset)[2:].zfill(14)
        binaryterms["xo"] = "00"
        binarycode = collectbinary(binaryterms,binarycode)
       
    if(words[0]=="stw"):
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(36)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        temp = temp[:len(temp)-1]
        a1 = temp.split(",")
        registers = []
        registers.append(a1[0])
        a2 = a1[1].split("(")
        registers.append(a2[1])
        offset = int(a2[0])
        r_num = []
        getnumbers(r_num,registers)
        binaryterms["rt"] = r_num[0]
        binaryterms["rs"] = r_num[1]
        binaryterms["ds"] = bin(offset)[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)
     
    if(words[0]=="stwu"):
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(37)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        temp = temp[:len(temp)-1]
        a1 = temp.split(",")
        registers = []
        registers.append(a1[0])
        a2 = a1[1].split("(")
        registers.append(a2[1])
        offset = int(a2[0])
        r_num = []
        getnumbers(r_num,registers)
        binaryterms["rt"] = r_num[0]
        binaryterms["rs"] = r_num[1]
        binaryterms["ds"] = bin(offset)[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)
        
    if(words[0]=="lhz"):
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(40)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        temp = temp[:len(temp)-1]
        a1 = temp.split(",")
        registers = []
        registers.append(a1[0])
        a2 = a1[1].split("(")
        registers.append(a2[1])
        offset = int(a2[0])
        r_num = []
        getnumbers(r_num,registers)
        binaryterms["rt"] = r_num[0]
        binaryterms["rs"] = r_num[1]
        binaryterms["ds"] = bin(offset)[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)
    
    if(words[0]=="lha"):
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(42)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        temp = temp[:len(temp)-1]
        a1 = temp.split(",")
        registers = []
        registers.append(a1[0])
        a2 = a1[1].split("(")
        registers.append(a2[1])
        offset = int(a2[0])
        r_num = []
        getnumbers(r_num,registers)
        binaryterms["rt"] = r_num[0]
        binaryterms["rs"] = r_num[1]
        binaryterms["ds"] = bin(offset)[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)
       
    if(words[0]=="sth"):
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(44)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        temp = temp[:len(temp)-1]
        a1 = temp.split(",")
        registers = []
        registers.append(a1[0])
        a2 = a1[1].split("(")
        registers.append(a2[1])
        offset = int(a2[0])
        r_num = []
        getnumbers(r_num,registers)
        binaryterms["rt"] = r_num[0]
        binaryterms["rs"] = r_num[1]
        binaryterms["ds"] = bin(offset)[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)
       
    if(words[0]=="lbz"):
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(34)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        temp = temp[:len(temp)-1]
        a1 = temp.split(",")
        registers = []
        registers.append(a1[0])
        a2 = a1[1].split("(")
        registers.append(a2[1])
        offset = int(a2[0])
        r_num = []
        getnumbers(r_num,registers)
        binaryterms["rt"] = r_num[0]
        binaryterms["rs"] = r_num[1]
        binaryterms["ds"] = bin(offset)[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)
    
    if(words[0]=="stb"):
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(38)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        temp = temp[:len(temp)-1]
        a1 = temp.split(",")
        registers = []
        registers.append(a1[0])
        a2 = a1[1].split("(")
        registers.append(a2[1])
        offset = int(a2[0])
        r_num = []
        getnumbers(r_num,registers)
        binaryterms["rt"] = r_num[0]
        binaryterms["rs"] = r_num[1]
        binaryterms["ds"] = bin(offset)[2:].zfill(16)
        binarycode = collectbinary(binaryterms,binarycode)
        
    
#########################################################################

    if words[0] == "rlwinm" :
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(21)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers[:2])
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["sh"] = bin(int(registers[2]))[2:].zfill(5)
        binaryterms["mb"] = bin(int(registers[3]))[2:].zfill(5)
        binaryterms["me"] = bin(int(registers[4]))[2:].zfill(5)
        binaryterms["rc"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)
        print(binaryterms)

    if words[0]=="sld":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(31)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers)
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["rb"] = r_num[2]
        binaryterms["xo"] = bin(27)[2:].zfill(10)
        binaryterms["rc"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)

    if words[0]=="srd":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(31)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers)
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["rb"] = r_num[2]
        binaryterms["xo"] = bin(539)[2:].zfill(10)
        binaryterms["rc"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)

    if words[0]=="srad":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(31)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers)
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["rb"] = r_num[2]
        binaryterms["xo"] = bin(794)[2:].zfill(10)
        binaryterms["rc"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)

    if words[0]=="sradi":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(31)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        r_num = []
        getnumbers(r_num,registers[:len(registers)-1])
        sh = bin(int(registers[2]))[2:].zfill(6)
        print(r_num)
        binaryterms["rs"] = r_num[1]
        binaryterms["ra"] = r_num[0]
        binaryterms["sh1"] = sh[:5]
        binaryterms["xo"] = bin(413)[2:].zfill(9)
        binaryterms["sh2"] = sh[5]
        binaryterms["rc"] = '0' 
        binarycode = collectbinary(binaryterms,binarycode)
    #############################################################
    
    if words[0] == "b":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(18)[2:].zfill(6)
        li = bin(int(words[1]))[2:].zfill(24);
        binaryterms["li"] = li
        binaryterms["aa"] = '0'
        binaryterms["lk"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)
        print(binaryterms)
    if words[0] == "ba":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(18)[2:].zfill(6)
        li = bin(int(words[1]))[2:].zfill(24);
        binaryterms["li"] = li
        binaryterms["aa"] = '1'
        binaryterms["lk"] = '0'
        binarycode = collectbinary(binaryterms,binarycode)
        print(binaryterms)
    if words[0] == "bl":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(18)[2:].zfill(6)
        li = bin(int(words[1]))[2:].zfill(24);
        binaryterms["li"] = li
        binaryterms["aa"] = '0'
        binaryterms["lk"] = '1'
        binarycode = collectbinary(binaryterms,binarycode)
        print(binaryterms)
    if words[0] == "bc":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(19)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        binaryterms['bo'] = bin(int(registers[0]))[2:].zfill(5)
        binaryterms['bi'] = bin(int(registers[1]))[2:].zfill(5)
        binaryterms["bd"] = bin(int(label_lines[registers[2]],16))[2:].zfill(15)
        binaryterms["aa"] = "0"
        binaryterms["lk"] = "0"
        binarycode = collectbinary(binaryterms,binarycode)
    if words[0] == "bca":
        binaryterms = OrderedDict()
        binaryterms["po"] = bin(19)[2:].zfill(6)
        temp=''
        for i in range(1,len(words)):
            temp = temp + words[i]
        registers = temp.split(",")
        binaryterms['bo'] = bin(int(registers[0]))[2:].zfill(5)
        binaryterms['bi'] = bin(int(registers[1]))[2:].zfill(5)
        binaryterms["bd"] = bin(int(label_lines[registers[2]],16))[2:].zfill(15)
        binaryterms["aa"] = "1"
        binaryterms["lk"] = "0"
        binarycode = collectbinary(binaryterms,binarycode)
    









        

        
        


    


      

      

    
    



        
        
        
    
     
     
    



    








    





        

        



    
    
    




















