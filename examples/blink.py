from nyanMigen import nyanify


@nyanify()
def blink():
    cnt = Signal(24)

    sync.cnt = cnt+1
    led = cnt[23]
