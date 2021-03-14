```python
class ram:
    def elaborate(self, platform):
        n = 10
        wr_en = Signal()
        wr_addr = Signal(aw)
        wr_data = Signal(dw)
        rd_addr = Signal(aw+2)
        rd_data = Signal(dw//4)

        Memory(width = dw, depth = 2**aw, we = wr_en, wa = wr_addr, wd = sync.wr_data, ra = rd_addr, rd = rd_data)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    sync.rd_data[i][j][k] = wr_data[i][j][k]

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
        top = ram(generics['aw'], generics['dw'])
        main(top, name='ram', ports=top.ports())

    def __init__(self, aw, dw):
        pass
        self.aw = aw
        self.dw = dw
        self.wr_en = Signal()
        self.wr_addr = Signal(aw)
        self.wr_data = Signal(dw)
        self.rd_addr = Signal((aw + 2))
        self.rd_data = Signal((dw // 4))

    def ports(self):
        return [self.wr_en, self.wr_addr, self.wr_data, self.rd_addr, self.rd_data]

    def inputs(self):
        return [self.wr_en, self.wr_addr, self.wr_data, self.rd_addr]

    def outputs(self):
        return [self.rd_data]

    def elaborate(self, platform):
        aw = self.aw
        dw = self.dw
        m = Module()
        n = 10
        wr_en = self.wr_en
        wr_addr = self.wr_addr
        wr_data = self.wr_data
        rd_addr = self.rd_addr
        rd_data = self.rd_data
        mem = Memory(width=dw, depth=(2 ** aw))
        m.submodules.rdport0 = rdport0 = mem.read_port(domain='comb')
        m.submodules.wrport0 = wrport0 = mem.write_port(domain='sync')
        m.d.comb += [rdport0.addr.eq(rd_addr), rd_data.eq(rdport0.data), wrport0.addr.eq(wr_addr), wrport0.data.eq(wr_data), wrport0.en.eq(wr_en)]
        for i in range(10):
            for j in range(10):
                for k in range(10):
                    m.d.sync += rd_data[i][j][k].eq(wr_data[i][j][k])
        return m

```
{'dw': 8, 'aw': 10, 'reg_wr': False}
