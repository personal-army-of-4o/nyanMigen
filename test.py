from nmigen import *
from nyanMigen import nyanMigen
import ast
import inspect
import astunparse

def foo(self, platform):
    m = Module()
    self.o = a = Signal()
    self.i1 = b = Signal()
    self.i2 = c = Signal()
    m.d.sync.a = b | c

bar = nyanMigen.code(foo)
str = astunparse.unparse(bar)
print("to run the test: `python3 test.py`")
print("")
print("example conversion")
print("")
print("original:")
print("```python")
print(astunparse.unparse(ast.parse(inspect.getsource(foo))))
print("```")
print("generated:")
print("```python")
print(str)
print("```")
