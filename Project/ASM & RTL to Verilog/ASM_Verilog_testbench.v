module ASM_testbench();
     reg [31:0]in1;
     reg [31:0]in2;
     wire [31:0]res;
     reg CLK;
     wire V;
     reg S;
     ASM_Verilog test(in1, in2, S, CLK, V, res);
     initial begin
          CLK <= 0;
          in1 <= 17;
          in2 <= 19;
          S <= 0;
          #100 S <= 1;
          #140 S <= 0;
     end
     always begin
          #20 CLK = ~CLK;
     end
endmodule
