from nmigen import *
from nyanMigen import nyanMigen
import ast
import inspect
import astunparse

def foo(self, platform):
    m = Module()
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
