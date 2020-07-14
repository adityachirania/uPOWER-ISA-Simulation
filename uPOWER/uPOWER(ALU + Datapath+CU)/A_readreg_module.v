module read_registers(
    output reg [63:0] ReadData1, ReadData2,
    input [4:0] rs,rt,rd,
    input [5:0] opcode, // RS, RA => Source registers ; RT => Destintion register
    input [63:0] memory_read_data,WriteData,  // Data to be written to the register
    input  RegRead, RegWrite , clk// RegWrite and RegRead are input signals to indicate whether the operation is reading/writing       
);
reg [63:0] registers [31:0]; // The set of 32 registers (32-bit)

initial
 begin
   $readmemb("registers.mem",registers);
 end

always @(posedge clk)
  begin
    if(RegWrite)
      begin  
      if(opcode == 6'd34)
       begin
           registers[rd] = {{56{1'b0}}, WriteData[7:0]};
       end
      if(opcode == 6'd40)
       begin
           registers[rd] = {{48{1'b0}}, WriteData[15:0]};
       end
      if (opcode == 6'd42)
       begin
           registers[rd] = {{48{WriteData[31]}}, WriteData[31:0]};
       end
      if (opcode == 6'd32)
       begin
           registers[rd] = memory_read_data;
       end
      if (opcode == 6'd14 | opcode == 6'd31)
       begin
           registers[rd] = WriteData;
       end
      $writememb("registers.mem",registers);
    end
 end

always @(rs,rt,rd)
 begin
     if(RegRead)
      begin
          ReadData1 = registers[rs];
          ReadData2 = registers[rt];
      end
 end

endmodule