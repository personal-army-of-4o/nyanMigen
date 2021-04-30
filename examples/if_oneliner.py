
from nyanMigen import nyanify

@nyanify
class if_oneliner:
    def elaborate(self, platform):
        a = Signal()
        b = Signal()
        a = 1 if b else 0
