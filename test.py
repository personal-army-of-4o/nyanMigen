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
        m.d.sync.a = b | c

