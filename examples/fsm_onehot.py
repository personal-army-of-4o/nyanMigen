from nyanMigen import nyanify


@nyanify()
def fsm_onehot():
    state = test = Fsm(encoding = 'onehot', init = 'one')
    o = Signal()
    i = Signal()
    o1 = Signal()
    o2 = Signal()
    o3 = Signal()

    o1 = 1 if state == 'one' else 0

    if 'two' == state:
        o2 = 1
    else:
        o2 = 0

    if i | (state == 'three'):
        o3 = 1
    else:
        o3 = 0

    with switch(state):
        with case('one'):
            state = 'two'
        with case('two'):
            state = 'three'
        with case('three'):
            state = 'four'

    with switch(state):
        with case('one'):
            o = 0
        with case('two'):
            o = 0
        with case('three'):
            o = 1
