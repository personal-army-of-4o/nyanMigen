from nyanMigen import nyanify


@nyanify
def fsm_encoding_bug1():
    state = Fsm(init = 'idle')
    iStart = Signal()
    oError = Signal()
    with switch(state):
        with case('idle'):
            if iStart:
                state = 'other_state'
        with case('other_state'):
            state = 'idle'
    oError = state.error
