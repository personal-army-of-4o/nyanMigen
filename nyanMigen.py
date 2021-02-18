import ast
import inspect
from ast import Assign, AugAssign, Name, Load, Store
from pprintast import pprintast as ppa


def nyanify(cls):
    code = nyanMigen.parse(cls.elaborate)
    fixed_code = nyanMigen.fix(code)
    fixed_code.body[0].decorator_list = []
    method = nyanMigen.compile(fixed_code)
    cls.elaborate = method
    return cls

converters = []
def converter(foo):
    converters.append(foo)
    return foo

class nyanMigen:
    def parse(code):
        code = inspect.getsource(code)
        code = nyanMigen.unindent(code)
        return ast.parse(code)

    def unindent(s):
        ret = ""
        indent = 0;
        for i in range(len(s)):
            if s[i] != " ":
                break
            else:
                indent += 1
        if indent > 0:
            for l in s.splitlines():
                if l[0:indent-1] != s[:indent-1]:
                    raise Exception("invalid code string")
                ret += l[indent:] + "\n"
        return ret

    def compile(method):
        code = compile(filename="fakename", source=method, mode="exec")
        mod = {}
        exec(code, mod)
        return mod["elaborate"]

    def fix(code):
        body = nyanMigen._getbody(code)
        body = nyanMigen._nyanify(body)
        nyanMigen._setbody(code, body)
        return code

    def _getbody(code):
        return code.body[0].body

    def _setbody(code, body):
        code.body[0].body = body

    def _nyanify(code):
        ctx = {}
        ret = []
        for i in code:
            for f in converters:
                try:
                    ii = f(i, ctx)
                    if ii:
                        i = ii
                        break
                except:
                    pass
            ret.append(i)
        return ret

    @converter
    def _parse_moodule(code, ctx):
        if isinstance(code, Assign):
            if (
                code.value.func.id == "Signal" and
                isinstance(code.value.func.ctx, Load) and
                len(code.value.keywords) == 0
            ):
                for i in code.targets:
                    if isinstance(i, Name):
                        if isinstance(i.ctx, Store):
                            ctx[i.id] = "Signal()"

    @converter
    def _parse_moodule(code, ctx):
        if isinstance(code, Assign):
            if (
                code.value.func.id == "Module" and
                isinstance(code.value.func.ctx, Load) and
                len(code.value.args) == 0 and
                len(code.value.keywords) == 0
            ):
                for i in code.targets:
                    if isinstance(i, Name):
                        if isinstance(i.ctx, Store):
                            ctx[i.id] = "Module()"

    @converter
    def _convert_assign(code, ctx):
        (module, domain, target, value) = i = nyanMigen._parse_assign(code)
        if nyanMigen._can_convert_assign(i, ctx):
            return nyanMigen._dump_assign(module, domain, target, value)
        else:
            raise Exception()

    def _can_convert_assign(arg, ctx):
        if (nyanMigen._is_type(arg[0], ctx, "Module()") and
            nyanMigen._is_type(arg[2], ctx, "Signal()")
        ):
            return True
        return False

    def _is_type(m, ctx, t):
        if m in ctx:
            if ctx[m] == t:
                return True
        return False

    def _parse_assign(code):
        if isinstance(code, Assign):
            if len(code.targets) == 1:
                module = code.targets[0].value.value.value.id
                domain = code.targets[0].value.attr
                target = code.targets[0].attr
                value = code.value
        return (module, domain, target, value)

    def _dump_assign(m, d, t, v):
        ret = ast.parse("m.d.sync += t.eq(v)").body[0]
        ret.target.value.value.id = m
        ret.target.attr = d
        ret.value.func.value.id = t
        ret.value.args = [v]
        return ret

    @converter
    def _convert_branching(code, ctx):
        return code


