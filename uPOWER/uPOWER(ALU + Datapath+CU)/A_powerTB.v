// MIPS test bench - To drive and simulate the entire MIPS ALU 
`include "A_powerCORE.v"
module power_testbench();

reg clock;
wire result;

mips_core Datapath(clock);
initial clock = 0;

initial 
 begin
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
#100 clock=~clock; #100 clock=~clock;
 end

endmodule