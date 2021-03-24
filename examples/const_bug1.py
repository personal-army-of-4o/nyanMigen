from nyanMigen import nyanify


@nyanify()
def const_bug1():
    n = 3
    index = n*2
    i = Signal(32)
    o = Signal()
    o = i[index]
