/* Generated by Yosys 0.9+3833 (git sha1 b0004911, clang 7.0.1-8+rpi3+deb10u2 -fPIC -Os) */

(* \nmigen.hierarchy  = "ram" *)
(* top =  1  *)
(* generator = "nMigen" *)
module ram(wr_addr, wr_data, rd_addr, rd_data, clk, rst, wr_en);
  (* src = "/home/pi/repos/nmigen/nmigen/hdl/ir.py:526" *)
  input clk;
  (* src = "fakename:2" *)
  wire [9:0] mem_r_addr;
  (* src = "fakename:2" *)
  wire [7:0] mem_r_data;
  (* src = "fakename:3" *)
  wire [9:0] mem_w_addr;
  (* src = "fakename:3" *)
  wire [7:0] mem_w_data;
  (* src = "fakename:3" *)
  wire mem_w_en;
  (* src = "fakename:6" *)
  input [9:0] rd_addr;
  (* src = "fakename:7" *)
  output [7:0] rd_data;
  (* src = "/home/pi/repos/nmigen/nmigen/hdl/ir.py:526" *)
  input rst;
  (* src = "fakename:4" *)
  input [9:0] wr_addr;
  (* src = "fakename:5" *)
  input [7:0] wr_data;
  (* src = "fakename:1" *)
  input wr_en;
  reg [7:0] mem [1023:0];
  initial begin
    mem[0] = 8'h00;
    mem[1] = 8'h00;
    mem[2] = 8'h00;
    mem[3] = 8'h00;
    mem[4] = 8'h00;
    mem[5] = 8'h00;
    mem[6] = 8'h00;
    mem[7] = 8'h00;
    mem[8] = 8'h00;
    mem[9] = 8'h00;
    mem[10] = 8'h00;
    mem[11] = 8'h00;
    mem[12] = 8'h00;
    mem[13] = 8'h00;
    mem[14] = 8'h00;
    mem[15] = 8'h00;
    mem[16] = 8'h00;
    mem[17] = 8'h00;
    mem[18] = 8'h00;
    mem[19] = 8'h00;
    mem[20] = 8'h00;
    mem[21] = 8'h00;
    mem[22] = 8'h00;
    mem[23] = 8'h00;
    mem[24] = 8'h00;
    mem[25] = 8'h00;
    mem[26] = 8'h00;
    mem[27] = 8'h00;
    mem[28] = 8'h00;
    mem[29] = 8'h00;
    mem[30] = 8'h00;
    mem[31] = 8'h00;
    mem[32] = 8'h00;
    mem[33] = 8'h00;
    mem[34] = 8'h00;
    mem[35] = 8'h00;
    mem[36] = 8'h00;
    mem[37] = 8'h00;
    mem[38] = 8'h00;
    mem[39] = 8'h00;
    mem[40] = 8'h00;
    mem[41] = 8'h00;
    mem[42] = 8'h00;
    mem[43] = 8'h00;
    mem[44] = 8'h00;
    mem[45] = 8'h00;
    mem[46] = 8'h00;
    mem[47] = 8'h00;
    mem[48] = 8'h00;
    mem[49] = 8'h00;
    mem[50] = 8'h00;
    mem[51] = 8'h00;
    mem[52] = 8'h00;
    mem[53] = 8'h00;
    mem[54] = 8'h00;
    mem[55] = 8'h00;
    mem[56] = 8'h00;
    mem[57] = 8'h00;
    mem[58] = 8'h00;
    mem[59] = 8'h00;
    mem[60] = 8'h00;
    mem[61] = 8'h00;
    mem[62] = 8'h00;
    mem[63] = 8'h00;
    mem[64] = 8'h00;
    mem[65] = 8'h00;
    mem[66] = 8'h00;
    mem[67] = 8'h00;
    mem[68] = 8'h00;
    mem[69] = 8'h00;
    mem[70] = 8'h00;
    mem[71] = 8'h00;
    mem[72] = 8'h00;
    mem[73] = 8'h00;
    mem[74] = 8'h00;
    mem[75] = 8'h00;
    mem[76] = 8'h00;
    mem[77] = 8'h00;
    mem[78] = 8'h00;
    mem[79] = 8'h00;
    mem[80] = 8'h00;
    mem[81] = 8'h00;
    mem[82] = 8'h00;
    mem[83] = 8'h00;
    mem[84] = 8'h00;
    mem[85] = 8'h00;
    mem[86] = 8'h00;
    mem[87] = 8'h00;
    mem[88] = 8'h00;
    mem[89] = 8'h00;
    mem[90] = 8'h00;
    mem[91] = 8'h00;
    mem[92] = 8'h00;
    mem[93] = 8'h00;
    mem[94] = 8'h00;
    mem[95] = 8'h00;
    mem[96] = 8'h00;
    mem[97] = 8'h00;
    mem[98] = 8'h00;
    mem[99] = 8'h00;
    mem[100] = 8'h00;
    mem[101] = 8'h00;
    mem[102] = 8'h00;
    mem[103] = 8'h00;
    mem[104] = 8'h00;
    mem[105] = 8'h00;
    mem[106] = 8'h00;
    mem[107] = 8'h00;
    mem[108] = 8'h00;
    mem[109] = 8'h00;
    mem[110] = 8'h00;
    mem[111] = 8'h00;
    mem[112] = 8'h00;
    mem[113] = 8'h00;
    mem[114] = 8'h00;
    mem[115] = 8'h00;
    mem[116] = 8'h00;
    mem[117] = 8'h00;
    mem[118] = 8'h00;
    mem[119] = 8'h00;
    mem[120] = 8'h00;
    mem[121] = 8'h00;
    mem[122] = 8'h00;
    mem[123] = 8'h00;
    mem[124] = 8'h00;
    mem[125] = 8'h00;
    mem[126] = 8'h00;
    mem[127] = 8'h00;
    mem[128] = 8'h00;
    mem[129] = 8'h00;
    mem[130] = 8'h00;
    mem[131] = 8'h00;
    mem[132] = 8'h00;
    mem[133] = 8'h00;
    mem[134] = 8'h00;
    mem[135] = 8'h00;
    mem[136] = 8'h00;
    mem[137] = 8'h00;
    mem[138] = 8'h00;
    mem[139] = 8'h00;
    mem[140] = 8'h00;
    mem[141] = 8'h00;
    mem[142] = 8'h00;
    mem[143] = 8'h00;
    mem[144] = 8'h00;
    mem[145] = 8'h00;
    mem[146] = 8'h00;
    mem[147] = 8'h00;
    mem[148] = 8'h00;
    mem[149] = 8'h00;
    mem[150] = 8'h00;
    mem[151] = 8'h00;
    mem[152] = 8'h00;
    mem[153] = 8'h00;
    mem[154] = 8'h00;
    mem[155] = 8'h00;
    mem[156] = 8'h00;
    mem[157] = 8'h00;
    mem[158] = 8'h00;
    mem[159] = 8'h00;
    mem[160] = 8'h00;
    mem[161] = 8'h00;
    mem[162] = 8'h00;
    mem[163] = 8'h00;
    mem[164] = 8'h00;
    mem[165] = 8'h00;
    mem[166] = 8'h00;
    mem[167] = 8'h00;
    mem[168] = 8'h00;
    mem[169] = 8'h00;
    mem[170] = 8'h00;
    mem[171] = 8'h00;
    mem[172] = 8'h00;
    mem[173] = 8'h00;
    mem[174] = 8'h00;
    mem[175] = 8'h00;
    mem[176] = 8'h00;
    mem[177] = 8'h00;
    mem[178] = 8'h00;
    mem[179] = 8'h00;
    mem[180] = 8'h00;
    mem[181] = 8'h00;
    mem[182] = 8'h00;
    mem[183] = 8'h00;
    mem[184] = 8'h00;
    mem[185] = 8'h00;
    mem[186] = 8'h00;
    mem[187] = 8'h00;
    mem[188] = 8'h00;
    mem[189] = 8'h00;
    mem[190] = 8'h00;
    mem[191] = 8'h00;
    mem[192] = 8'h00;
    mem[193] = 8'h00;
    mem[194] = 8'h00;
    mem[195] = 8'h00;
    mem[196] = 8'h00;
    mem[197] = 8'h00;
    mem[198] = 8'h00;
    mem[199] = 8'h00;
    mem[200] = 8'h00;
    mem[201] = 8'h00;
    mem[202] = 8'h00;
    mem[203] = 8'h00;
    mem[204] = 8'h00;
    mem[205] = 8'h00;
    mem[206] = 8'h00;
    mem[207] = 8'h00;
    mem[208] = 8'h00;
    mem[209] = 8'h00;
    mem[210] = 8'h00;
    mem[211] = 8'h00;
    mem[212] = 8'h00;
    mem[213] = 8'h00;
    mem[214] = 8'h00;
    mem[215] = 8'h00;
    mem[216] = 8'h00;
    mem[217] = 8'h00;
    mem[218] = 8'h00;
    mem[219] = 8'h00;
    mem[220] = 8'h00;
    mem[221] = 8'h00;
    mem[222] = 8'h00;
    mem[223] = 8'h00;
    mem[224] = 8'h00;
    mem[225] = 8'h00;
    mem[226] = 8'h00;
    mem[227] = 8'h00;
    mem[228] = 8'h00;
    mem[229] = 8'h00;
    mem[230] = 8'h00;
    mem[231] = 8'h00;
    mem[232] = 8'h00;
    mem[233] = 8'h00;
    mem[234] = 8'h00;
    mem[235] = 8'h00;
    mem[236] = 8'h00;
    mem[237] = 8'h00;
    mem[238] = 8'h00;
    mem[239] = 8'h00;
    mem[240] = 8'h00;
    mem[241] = 8'h00;
    mem[242] = 8'h00;
    mem[243] = 8'h00;
    mem[244] = 8'h00;
    mem[245] = 8'h00;
    mem[246] = 8'h00;
    mem[247] = 8'h00;
    mem[248] = 8'h00;
    mem[249] = 8'h00;
    mem[250] = 8'h00;
    mem[251] = 8'h00;
    mem[252] = 8'h00;
    mem[253] = 8'h00;
    mem[254] = 8'h00;
    mem[255] = 8'h00;
    mem[256] = 8'h00;
    mem[257] = 8'h00;
    mem[258] = 8'h00;
    mem[259] = 8'h00;
    mem[260] = 8'h00;
    mem[261] = 8'h00;
    mem[262] = 8'h00;
    mem[263] = 8'h00;
    mem[264] = 8'h00;
    mem[265] = 8'h00;
    mem[266] = 8'h00;
    mem[267] = 8'h00;
    mem[268] = 8'h00;
    mem[269] = 8'h00;
    mem[270] = 8'h00;
    mem[271] = 8'h00;
    mem[272] = 8'h00;
    mem[273] = 8'h00;
    mem[274] = 8'h00;
    mem[275] = 8'h00;
    mem[276] = 8'h00;
    mem[277] = 8'h00;
    mem[278] = 8'h00;
    mem[279] = 8'h00;
    mem[280] = 8'h00;
    mem[281] = 8'h00;
    mem[282] = 8'h00;
    mem[283] = 8'h00;
    mem[284] = 8'h00;
    mem[285] = 8'h00;
    mem[286] = 8'h00;
    mem[287] = 8'h00;
    mem[288] = 8'h00;
    mem[289] = 8'h00;
    mem[290] = 8'h00;
    mem[291] = 8'h00;
    mem[292] = 8'h00;
    mem[293] = 8'h00;
    mem[294] = 8'h00;
    mem[295] = 8'h00;
    mem[296] = 8'h00;
    mem[297] = 8'h00;
    mem[298] = 8'h00;
    mem[299] = 8'h00;
    mem[300] = 8'h00;
    mem[301] = 8'h00;
    mem[302] = 8'h00;
    mem[303] = 8'h00;
    mem[304] = 8'h00;
    mem[305] = 8'h00;
    mem[306] = 8'h00;
    mem[307] = 8'h00;
    mem[308] = 8'h00;
    mem[309] = 8'h00;
    mem[310] = 8'h00;
    mem[311] = 8'h00;
    mem[312] = 8'h00;
    mem[313] = 8'h00;
    mem[314] = 8'h00;
    mem[315] = 8'h00;
    mem[316] = 8'h00;
    mem[317] = 8'h00;
    mem[318] = 8'h00;
    mem[319] = 8'h00;
    mem[320] = 8'h00;
    mem[321] = 8'h00;
    mem[322] = 8'h00;
    mem[323] = 8'h00;
    mem[324] = 8'h00;
    mem[325] = 8'h00;
    mem[326] = 8'h00;
    mem[327] = 8'h00;
    mem[328] = 8'h00;
    mem[329] = 8'h00;
    mem[330] = 8'h00;
    mem[331] = 8'h00;
    mem[332] = 8'h00;
    mem[333] = 8'h00;
    mem[334] = 8'h00;
    mem[335] = 8'h00;
    mem[336] = 8'h00;
    mem[337] = 8'h00;
    mem[338] = 8'h00;
    mem[339] = 8'h00;
    mem[340] = 8'h00;
    mem[341] = 8'h00;
    mem[342] = 8'h00;
    mem[343] = 8'h00;
    mem[344] = 8'h00;
    mem[345] = 8'h00;
    mem[346] = 8'h00;
    mem[347] = 8'h00;
    mem[348] = 8'h00;
    mem[349] = 8'h00;
    mem[350] = 8'h00;
    mem[351] = 8'h00;
    mem[352] = 8'h00;
    mem[353] = 8'h00;
    mem[354] = 8'h00;
    mem[355] = 8'h00;
    mem[356] = 8'h00;
    mem[357] = 8'h00;
    mem[358] = 8'h00;
    mem[359] = 8'h00;
    mem[360] = 8'h00;
    mem[361] = 8'h00;
    mem[362] = 8'h00;
    mem[363] = 8'h00;
    mem[364] = 8'h00;
    mem[365] = 8'h00;
    mem[366] = 8'h00;
    mem[367] = 8'h00;
    mem[368] = 8'h00;
    mem[369] = 8'h00;
    mem[370] = 8'h00;
    mem[371] = 8'h00;
    mem[372] = 8'h00;
    mem[373] = 8'h00;
    mem[374] = 8'h00;
    mem[375] = 8'h00;
    mem[376] = 8'h00;
    mem[377] = 8'h00;
    mem[378] = 8'h00;
    mem[379] = 8'h00;
    mem[380] = 8'h00;
    mem[381] = 8'h00;
    mem[382] = 8'h00;
    mem[383] = 8'h00;
    mem[384] = 8'h00;
    mem[385] = 8'h00;
    mem[386] = 8'h00;
    mem[387] = 8'h00;
    mem[388] = 8'h00;
    mem[389] = 8'h00;
    mem[390] = 8'h00;
    mem[391] = 8'h00;
    mem[392] = 8'h00;
    mem[393] = 8'h00;
    mem[394] = 8'h00;
    mem[395] = 8'h00;
    mem[396] = 8'h00;
    mem[397] = 8'h00;
    mem[398] = 8'h00;
    mem[399] = 8'h00;
    mem[400] = 8'h00;
    mem[401] = 8'h00;
    mem[402] = 8'h00;
    mem[403] = 8'h00;
    mem[404] = 8'h00;
    mem[405] = 8'h00;
    mem[406] = 8'h00;
    mem[407] = 8'h00;
    mem[408] = 8'h00;
    mem[409] = 8'h00;
    mem[410] = 8'h00;
    mem[411] = 8'h00;
    mem[412] = 8'h00;
    mem[413] = 8'h00;
    mem[414] = 8'h00;
    mem[415] = 8'h00;
    mem[416] = 8'h00;
    mem[417] = 8'h00;
    mem[418] = 8'h00;
    mem[419] = 8'h00;
    mem[420] = 8'h00;
    mem[421] = 8'h00;
    mem[422] = 8'h00;
    mem[423] = 8'h00;
    mem[424] = 8'h00;
    mem[425] = 8'h00;
    mem[426] = 8'h00;
    mem[427] = 8'h00;
    mem[428] = 8'h00;
    mem[429] = 8'h00;
    mem[430] = 8'h00;
    mem[431] = 8'h00;
    mem[432] = 8'h00;
    mem[433] = 8'h00;
    mem[434] = 8'h00;
    mem[435] = 8'h00;
    mem[436] = 8'h00;
    mem[437] = 8'h00;
    mem[438] = 8'h00;
    mem[439] = 8'h00;
    mem[440] = 8'h00;
    mem[441] = 8'h00;
    mem[442] = 8'h00;
    mem[443] = 8'h00;
    mem[444] = 8'h00;
    mem[445] = 8'h00;
    mem[446] = 8'h00;
    mem[447] = 8'h00;
    mem[448] = 8'h00;
    mem[449] = 8'h00;
    mem[450] = 8'h00;
    mem[451] = 8'h00;
    mem[452] = 8'h00;
    mem[453] = 8'h00;
    mem[454] = 8'h00;
    mem[455] = 8'h00;
    mem[456] = 8'h00;
    mem[457] = 8'h00;
    mem[458] = 8'h00;
    mem[459] = 8'h00;
    mem[460] = 8'h00;
    mem[461] = 8'h00;
    mem[462] = 8'h00;
    mem[463] = 8'h00;
    mem[464] = 8'h00;
    mem[465] = 8'h00;
    mem[466] = 8'h00;
    mem[467] = 8'h00;
    mem[468] = 8'h00;
    mem[469] = 8'h00;
    mem[470] = 8'h00;
    mem[471] = 8'h00;
    mem[472] = 8'h00;
    mem[473] = 8'h00;
    mem[474] = 8'h00;
    mem[475] = 8'h00;
    mem[476] = 8'h00;
    mem[477] = 8'h00;
    mem[478] = 8'h00;
    mem[479] = 8'h00;
    mem[480] = 8'h00;
    mem[481] = 8'h00;
    mem[482] = 8'h00;
    mem[483] = 8'h00;
    mem[484] = 8'h00;
    mem[485] = 8'h00;
    mem[486] = 8'h00;
    mem[487] = 8'h00;
    mem[488] = 8'h00;
    mem[489] = 8'h00;
    mem[490] = 8'h00;
    mem[491] = 8'h00;
    mem[492] = 8'h00;
    mem[493] = 8'h00;
    mem[494] = 8'h00;
    mem[495] = 8'h00;
    mem[496] = 8'h00;
    mem[497] = 8'h00;
    mem[498] = 8'h00;
    mem[499] = 8'h00;
    mem[500] = 8'h00;
    mem[501] = 8'h00;
    mem[502] = 8'h00;
    mem[503] = 8'h00;
    mem[504] = 8'h00;
    mem[505] = 8'h00;
    mem[506] = 8'h00;
    mem[507] = 8'h00;
    mem[508] = 8'h00;
    mem[509] = 8'h00;
    mem[510] = 8'h00;
    mem[511] = 8'h00;
    mem[512] = 8'h00;
    mem[513] = 8'h00;
    mem[514] = 8'h00;
    mem[515] = 8'h00;
    mem[516] = 8'h00;
    mem[517] = 8'h00;
    mem[518] = 8'h00;
    mem[519] = 8'h00;
    mem[520] = 8'h00;
    mem[521] = 8'h00;
    mem[522] = 8'h00;
    mem[523] = 8'h00;
    mem[524] = 8'h00;
    mem[525] = 8'h00;
    mem[526] = 8'h00;
    mem[527] = 8'h00;
    mem[528] = 8'h00;
    mem[529] = 8'h00;
    mem[530] = 8'h00;
    mem[531] = 8'h00;
    mem[532] = 8'h00;
    mem[533] = 8'h00;
    mem[534] = 8'h00;
    mem[535] = 8'h00;
    mem[536] = 8'h00;
    mem[537] = 8'h00;
    mem[538] = 8'h00;
    mem[539] = 8'h00;
    mem[540] = 8'h00;
    mem[541] = 8'h00;
    mem[542] = 8'h00;
    mem[543] = 8'h00;
    mem[544] = 8'h00;
    mem[545] = 8'h00;
    mem[546] = 8'h00;
    mem[547] = 8'h00;
    mem[548] = 8'h00;
    mem[549] = 8'h00;
    mem[550] = 8'h00;
    mem[551] = 8'h00;
    mem[552] = 8'h00;
    mem[553] = 8'h00;
    mem[554] = 8'h00;
    mem[555] = 8'h00;
    mem[556] = 8'h00;
    mem[557] = 8'h00;
    mem[558] = 8'h00;
    mem[559] = 8'h00;
    mem[560] = 8'h00;
    mem[561] = 8'h00;
    mem[562] = 8'h00;
    mem[563] = 8'h00;
    mem[564] = 8'h00;
    mem[565] = 8'h00;
    mem[566] = 8'h00;
    mem[567] = 8'h00;
    mem[568] = 8'h00;
    mem[569] = 8'h00;
    mem[570] = 8'h00;
    mem[571] = 8'h00;
    mem[572] = 8'h00;
    mem[573] = 8'h00;
    mem[574] = 8'h00;
    mem[575] = 8'h00;
    mem[576] = 8'h00;
    mem[577] = 8'h00;
    mem[578] = 8'h00;
    mem[579] = 8'h00;
    mem[580] = 8'h00;
    mem[581] = 8'h00;
    mem[582] = 8'h00;
    mem[583] = 8'h00;
    mem[584] = 8'h00;
    mem[585] = 8'h00;
    mem[586] = 8'h00;
    mem[587] = 8'h00;
    mem[588] = 8'h00;
    mem[589] = 8'h00;
    mem[590] = 8'h00;
    mem[591] = 8'h00;
    mem[592] = 8'h00;
    mem[593] = 8'h00;
    mem[594] = 8'h00;
    mem[595] = 8'h00;
    mem[596] = 8'h00;
    mem[597] = 8'h00;
    mem[598] = 8'h00;
    mem[599] = 8'h00;
    mem[600] = 8'h00;
    mem[601] = 8'h00;
    mem[602] = 8'h00;
    mem[603] = 8'h00;
    mem[604] = 8'h00;
    mem[605] = 8'h00;
    mem[606] = 8'h00;
    mem[607] = 8'h00;
    mem[608] = 8'h00;
    mem[609] = 8'h00;
    mem[610] = 8'h00;
    mem[611] = 8'h00;
    mem[612] = 8'h00;
    mem[613] = 8'h00;
    mem[614] = 8'h00;
    mem[615] = 8'h00;
    mem[616] = 8'h00;
    mem[617] = 8'h00;
    mem[618] = 8'h00;
    mem[619] = 8'h00;
    mem[620] = 8'h00;
    mem[621] = 8'h00;
    mem[622] = 8'h00;
    mem[623] = 8'h00;
    mem[624] = 8'h00;
    mem[625] = 8'h00;
    mem[626] = 8'h00;
    mem[627] = 8'h00;
    mem[628] = 8'h00;
    mem[629] = 8'h00;
    mem[630] = 8'h00;
    mem[631] = 8'h00;
    mem[632] = 8'h00;
    mem[633] = 8'h00;
    mem[634] = 8'h00;
    mem[635] = 8'h00;
    mem[636] = 8'h00;
    mem[637] = 8'h00;
    mem[638] = 8'h00;
    mem[639] = 8'h00;
    mem[640] = 8'h00;
    mem[641] = 8'h00;
    mem[642] = 8'h00;
    mem[643] = 8'h00;
    mem[644] = 8'h00;
    mem[645] = 8'h00;
    mem[646] = 8'h00;
    mem[647] = 8'h00;
    mem[648] = 8'h00;
    mem[649] = 8'h00;
    mem[650] = 8'h00;
    mem[651] = 8'h00;
    mem[652] = 8'h00;
    mem[653] = 8'h00;
    mem[654] = 8'h00;
    mem[655] = 8'h00;
    mem[656] = 8'h00;
    mem[657] = 8'h00;
    mem[658] = 8'h00;
    mem[659] = 8'h00;
    mem[660] = 8'h00;
    mem[661] = 8'h00;
    mem[662] = 8'h00;
    mem[663] = 8'h00;
    mem[664] = 8'h00;
    mem[665] = 8'h00;
    mem[666] = 8'h00;
    mem[667] = 8'h00;
    mem[668] = 8'h00;
    mem[669] = 8'h00;
    mem[670] = 8'h00;
    mem[671] = 8'h00;
    mem[672] = 8'h00;
    mem[673] = 8'h00;
    mem[674] = 8'h00;
    mem[675] = 8'h00;
    mem[676] = 8'h00;
    mem[677] = 8'h00;
    mem[678] = 8'h00;
    mem[679] = 8'h00;
    mem[680] = 8'h00;
    mem[681] = 8'h00;
    mem[682] = 8'h00;
    mem[683] = 8'h00;
    mem[684] = 8'h00;
    mem[685] = 8'h00;
    mem[686] = 8'h00;
    mem[687] = 8'h00;
    mem[688] = 8'h00;
    mem[689] = 8'h00;
    mem[690] = 8'h00;
    mem[691] = 8'h00;
    mem[692] = 8'h00;
    mem[693] = 8'h00;
    mem[694] = 8'h00;
    mem[695] = 8'h00;
    mem[696] = 8'h00;
    mem[697] = 8'h00;
    mem[698] = 8'h00;
    mem[699] = 8'h00;
    mem[700] = 8'h00;
    mem[701] = 8'h00;
    mem[702] = 8'h00;
    mem[703] = 8'h00;
    mem[704] = 8'h00;
    mem[705] = 8'h00;
    mem[706] = 8'h00;
    mem[707] = 8'h00;
    mem[708] = 8'h00;
    mem[709] = 8'h00;
    mem[710] = 8'h00;
    mem[711] = 8'h00;
    mem[712] = 8'h00;
    mem[713] = 8'h00;
    mem[714] = 8'h00;
    mem[715] = 8'h00;
    mem[716] = 8'h00;
    mem[717] = 8'h00;
    mem[718] = 8'h00;
    mem[719] = 8'h00;
    mem[720] = 8'h00;
    mem[721] = 8'h00;
    mem[722] = 8'h00;
    mem[723] = 8'h00;
    mem[724] = 8'h00;
    mem[725] = 8'h00;
    mem[726] = 8'h00;
    mem[727] = 8'h00;
    mem[728] = 8'h00;
    mem[729] = 8'h00;
    mem[730] = 8'h00;
    mem[731] = 8'h00;
    mem[732] = 8'h00;
    mem[733] = 8'h00;
    mem[734] = 8'h00;
    mem[735] = 8'h00;
    mem[736] = 8'h00;
    mem[737] = 8'h00;
    mem[738] = 8'h00;
    mem[739] = 8'h00;
    mem[740] = 8'h00;
    mem[741] = 8'h00;
    mem[742] = 8'h00;
    mem[743] = 8'h00;
    mem[744] = 8'h00;
    mem[745] = 8'h00;
    mem[746] = 8'h00;
    mem[747] = 8'h00;
    mem[748] = 8'h00;
    mem[749] = 8'h00;
    mem[750] = 8'h00;
    mem[751] = 8'h00;
    mem[752] = 8'h00;
    mem[753] = 8'h00;
    mem[754] = 8'h00;
    mem[755] = 8'h00;
    mem[756] = 8'h00;
    mem[757] = 8'h00;
    mem[758] = 8'h00;
    mem[759] = 8'h00;
    mem[760] = 8'h00;
    mem[761] = 8'h00;
    mem[762] = 8'h00;
    mem[763] = 8'h00;
    mem[764] = 8'h00;
    mem[765] = 8'h00;
    mem[766] = 8'h00;
    mem[767] = 8'h00;
    mem[768] = 8'h00;
    mem[769] = 8'h00;
    mem[770] = 8'h00;
    mem[771] = 8'h00;
    mem[772] = 8'h00;
    mem[773] = 8'h00;
    mem[774] = 8'h00;
    mem[775] = 8'h00;
    mem[776] = 8'h00;
    mem[777] = 8'h00;
    mem[778] = 8'h00;
    mem[779] = 8'h00;
    mem[780] = 8'h00;
    mem[781] = 8'h00;
    mem[782] = 8'h00;
    mem[783] = 8'h00;
    mem[784] = 8'h00;
    mem[785] = 8'h00;
    mem[786] = 8'h00;
    mem[787] = 8'h00;
    mem[788] = 8'h00;
    mem[789] = 8'h00;
    mem[790] = 8'h00;
    mem[791] = 8'h00;
    mem[792] = 8'h00;
    mem[793] = 8'h00;
    mem[794] = 8'h00;
    mem[795] = 8'h00;
    mem[796] = 8'h00;
    mem[797] = 8'h00;
    mem[798] = 8'h00;
    mem[799] = 8'h00;
    mem[800] = 8'h00;
    mem[801] = 8'h00;
    mem[802] = 8'h00;
    mem[803] = 8'h00;
    mem[804] = 8'h00;
    mem[805] = 8'h00;
    mem[806] = 8'h00;
    mem[807] = 8'h00;
    mem[808] = 8'h00;
    mem[809] = 8'h00;
    mem[810] = 8'h00;
    mem[811] = 8'h00;
    mem[812] = 8'h00;
    mem[813] = 8'h00;
    mem[814] = 8'h00;
    mem[815] = 8'h00;
    mem[816] = 8'h00;
    mem[817] = 8'h00;
    mem[818] = 8'h00;
    mem[819] = 8'h00;
    mem[820] = 8'h00;
    mem[821] = 8'h00;
    mem[822] = 8'h00;
    mem[823] = 8'h00;
    mem[824] = 8'h00;
    mem[825] = 8'h00;
    mem[826] = 8'h00;
    mem[827] = 8'h00;
    mem[828] = 8'h00;
    mem[829] = 8'h00;
    mem[830] = 8'h00;
    mem[831] = 8'h00;
    mem[832] = 8'h00;
    mem[833] = 8'h00;
    mem[834] = 8'h00;
    mem[835] = 8'h00;
    mem[836] = 8'h00;
    mem[837] = 8'h00;
    mem[838] = 8'h00;
    mem[839] = 8'h00;
    mem[840] = 8'h00;
    mem[841] = 8'h00;
    mem[842] = 8'h00;
    mem[843] = 8'h00;
    mem[844] = 8'h00;
    mem[845] = 8'h00;
    mem[846] = 8'h00;
    mem[847] = 8'h00;
    mem[848] = 8'h00;
    mem[849] = 8'h00;
    mem[850] = 8'h00;
    mem[851] = 8'h00;
    mem[852] = 8'h00;
    mem[853] = 8'h00;
    mem[854] = 8'h00;
    mem[855] = 8'h00;
    mem[856] = 8'h00;
    mem[857] = 8'h00;
    mem[858] = 8'h00;
    mem[859] = 8'h00;
    mem[860] = 8'h00;
    mem[861] = 8'h00;
    mem[862] = 8'h00;
    mem[863] = 8'h00;
    mem[864] = 8'h00;
    mem[865] = 8'h00;
    mem[866] = 8'h00;
    mem[867] = 8'h00;
    mem[868] = 8'h00;
    mem[869] = 8'h00;
    mem[870] = 8'h00;
    mem[871] = 8'h00;
    mem[872] = 8'h00;
    mem[873] = 8'h00;
    mem[874] = 8'h00;
    mem[875] = 8'h00;
    mem[876] = 8'h00;
    mem[877] = 8'h00;
    mem[878] = 8'h00;
    mem[879] = 8'h00;
    mem[880] = 8'h00;
    mem[881] = 8'h00;
    mem[882] = 8'h00;
    mem[883] = 8'h00;
    mem[884] = 8'h00;
    mem[885] = 8'h00;
    mem[886] = 8'h00;
    mem[887] = 8'h00;
    mem[888] = 8'h00;
    mem[889] = 8'h00;
    mem[890] = 8'h00;
    mem[891] = 8'h00;
    mem[892] = 8'h00;
    mem[893] = 8'h00;
    mem[894] = 8'h00;
    mem[895] = 8'h00;
    mem[896] = 8'h00;
    mem[897] = 8'h00;
    mem[898] = 8'h00;
    mem[899] = 8'h00;
    mem[900] = 8'h00;
    mem[901] = 8'h00;
    mem[902] = 8'h00;
    mem[903] = 8'h00;
    mem[904] = 8'h00;
    mem[905] = 8'h00;
    mem[906] = 8'h00;
    mem[907] = 8'h00;
    mem[908] = 8'h00;
    mem[909] = 8'h00;
    mem[910] = 8'h00;
    mem[911] = 8'h00;
    mem[912] = 8'h00;
    mem[913] = 8'h00;
    mem[914] = 8'h00;
    mem[915] = 8'h00;
    mem[916] = 8'h00;
    mem[917] = 8'h00;
    mem[918] = 8'h00;
    mem[919] = 8'h00;
    mem[920] = 8'h00;
    mem[921] = 8'h00;
    mem[922] = 8'h00;
    mem[923] = 8'h00;
    mem[924] = 8'h00;
    mem[925] = 8'h00;
    mem[926] = 8'h00;
    mem[927] = 8'h00;
    mem[928] = 8'h00;
    mem[929] = 8'h00;
    mem[930] = 8'h00;
    mem[931] = 8'h00;
    mem[932] = 8'h00;
    mem[933] = 8'h00;
    mem[934] = 8'h00;
    mem[935] = 8'h00;
    mem[936] = 8'h00;
    mem[937] = 8'h00;
    mem[938] = 8'h00;
    mem[939] = 8'h00;
    mem[940] = 8'h00;
    mem[941] = 8'h00;
    mem[942] = 8'h00;
    mem[943] = 8'h00;
    mem[944] = 8'h00;
    mem[945] = 8'h00;
    mem[946] = 8'h00;
    mem[947] = 8'h00;
    mem[948] = 8'h00;
    mem[949] = 8'h00;
    mem[950] = 8'h00;
    mem[951] = 8'h00;
    mem[952] = 8'h00;
    mem[953] = 8'h00;
    mem[954] = 8'h00;
    mem[955] = 8'h00;
    mem[956] = 8'h00;
    mem[957] = 8'h00;
    mem[958] = 8'h00;
    mem[959] = 8'h00;
    mem[960] = 8'h00;
    mem[961] = 8'h00;
    mem[962] = 8'h00;
    mem[963] = 8'h00;
    mem[964] = 8'h00;
    mem[965] = 8'h00;
    mem[966] = 8'h00;
    mem[967] = 8'h00;
    mem[968] = 8'h00;
    mem[969] = 8'h00;
    mem[970] = 8'h00;
    mem[971] = 8'h00;
    mem[972] = 8'h00;
    mem[973] = 8'h00;
    mem[974] = 8'h00;
    mem[975] = 8'h00;
    mem[976] = 8'h00;
    mem[977] = 8'h00;
    mem[978] = 8'h00;
    mem[979] = 8'h00;
    mem[980] = 8'h00;
    mem[981] = 8'h00;
    mem[982] = 8'h00;
    mem[983] = 8'h00;
    mem[984] = 8'h00;
    mem[985] = 8'h00;
    mem[986] = 8'h00;
    mem[987] = 8'h00;
    mem[988] = 8'h00;
    mem[989] = 8'h00;
    mem[990] = 8'h00;
    mem[991] = 8'h00;
    mem[992] = 8'h00;
    mem[993] = 8'h00;
    mem[994] = 8'h00;
    mem[995] = 8'h00;
    mem[996] = 8'h00;
    mem[997] = 8'h00;
    mem[998] = 8'h00;
    mem[999] = 8'h00;
    mem[1000] = 8'h00;
    mem[1001] = 8'h00;
    mem[1002] = 8'h00;
    mem[1003] = 8'h00;
    mem[1004] = 8'h00;
    mem[1005] = 8'h00;
    mem[1006] = 8'h00;
    mem[1007] = 8'h00;
    mem[1008] = 8'h00;
    mem[1009] = 8'h00;
    mem[1010] = 8'h00;
    mem[1011] = 8'h00;
    mem[1012] = 8'h00;
    mem[1013] = 8'h00;
    mem[1014] = 8'h00;
    mem[1015] = 8'h00;
    mem[1016] = 8'h00;
    mem[1017] = 8'h00;
    mem[1018] = 8'h00;
    mem[1019] = 8'h00;
    mem[1020] = 8'h00;
    mem[1021] = 8'h00;
    mem[1022] = 8'h00;
    mem[1023] = 8'h00;
  end
  always @(posedge clk) begin
    if (mem_w_en) mem[mem_w_addr] <= mem_w_data;
  end
  assign mem_r_data = mem[mem_r_addr];
  assign mem_w_en = wr_en;
  assign mem_w_data = wr_data;
  assign mem_w_addr = wr_addr;
  assign rd_data = mem_r_data;
  assign mem_r_addr = rd_addr;
endmodule
