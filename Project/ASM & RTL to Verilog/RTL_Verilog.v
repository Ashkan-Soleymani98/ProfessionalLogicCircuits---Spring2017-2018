module RTL_Verilog(input wire [31:0]in1, input wire [31:0]in2, input wire S, input wire clock, output reg V, output reg [31:0]data_out);
reg out;
reg [31:0]R1;
reg [31:0]R2;
reg [31:0]R3;
reg F1=0, F2=0;
always@(posedge clock)
begin
	if ((!F1) && S)
	begin
		R1 <= in1;
		R2 <= in2;
		R3 <= 0;
		V <= 0;
		F1 <= 1;
		F2 <= 0;
	end
	if ((!F2) && F1 && (R1 > R2))
	begin
		R1 <= R2;
		R2 <= R1;
	end
	if (!F2)
	begin
		F2 <= 1;
	end
	if (F2 && F1 && (R1 > 0))
	begin
		R3 <= R2 + R3;
		R1 <= R1-1;
	end
	if (R1 == 0)
	begin
		 F1 <= 0;
		 data_out <= R3;
		 V <= 1 ;
	end
end
endmodule
