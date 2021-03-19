from nyanMigen import nyanify


@nyanify()
class simple_inheritance:
    def elaborate(self, platform):
        ins = Signal()
        inv = Signal(32)
        outs = ins
        outv = inv
