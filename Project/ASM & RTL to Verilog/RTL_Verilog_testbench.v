module RTL_Verilog_testbench();
     reg [31:0]in1;
     reg [31:0]in2;
     reg S;
     wire [31:0]res;
     reg CLK;
     wire V;
     RTL_Verilog test(in1, in2, S, CLK, V, res);
     initial begin
          CLK <= 0;
          in1 <= 24;
          in2 <= 13;
          S <= 0;
          #100 S <= 1;
          #140 S <= 0;
     end
     always begin
          #20 CLK = ~CLK;
     end
endmodule
