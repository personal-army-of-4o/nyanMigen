from nyanMigen import nyanify


@nyanify
def fsm_default_encoding():
    s = Fsm(init = 'one')
    o = Signal()

    with switch(s):
        with case('one'):
            s = 'two'
            o = 1
        with case('two'):
            s = 'one'
            o = 0
