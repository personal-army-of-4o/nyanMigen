from nyanMigen import nyanify


@nyanify()
def inherit_width_from_slicing():
    cnt = Signal(24)

    sync.cnt = cnt+1
    led = cnt[23]
