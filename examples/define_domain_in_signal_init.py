from nyanMigen import nyanify


@nyanify
def define_domain_in_signal_init():
    a = Signal()
    b = Signal(domain = 'sync')
    b = a
