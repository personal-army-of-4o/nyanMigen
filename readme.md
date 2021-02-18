to run the test: `python3 test.py`

example conversion

original:
```python


def foo(self, platform):
    m = Module()
    self.o = a = Signal()
    self.i1 = b = Signal()
    self.i2 = c = Signal()
    m.d.sync.a = (b | c)

```
generated:
```python


def foo(self, platform):
    m = Module()
    self.o = a = Signal()
    self.i1 = b = Signal()
    self.i2 = c = Signal()
    m.d.sync += a.eq((b | c))

```
