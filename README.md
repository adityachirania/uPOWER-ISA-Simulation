# uPOWER-ISA-Simulation
An Simulator that parses assembly level code of uPOWER instruction set, converts to object code and then simulates its execution

# Instructions that have been implemented in the assembler
All the instructions mentioned in the pdf have been implemented in the assembler. The assembler is a 2 pass assembler that maps all labels to their addresses in memory the first pass. In the second pass the instructions are converted to binary code.The memory contents and binary codes are passed to the simulator and the simulator executes them one by one. 

# To sample codes that this simulator simulates 
 something.s - Sums up the elements of an array
 hello.s - Prints hello world with the help of a system call
 
 
 # Running instructions 
 1.Clone the repository 
 2.Open assembly.py and change the filename variable on line 28 to the filename that you have created and want to simualte.
 3.Run "python3 Simulator.py" in the command line.
 
 
