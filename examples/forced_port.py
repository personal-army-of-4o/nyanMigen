from nyanMigen import nyanify


@nyanify()
class forced_port:
    def elaborate(self, platform):
        a = Signal(5)
        b = Signal(5, port = True)
        c = Signal(5)

        b = a
        c = b
