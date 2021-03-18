from nyanMigen import nyanify


@nyanify(generics_file="config.json")
class indexing:
    def elaborate(self, platform):
        n = 3
        inp = Signal(n**n)
        outp = Signal(n**n)
        ari = Array(Array(Signal for _ in range(n)) for _ in range(n))
        aro = Array(Array(Signal for _ in range(n)) for _ in range(n))

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    index = i*(n**2) + j*(n) + k
                    v = inp[index]
                    ari[i][j][k] = v

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    sync.aro[i][j][k] = ari[j][k][i]

        outp = Cat(Cat(aro))

if (__name__ == '__main__'):
    indexing.main()