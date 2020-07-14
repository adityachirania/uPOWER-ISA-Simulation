/* MIPS Core Module is the centre of all operations that handles all the operations and instantiates
   all the necessary modules
*/
`include "A_control_module.v"
`include "A_readreg_module.v"
`include "A_alu_module.v"
`include "A_readins_module.v"
`include "A_readmem_module.v"
`include "A_insparse_module.v"


module mips_core(clock);

    input clock;   // Execution happens only at positive level-transition (edge sensitive)
	
    // Program counter
    reg[31:0] PC = 32'b0;
    reg [31:0] n;
	
    // Instruction
    wire [31:0] instruction;
	
    // Parse instruction
    wire [5:0] funct;
    wire [4:0] rs, rt, rd, shamt;
    wire [25:0] address;
    wire [15:0] immediate;
    wire [5:0] opcode;
	
    // Signals
    wire RegRead, RegWrite, RegDst;  
    wire MemRead, MemWrite;
    wire branch_signal,bs;
	
    // Registers contents
    wire [31:0] write_data, rs_content, rt_content, memory_read_data;
	
	
    // Instantiating all necessary modules
    read_instructions inst_mem (instruction, PC);
	
    ins_parse parse (opcode, rs, rt, rd, shamt, funct, immediate, address, instruction, PC);
	
    control_unit signals (RegRead, RegWrite,MemRead, MemWrite, RegDst, 
                                branch_signal, opcode, funct);
								 
    ALU32bit alu_process (write_data, bs, opcode, rs_content, rt_content, shamt, funct, immediate);
	
    read_data_memory dataMemory (memory_read_data, write_data, rt_content, opcode, MemRead, MemWrite);
	
    read_registers contents (rs_content, rt_content,memory_read_data, write_data, rs, rt, rd, opcode, 
                                    RegRead, RegWrite, RegDst, clock);
	
    // PC operations - The next instruction is read only when the clock is at positive edge
    always @(posedge clock) begin 
        // JUMP 
        n = $signed(immediate);
        // $monitor("PCB : %d",PC);
        if(opcode == 6'h2) begin
            PC = address;
        end
        // JUMP REGISTER
        else if(opcode == 6'h0 & funct == 6'h08)begin
            PC = rs_content;
        end
        // BRANCH
        else if(write_data == 0 & branch_signal == 1 & bs == 1) begin
            PC = PC + 1 + n;
        end
        else begin
            PC = PC+1;
        end
    end 
endmodule