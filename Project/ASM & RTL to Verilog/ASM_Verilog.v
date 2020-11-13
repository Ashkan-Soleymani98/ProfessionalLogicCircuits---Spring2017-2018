module ASM_Verilog(input wire [31:0]in1, input wire [31:0]in2, input wire S, input wire clock, output reg V, output reg [31:0]data_out);
reg out;
reg [31:0]R1;
reg [31:0]R2;
reg [31:0]R3;
reg [31:0]R4;
integer blockNum = 1, nextBlock;
always@(posedge clock)
begin
	if(blockNum == 1)
	begin
		V<=0;
		if (S==1)
		begin
			R1[31:0]<=in1[31:0];
			R2[31:0]<=in2[31:0];
			R3[31:0]<=32'b0;
			V<=0;
		end
		if(!(S==1))
			blockNum <= 1;
		else if(S==1)
			blockNum <= 2;
	end
	else if(blockNum == 2)
	begin
		if (R1[31:0]>R2[31:0])
		begin
			R1[31:0]<=R2[31:0];
			R2[31:0]<=R1[31:0];
		end
		if(!(R1[31:0]>R2[31:0]))
			blockNum <= 3;
		else if(R1[31:0]>R2[31:0])
			blockNum <= 3;
	end
	else if(blockNum == 3)
	begin
		if (R1[31:0] > 0)
		begin
			R3[31:0]<=R3[31:0]+R2[31:0];
			R1[31:0]<=R1[31:0]-1;
		end
		if ((!(R1[31:0] > 0)) && (V==0))
		begin
			data_out[31:0]<=R3[31:0];
			R4[31:0]<=R3[31:0];
			V<=1;
		end
		if(R1[31:0] > 0)
			blockNum <= 3;
		else if((!(V==0)) && (!(R1[31:0] > 0)))
			blockNum <= 1;
		else if((!(R1[31:0] > 0)) && (V==0))
			blockNum <= 1;
	end
end
endmodule
