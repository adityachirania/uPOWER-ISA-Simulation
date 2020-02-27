# The following simulator reads the object code and does operations
from assembly import label_lines # the address of the labels 
from assembly import Static_memory #the main memory contents of static data
from assembly import Instructions

print(Instructions)

text_base = 0x400000 #base address of the text section
data_base = 0x10000000 #base address of the data section 
stack_ptr = 0x3FFFFFFFF0 #stack pointer

# Now we need 32 registers and all purpose      
def int2(s):
    value = -1*int(s[0])*(2**15)
    for i in range(1,16):
        value = value + (int(s[i])*(2**(15-i)))
    return value

# General purpose registers
Registers=[]
for i in range(32):
    Registers.append(0)
# Special purpose registers
CIA = text_base # current instruction address
NIA = text_base+4 # next instruction address
SRRO = 0 # register to store return address after system call
CR = 0 # Condition register

last_instruction = text_base + (len(Instructions)-1)*4
while CIA <= last_instruction:
    instruction = Instructions[hex(CIA)] # STORE CURRENT INSTRUCTION IN VARIABLE 'instruction'

    # Checking if the instruction is an "add" instruction
    if int(instruction[0:6],2)==31 and instruction[21]=="0" and instruction[31]=="0" and int(instruction[22:31],2)==266:
        rt = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        rb = int(instruction[16:21],2)
        Registers[rt] = Registers[ra] + Registers[rb]

    # Checking if the instruction is an "addi" instruction
    if int(instruction[0:6],2)==14:
        rt = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        si = int2(instruction[16:32])
        Registers[rt] = Registers[ra] + si

    # Checking if the instruction is an "and" instruction
    if int(instruction[0:6],2)==31 and instruction[31]=="0" and int(instruction[21:31],2)==28:
        rs = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        rb = int(instruction[16:21],2)
        Registers[ra] = Registers[rs] & Registers[rb]
    
    # Checking if the instruction is an "andi" instruction
    if int(instruction[0:6],2)==28:
        rs = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        ui = int2(instruction[16:32])
        Registers[ra] = Registers[rs] & ui
    
    # Checking if the instruction is an "or" instruction
    if int(instruction[0:6],2)==31 and instruction[31]=="0" and int(instruction[21:31],2)==444:
        rs = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        rb = int(instruction[16:21],2)
        Registers[ra] = Registers[rs] or Registers[rb]

    # Checking if the instruction is an "ori" instruction
    if int(instruction[0:6],2)==24:
        rs = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        ui = int(instruction[16:32])
        Registers[ra] = Registers[rs] | ui
    
    # Checking if the instruction is a subf instruction
    if int(instruction[0:6],2)==31 and instruction[21]=="0" and instruction[31]=="0" and int(instruction[22:31],2)==40:
        rt = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        rb = int(instruction[16:21],2)
        Registers[rt] = Registers[rb] - Registers[ra]

    # Checking if the instruction is an "xor" instruction
    if int(instruction[0:6],2)==31 and instruction[31]=="0" and int(instruction[21:31],2)==316:
        rs = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        rb = int(instruction[16:21],2)
        Registers[ra] = Registers[rs] ^ Registers[rb]
    
    # Checking if the instruction is an "xori" instruction
    if int(instruction[0:6],2)==26:
        rs = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        ui = int(instruction[16:32],2)
        Registers[ra] = Registers[rs] ^ ui

    ################## BASIC ALU INSTRUCTIONS ##########################
    
    # data transfer instructions
    # load address
    if int(instruction[0:6],2)==23:
        rt = int(instruction[6:11],2)
        a = int(instruction[11:31],2)
        Registers[rt] = data_base+a
    
    # load word
    if int(instruction[0:6],2)==32: 
        rt = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        d = int2(instruction[16:32])
        Registers[rt] = Static_memory[hex(Registers[ra]+d)]
        
    # store word
    if int(instruction[0:6],2)==36:
        rt = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        d = int2(instruction[16:32])            
        Static_memory[hex(Registers[ra]+d)] = Registers[rt]
    
    # load byte
    if int(instruction[0:6],2)==34: 
        rt = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        d = int2(instruction[16:32])
        Registers[rt] = Static_memory[hex(Registers[ra])][d]

    # store byte
    if int(instruction[0:6],2)==38:
        rt = int(instruction[6:11],2)
        ra = int(instruction[11:16],2)
        d = int2(instruction[16:32])            
        Static_memory[hex(Registers[ra])][d] = Registers[rt]
    
    # Control instruction######################################3
    # Checking if the instruction is an "cmp" instruction
    if int(instruction[0:6],2)==31 and instruction[31]=="0" and int(instruction[21:31],2)==0 and int(instruction[6:9],2)==7 and int(instruction[9:11],2)==1:
        ra = int(instruction[11:16],2)
        rb = int(instruction[16:21],2)
        if Registers[ra]<Registers[rb]:
            CR = 8
        elif Registers[ra]>Registers[rb]:
            CR = 4
        else:
            CR = 2
        print(CR)
        
    
    # bc instruction
    if int(instruction[0:6],2)==19 and instruction[30:]=="00":
        bi = int(instruction[11:16],2)
        bd = int2(instruction[16:30]+"00")
        bd = int(bd/4)
        if bi==28:
            if CR==4:
                NIA = CIA + bd
        elif bi==29:
            if CR==8:
                NIA = CIA + bd
        elif bi==30:
            if CR==2:
                NIA = CIA + bd
    
    #system call
    if int(instruction[:31],2)==0:
        if Registers[0]==1:
            print(Static_memory[hex(Registers[3])])
        
    CIA = NIA
    NIA = NIA + 4
    print(hex(NIA))
    print("REGISTER CONTENTS:")
    print(Registers)
    print("STATIC MEMORY CONTENTS:")
    print(Static_memory)
    print("\n\n")

    
    

