```python
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

```
failed to convert line
Assign(targets=[
    Subscript(value=Attribute(value=Name(id='sync', ctx=Load()), attr='mem', ctx=Load()), slice=Index(value=Name(id='wr_addr_reg', ctx=Load())), ctx=Store()),
  ], value=Name(id='wr_data_reg', ctx=Load()))
failed to convert line
Assign(targets=[
    Subscript(value=Attribute(value=Name(id='sync', ctx=Load()), attr='mem', ctx=Load()), slice=Index(value=Name(id='wr_addr', ctx=Load())), ctx=Store()),
  ], value=Name(id='wr_data', ctx=Load()))
 ->
```python


class ram():

    def __init__(self, aw, dw, reg_wr):
        self.aw = aw
        self.dw = dw
        self.reg_wr = reg_wr
        self.wr_en = Signal()
        self.wr_addr = Signal(aw)
        self.wr_data = Signal(dw)
        self.rd_addr = Signal(aw)
        self.mem = Signal((Signal(dw) for i in range((2 ** aw))))
        self.rd_data = Signal(dw)
        self.wr_addr_reg = Signal(aw)
        self.wr_data_reg = Signal(dw)

    def ports(self):
        return [self.wr_en, self.wr_addr, self.wr_data, self.rd_addr, self.mem, self.rd_data, self.wr_addr_reg, self.wr_data_reg]

    def inputs(self):
        return [self.wr_en, self.wr_addr, self.wr_data, self.rd_addr, self.mem]

    def outputs(self):
        return [self.rd_data, self.wr_addr_reg, self.wr_data_reg]

    def elaborate(self, platform):
        aw = self.aw
        dw = self.dw
        reg_wr = self.reg_wr
        from nmigen import Module, Signal, If, Else, Array
        m = Module()
        wr_en = self.wr_en
        wr_addr = self.wr_addr
        wr_data = self.wr_data
        rd_addr = self.rd_addr
        rd_data = self.rd_data
        mem = self.mem
        if reg_wr:
            wr_en_reg = Signal()
            wr_addr_reg = Signal(aw)
            wr_data_reg = Signal(dw)
            m.d.sync += wr_en_reg.eq(wr_en)
            m.d.sync += wr_addr_reg.eq(wr_addr)
            m.d.sync += wr_data_reg.eq(wr_data)
            with m.If(wr_en_reg):
                sync.mem[wr_addr_reg] = wr_data_reg
        else:
            with m.If(wr_en):
                sync.mem[wr_addr] = wr_data
        m.d.comb += rd_data.eq(mem[rd_addr])
        return m
if (__name__ == '__main__'):
    import json
    with open('config.json', 'r') as read_file:
        generics = json.load(read_file)
    top = ram(generics.aw, generics.dw, generics.reg_wr)
    from nMigen.cli import main
    main(top, top.ports())

```
660 chars -> 1892 chars
m {'initialized': True, 'type': 'Module()'}
wr_en {'initialized': True, 'type': 'Signal()', 'driver': True, 'is_driven': False, 'args': []}
wr_addr {'initialized': True, 'type': 'Signal()', 'driver': True, 'is_driven': False, 'args': [<_ast.Name object at 0xb5f47e90>]}
aw {'driver': True, 'type': 'other', 'is_driven': False, 'args': None}
wr_data {'initialized': True, 'type': 'Signal()', 'driver': True, 'is_driven': False, 'args': [<_ast.Name object at 0xb5f47d10>]}
dw {'driver': True, 'type': 'other', 'is_driven': False, 'args': None}
rd_addr {'initialized': True, 'type': 'Signal()', 'driver': True, 'is_driven': False, 'args': [<_ast.Name object at 0xb5f47610>]}
rd_data {'initialized': True, 'type': 'Signal()', 'driver': False, 'is_driven': True, 'args': [<_ast.Name object at 0xb5f47650>]}
mem {'initialized': True, 'type': 'Array()', 'driver': True, 'is_driven': False, 'args': [<_ast.GeneratorExp object at 0xb5f47710>]}
reg_wr {'driver': True, 'type': 'other', 'is_driven': False, 'args': None}
wr_en_reg {'initialized': True, 'type': 'Signal()', 'driver': True, 'is_driven': True, 'args': []}
wr_addr_reg {'initialized': True, 'type': 'Signal()', 'driver': False, 'is_driven': True, 'args': [<_ast.Name object at 0xb5f479b0>]}
wr_data_reg {'initialized': True, 'type': 'Signal()', 'driver': False, 'is_driven': True, 'args': [<_ast.Name object at 0xb5f47a70>]}
