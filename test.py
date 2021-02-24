from nyanMigen import nyanify


@nyanify
class c:
    def elaborate(self, platform):
        a = Signal()
        b = Signal()
        c = Signal()
        d = Signal()
        f = Signal()
        e = Signal()

        cc_flag0 = 1
        cc_flag1 = 1

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
        sync.a = d | e

