to run the test: `python3 test.py`

example conversion

original:
```python


def foo(self, platform):
    m = Module()
    m.d.sync.a = (b | c)

```
generated:
```python


def foo(self, platform):
    m = Module()
    m.d.sync += a.eq((b | c))

```
