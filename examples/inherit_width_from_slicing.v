/* Generated by Yosys 0.9+3833 (git sha1 b0004911, clang 7.0.1-8+rpi3+deb10u2 -fPIC -Os) */

(* \nmigen.hierarchy  = "inherit_width_from_slicing" *)
(* top =  1  *)
(* generator = "nMigen" *)
module inherit_width_from_slicing(clk, rst, led);
  reg \initial  = 0;
  (* src = "fakename:5" *)
  wire [24:0] \$1 ;
  (* src = "fakename:5" *)
  wire [24:0] \$2 ;
  (* src = "/home/pi/repos/nmigen/nmigen/hdl/ir.py:526" *)
  input clk;
  (* src = "fakename:3" *)
  reg [23:0] cnt = 24'h000000;
  (* src = "fakename:3" *)
  reg [23:0] \cnt$next ;
  (* src = "fakename:1" *)
  output led;
  (* src = "/home/pi/repos/nmigen/nmigen/hdl/ir.py:526" *)
  input rst;
  assign \$2  = cnt + (* src = "fakename:5" *) 1'h1;
  always @(posedge clk)
    cnt <= \cnt$next ;
  always @* begin
    if (\initial ) begin end
    \cnt$next  = \$1 [23:0];
    (* src = "/home/pi/repos/nmigen/nmigen/hdl/xfrm.py:519" *)
    casez (rst)
      1'h1:
          \cnt$next  = 24'h000000;
    endcase
  end
  assign \$1  = \$2 ;
  assign led = cnt[23];
endmodule
