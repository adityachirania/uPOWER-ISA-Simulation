# uPOWER-ISA-Simulation
A Simulator that parses assembly level code of uPOWER instruction set, converts to object code and then simulates its execution 
Also present is behavioural implementation of the microprocessor in verilog.

# Instructions that have been implemented in the assembler
All the instructions mentioned in the pdf have been implemented in the assembler. The assembler is a 2 pass assembler that maps all labels to their addresses in memory the first pass. In the second pass the instructions are converted to binary code.The memory contents and binary codes are passed to the simulator and the simulator executes them one by one. 

# To sample codes that this simulator simulates 
- something.s - Sums up the elements of an array
- hello.s - Prints hello world with the help of a system call
 
# Video Demos of the simulations are also availible on : 
- https://youtu.be/MCr6ZGgKVrc (Demo of the python based simulator) 
- https://youtu.be/3gv1E0ndNEQ (Hardware based simulator in verilog) 
 
 # Running instructions 
 1.Clone the repository <br/>
 2.Open assembly.py and change the filename variable on line 28 to the filename that you have created and want to simualte.<br/>
 3.Run "python3 Simulator.py" in the command line.
 4.The binary code of each equivalent intstruction shall be written in a file called something.txt.
 
