```python
class ram:
    def elaborate(self, platform):
        n = 0
        wr_en = Signal()
        wr_addr = Signal(aw)
        wr_data = Signal(dw)
        rd_addr = Signal(aw)
        rd_data = Signal(dw)

        mem = Array(Signal(dw) for i in range(2**aw))

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

        rd_data = mem[rd_addr]

```
 ->
```python

from nmigen import *
from nmigen.cli import main

class ram(Elaboratable):

    def main():
        import json
        with open('config.json', 'r') as read_file:
            generics = json.load(read_file)
        print(generics)
        top = ram(generics['aw'], generics['dw'], generics['reg_wr'])
        main(top, name='ram', ports=top.ports())

    def __init__(self, aw, dw, reg_wr):
        pass
        self.aw = aw
        self.dw = dw
        self.reg_wr = reg_wr
        self.wr_en = Signal()
        self.wr_addr = Signal(aw)
        self.wr_data = Signal(dw)
        self.rd_addr = Signal(aw)
        self.rd_data = Signal(dw)

    def ports(self):
        return [self.wr_en, self.wr_addr, self.wr_data, self.rd_addr, self.rd_data]

    def inputs(self):
        return [self.wr_en, self.wr_addr, self.wr_data, self.rd_addr]

    def outputs(self):
        return [self.rd_data]

    def elaborate(self, platform):
        aw = self.aw
        dw = self.dw
        reg_wr = self.reg_wr
        m = Module()
        n = 0
        wr_en = self.wr_en
        wr_addr = self.wr_addr
        wr_data = self.wr_data
        rd_addr = self.rd_addr
        rd_data = self.rd_data
        mem = Array((Signal(dw) for i in range((2 ** aw))))
        for i in range(n):
            if reg_wr:
                wr_en_reg = Signal()
                wr_addr_reg = Signal(aw)
                wr_data_reg = Signal(dw)
                m.d.sync += wr_en_reg.eq(wr_en)
                m.d.sync += wr_addr_reg.eq(wr_addr)
                m.d.sync += wr_data_reg.eq(wr_data)
                with m.If(wr_en_reg):
                    m.d.sync += mem[wr_addr_reg].eq(wr_data_reg)
            else:
                with m.If(wr_en):
                    m.d.sync += mem[wr_addr].eq(wr_data)
        m.d.comb += rd_data.eq(mem[rd_addr])
        return m

```
{'dw': 8, 'aw': 10, 'reg_wr': False}
