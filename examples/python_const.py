from nyanMigen import nyanify


@nyanify()
class python_const:
    def elaborate(self, platform):
        o = Signal(32)
        val= 12345
        o = val

if __name__ == '__main__':
    python_const.main()
