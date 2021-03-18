from nyanMigen import nyanify


@nyanify()
class blink:
    def elaborate(self, platform):
        cnt = Signal(24)
        led = Signal()

        sync.cnt = cnt+1
        led = cnt[23]

if __name__ == '__main__':
    blink.main()
