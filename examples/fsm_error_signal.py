from nyanMigen import nyanify


@nyanify()
def fsm_error_signal():
    s = Fsm(encoding = 'onehot', init = 'one')
    o = Signal()
    o = s.error
    with switch(s):
        with case('one'):
            s = 'two'
        with case('two'):
            s = 'one'
