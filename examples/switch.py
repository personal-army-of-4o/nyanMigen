from nyanMigen import nyanify


@nyanify
def switch():
    a = Signal(2)
    b = Signal(2)

    with switch(a):
        b = 3
        with case(0):
            b = 1
        with case(1):
            b = 0
