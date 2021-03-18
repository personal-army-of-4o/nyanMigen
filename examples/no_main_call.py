from nyanMigen import nyanify


@nyanify()
class no_main_call:
    def elaborate(self, platform):
        a = Signal()
        b = Signal()
        b = a
