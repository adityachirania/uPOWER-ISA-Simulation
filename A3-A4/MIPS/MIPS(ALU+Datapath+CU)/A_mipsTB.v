// MIPS test bench - To drive and simulate the entire MIPS ALU 
`include "A_mipsCORE.v"
module mips_testbench ();

    reg clock;
    wire result;
	
    mips_core test(clock);

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
        #100 clock=~clock; #100 clock=~clock;
    end
endmodule
