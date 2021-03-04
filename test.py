from nmigen import *
from nmigen.cli import main
from nyanMigen import nyanify


@nyanify(generics_file="config.json")
class ram:
    def elaborate(self, platform):
        wr_en = Signal()
        wr_addr = Signal(aw)
        wr_data = Signal(dw)
        rd_addr = Signal(aw+2)
        rd_data = Signal(dw//4)

        Memory(width = dw, depth = 2**aw, we = wr_en, wa = wr_addr, wd = wr_data, ra = rd_addr, rd = rd_data)

if (__name__ == '__main__'):
    ram.main()
