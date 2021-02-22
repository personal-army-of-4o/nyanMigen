from nyanMigen import nyanify


@nyanify
class c:
    def __init__(self):
        pass
    def elaborate(self, platform):
        self.o = a = Signal()
        self.i1 = b = Signal()
        self.i2 = c = Signal()
        self.i3 = d = Signal()
        self.i4 = f = Signal()
        e = Signal()

        cc_flag0 = 1
        cc_flag1 = 1

        if cc_flag0:
            if f:
                e = b | c
            else:
                e = b & c
        elif cc_flag1:
            if f:
                e = b | c
            else:
                e = b & c
        sync.a = d | e

