from nyanMigen import nyanify


@nyanify
class c:
    def __init__(self):
        pass
    def elaborate(self, platform):
        m = Module()
        self.o = a = Signal()
        self.i1 = b = Signal()
        self.i2 = c = Signal()
        self.i3 = d = Signal()
        e = Signal()
        e = b | c
        m.d.sync.a = d | e

