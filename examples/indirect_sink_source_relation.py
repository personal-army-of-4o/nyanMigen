
from nyanMigen import nyanify

@nyanify()
class indirect_sink_source_relation:
    def elaborate(self, platform):
        a = Signal()
        b = Signal()
        v = a
        b = v
