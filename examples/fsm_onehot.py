from nyanMigen import nyanify


@nyanify()
def fsm_onehot():
    state = test = Fsm(encoding = 'onehot')
    o = Signal()

    with switch(state):
        with case(one):
            o = 0
        with case(two):
            o = 0
        with case(three):
            o = 1

    with switch(state):
        with case(one):
            sync.state = two
        with case(two):
            sync.state = three
        with case(three):
            sync.state = four
