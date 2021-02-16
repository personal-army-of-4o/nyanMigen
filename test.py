from nmigen import *
from nyanMigen import nyanMigen
import ast
import inspect
import astunparse

def foo(self, platform):
    m.d.sync.a = b | c

bar = nyanMigen.code(foo)
str = astunparse.unparse(bar)
print("example conversion")
print("original:")
print(astunparse.unparse(ast.parse(inspect.getsource(foo))))
print("generated:")
print(str)
