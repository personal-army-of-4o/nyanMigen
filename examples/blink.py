from nyanMigen import nyanify


@nyanify()
def blink():
    cnt = Signal(24, domain = 'sync')

    cnt = cnt+1
    led = cnt[23]
