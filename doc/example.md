```python


class c():

    def elaborate(self, platform):
        a = Signal(8)
        b = Signal()
        c = Signal()
        d = Signal(8)
        f = Signal()
        e = Signal()
        cc_flag0 = 1
        cc_flag1 = 1
        if cc_flag0:
            if (f | f):
                e = (b | c)
            else:
                e = (b & c)
        elif cc_flag1:
            if f:
                e = (b | c)
            else:
                e = (b & c)
        sync.a = (d + e)

```
```python


class c():

    def __init__(self):
        self.b = Signal()
        self.c = Signal()
        self.d = Signal(8)
        self.f = Signal()
        self.a = Signal(8)

    def ports(self):
        return [self.b, self.c, self.d, self.f, self.a]

    def inputs(self):
        return [self.b, self.c, self.d, self.f]

    def outputs(self):
        return [self.a]

    def elaborate(self, platform):
        from nmigen import Module, Signal, If, Else
        m = Module()
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        f = self.f
        e = Signal()
        cc_flag0 = 1
        cc_flag1 = 1
        if cc_flag0:
            with m.If((f | f)):
                m.d.comb += e.eq((b | c))
            with m.Else():
                m.d.comb += e.eq((b & c))
        elif cc_flag1:
            with m.If(f):
                m.d.comb += e.eq((b | c))
            with m.Else():
                m.d.comb += e.eq((b & c))
        m.d.sync += a.eq((d + e))
        return m
if (__name__ == '__main__'):
    top = c()
    from nmigen.cli import main
    main(top, top.ports())

```
478 -> 1111
