/* Test Module designed to read the instructions from a .mem file containing the 32-bit MIPS instructions
in binary
*/
module read_instructions(
output reg [31:0] instruction,
input [31:0] program_counter
);  //set according to use
reg [31:0] instructions [55:0];
initial
  begin
    $readmemb("instruction.mem",instructions);
  end

always @(program_counter)
  begin
    instruction = instructions[program_counter];
  end

endmodule