from nmigen import *
from nmigen.cli import main
from nyanMigen import nyanify


@nyanify(generics_file="config.json")
class ram:
    def elaborate(self, platform):
        wr_en = Signal()
        wr_addr = Signal(aw)
        wr_data = Signal(dw)
        rd_addr = Signal(aw)
        rd_data = Signal(dw)

        mem = Array(Signal(dw) for i in range(2**aw))

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

        rd_data = mem[rd_addr]

if (__name__ == '__main__'):
    ram.main()
