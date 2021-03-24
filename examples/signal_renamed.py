from nyanMigen import nyanify


@nyanify()
def signal_renamed():
    i = Signal()
    s = Signal(name = 'sig')
    o = Signal(name = 'os')
    s = i
    o = s
