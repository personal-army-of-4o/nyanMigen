from nmigen import *
from nmigen.cli import main
from nyanMigen import nyanify


@nyanify(generics_file="config.json")
class ram:
    def elaborate(self, platform):
        n = 0
        wr_en = Signal()
        wr_addr = Signal(aw)
        wr_data = Signal(dw)
        rd_addr = Signal(aw+2)
        rd_data = Signal(dw//4)

        mem = Array(Signal(dw) for i in range(2**aw))
        sData = Signal(dw)
        sRd_addr = Signal(aw)
        sSel = Signal(2)

        sRd_addr = rd_addr[2:]
        sSel = rd_addr[0:2]

        for i in range(n):
            if reg_wr:
                wr_en_reg = Signal()
                wr_addr_reg = Signal(aw)
                wr_data_reg = Signal(dw)

                sync.wr_en_reg = wr_en
                sync.wr_addr_reg = wr_addr
                sync.wr_data_reg = wr_data

                if wr_en_reg:
                    sync.mem[wr_addr_reg] = wr_data_reg
            else:
                if wr_en:
                    sync.mem[wr_addr] = wr_data

        sData = mem[sRd_addr]

        with switch(sSel):
            with case(0):
                rd_data = sData[0:dw]
            with case(1):
                rd_data = sData[dw:dw*2]
            with case(2):
                rd_data = sData[dw*2:dw*3]
            with default:
                rd_data = sData[dw*3:dw*4]

if (__name__ == '__main__'):
    ram.main()
