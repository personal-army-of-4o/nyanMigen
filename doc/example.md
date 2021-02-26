```python
class c:
    def elaborate(self, platform):
        a = Signal(w)
        b = Signal()
        c = Signal()
        d = Signal(w)
        f = Signal()
        e = Signal()

        cc_flag0 = 1

        if cc_flag0:
            if f | f:
                e = b | c
            else:
                e = b & c
        elif cc_flag1:
            if f:
                e = b | c
            else:
                e = b & c
        sync.a = d + e

```
 ->
```python


class c():

    def __init__(self, w, cc_flag1):
        self.w = w
        self.cc_flag1 = cc_flag1
        self.b = Signal()
        self.c = Signal()
        self.d = Signal(w)
        self.f = Signal()
        self.a = Signal(w)

    def ports(self):
        return [self.b, self.c, self.d, self.f, self.a]

    def inputs(self):
        return [self.b, self.c, self.d, self.f]

    def outputs(self):
        return [self.a]

    def elaborate(self, platform):
        w = self.w
        cc_flag1 = self.cc_flag1
        m = Module()
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        f = self.f
        e = Signal()
        cc_flag0 = 1
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
    import json
    with open('generics.json', 'r') as read_file:
        generics = json.load(read_file)
    top = c(generics.w, generics.cc_flag1)
    main(top, top.ports())

```
457 chars -> 1258 chars
