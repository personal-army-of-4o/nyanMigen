import ast
from ast import Assign, AugAssign
import inspect
from pprintast import pprintast as ppast


class nyanMigen:
    def code(method):
        code = ast.parse(inspect.getsource(method))
        body = nyanMigen._getbody(code)
        body = nyanMigen._nyanify(body)
        nyanMigen._setbody(code, body)
        return code

    def _getbody(code):
        return code.body[0].body

    def _setbody(code, body):
        code.body[0].body = body

    def _nyanify(code):
        fns = [nyanMigen._convert_assign, nyanMigen._convert_branching]
        ret = []
        for i in code:
            for f in fns:
                try:
                    i = f(i)
                    break
                except:
                    pass
            ret.append(i)
        return ret

    def _convert_assign(code):
        (module, domain, target, value) = nyanMigen._parse_assign(code)
        return nyanMigen._dump_assign(module, domain, target, value)

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

    def _convert_branching(code):
        return code
        
