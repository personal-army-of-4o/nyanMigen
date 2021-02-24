import ast
import inspect
from ast import Assign, AugAssign, Name, Load, Store, Call, If
from pprintast import pprintast as ppa
from astunparse import unparse


def nyanify(cls):
    cls_src = ast.parse(inspect.getsource(cls))
    print("```python\n" + unparse(cls_src) + "\n```")
    l = len(unparse(cls_src))
    code = nyanMigen.parse(cls_src, "elaborate")
    (elaborate, ctx) = nyanMigen.fix(code)
    cls_src.body[0].decorator_list = []
    ports = nyanMigen.gen_ports(ctx)
    inputs = nyanMigen.gen_in_ports(ctx)
    outputs = nyanMigen.gen_out_ports(ctx)
    init = nyanMigen.gen_init(ctx)
    e = nyanMigen.gen_exec(cls_src)
    cls_src.body[0].body = [init, ports, inputs, outputs, elaborate]
    cls_src.body.append(e)
    print("```python\n" + unparse(cls_src) + "\n```")
    print(l, "->", len(unparse(cls_src)))
    return nyanMigen.compile(cls_src)

converters = []
def converter(foo):
    converters.append(foo)
    return foo

class nyanMigen:
    def parse(cls, fn):
        code = None
        for i in cls.body[0].body:
            if i.name == fn:
                code = i
        if not code:
            raise Exception("can't find `elaborate` method on class", cls.body[0].name)
        return ast.parse(code)

    def compile(thing):
        code = compile(filename="fakename", source=thing, mode="exec")
        mod = {}
        exec(code, mod)
        return mod[thing.body[0].name]

    def fix(code):
        nyanMigen._add_module(code)
        (code.body, ctx) = nyanMigen._nyanify(code.body)
        nyanMigen._replace_ports_assigns(code.body, ctx)
        return (code, ctx)

    def gen_ports(ctx):
        return nyanMigen._gen_ports(ctx, "ports", nyanMigen._get_ports)

    def gen_in_ports(ctx):
        return nyanMigen._gen_ports(ctx, "inputs", nyanMigen._get_inputs)

    def gen_out_ports(ctx):
        return nyanMigen._gen_ports(ctx, "outputs", nyanMigen._get_outputs)

    def gen_init(ctx):
        code = ast.parse("def __init__(self):\n    pass").body[0]
        body = []
        for i in nyanMigen._get_ports(ctx):
            add = ast.parse("self.a = Signal()").body[0]
            add.targets[0].attr = i
            body.append(add)
        code.body = body
        return code

    def gen_exec(cls):
        code = ast.parse("if __name__ == \"__main__\":\n    top = " + cls.body[0].name + "()\n    main(top, top.ports())")
        return code.body[0]

    def _replace_ports_assigns(body, ctx):
        ports = nyanMigen._get_ports(ctx)
        for n in range(len(body)):
            i = body[n]
            try:
                if isinstance(i, Assign) and len(i.targets) == 1 and i.targets[0].id in ports:
                    add = ast.parse("a = self.a").body[0]
                    add.targets[0].id = i.targets[0].id
                    add.value.attr  = i.targets[0].id
                    body[n] = add
            except:
                pass

    def _gen_ports(ctx, name, foo):
        code = ast.parse("def " + name + "(self):\n   return [self.a]").body[0]
        elts = []
        ports = foo(ctx)
        for i in ports:
            add = ast.parse("self.t").body[0].value
            add.attr = i
            elts.append(add)
        code.body[0].value.elts = elts
        return code

    def _add_module(code):
        modcode = ast.parse("m = Module()").body
        modcode.extend(code.body)
        code.body = modcode
        return code

    def _nyanify(code, ctx = None):
        if not ctx:
            ctx = {}
        ret = []
        for i in code:
            for f in converters:
                try:
                    ii = f(i, ctx)
                    if ii:
                        i = ii
                        break
                except Exception as e:
                    pass
            if isinstance(i, list):
                ret.extend(i)
            else:
                ret.append(i)
        return (ret, ctx)

    @converter
    def _parse_signal(code, ctx):
        if isinstance(code, Assign):
            if (
                code.value.func.id == "Signal" and
                isinstance(code.value.func.ctx, Load) and
                len(code.value.keywords) == 0
            ):
                for i in code.targets:
                    if isinstance(i, Name):
                        if isinstance(i.ctx, Store):
                            nyanMigen._set_type(ctx, i.id, "Signal()")

    @converter
    def _parse_module(code, ctx):
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
                            nyanMigen._set_type(ctx, i.id, "Module()")

    @converter
    def _convert_comb_assign(code, ctx):
        (target, value) = i = nyanMigen._parse_comb_assign(code)
        module = nyanMigen._get_module(ctx)
        if not module:
            return
        if nyanMigen._can_convert_comb_assign(i, ctx):
            nyanMigen._parse_assign_deps(value, ctx)
            nyanMigen._add_target(target, ctx)
            return nyanMigen._dump_assign(module, None, target, value)
        else:
            raise Exception()

    def _get_module(ctx):
        for i in list(ctx.keys()):
            if nyanMigen._is_type(ctx, i, "Module()"):
                return i
        return None

    @converter
    def _convert_sync_assign(code, ctx):
        (domain, target, value) = i = nyanMigen._parse_sync_assign(code)
        module = nyanMigen._get_module(ctx)
        if nyanMigen._can_convert_sync_assign(i, ctx):
            nyanMigen._parse_assign_deps(value, ctx)
            nyanMigen._add_target(target, ctx)
            return nyanMigen._dump_assign(module, domain, target, value)
        else:
            raise Exception()

    @converter
    def _convert_if(code, ctx):
        if isinstance(code, If):
            deps = nyanMigen._get_if_deps(code)
            nyanMigen._add_drivers_to_ctx(deps, ctx)
            doit = nyanMigen._is_signal(deps, ctx)
            if doit:
                return nyanMigen._gen_if_code(code, ctx)
            else:
                (code.body, ctx) = nyanMigen._nyanify(code.body, ctx)
                if len(code.orelse) > 0:
                    (code.orelse, ctx) = nyanMigen._nyanify(code.orelse, ctx)
                return code

    def _add_target(target, ctx):
        if target in ctx:
            if nyanMigen._is_type(ctx, target, "Signal()"):
                ctx[target]["is_driven"] = True

    def _parse_assign_deps(value, ctx):
        if isinstance(value, list):
            for i in value:
                nyanMigen._parse_assign_deps(i, ctx)
        else:
            try:
                if nyanMigen._is_type(ctx, value.id, "Signal()") and isinstance(value.ctx, Load):
                    ctx[value.id]["driver"] = True
            except:
                try:
                    for i in value.__dict__.keys():
                        nyanMigen._parse_assign_deps(getattr(value, i), ctx)
                except Exception as e:
                    pass

    def _get_ports(ctx):
        ret = nyanMigen._get_inputs(ctx)
        ret.extend(nyanMigen._get_outputs(ctx))
        return ret

    def _get_inputs(ctx):
        ret = []
        for i in ctx:
            if nyanMigen._is_type(ctx, i, "Signal()"):
                if ctx[i]["is_driven"] == False:
                    if ctx[i]["driver"]:
                        ret.append(i)
        return ret

    def _get_outputs(ctx):
        ret = []
        for i in ctx:
            if nyanMigen._is_type(ctx, i, "Signal()"):
                if ctx[i]["driver"] == False:
                    if ctx[i]["is_driven"]:
                        ret.append(i)
        return ret

    def _add_drivers_to_ctx(drvs, ctx):
        if isinstance(drvs, list):
            for i in drvs:
                nyanMigen._add_drivers_to_ctx(i, ctx)
        else:
            if not drvs in ctx:
                ctx[drvs] = {}
            ctx[drvs]["driver"] = True

    def _get_if_deps(code):
        if isinstance(code.test, Name):
            return [code.test.id]

    def _set_type(ctx, n, v):
        if not n in ctx:
            ctx[n] = {}
        if "type" in ctx[n]:
            print("warning: redefining type on", n)
        ctx[n]["type"] = v
        if v == "Signal()":
            ctx[n]["driver"] = False
            ctx[n]["is_driven"] = False

    def _get_type(ctx, n):
        if n in ctx:
            if "type" in ctx[n]:
                return ctx[n]["type"]

    def _is_signal(v, ctx):
        if isinstance(v, list):
            for i in v:
                if nyanMigen._is_signal(i, ctx):
                    return True
        else:
            return nyanMigen._get_type(ctx, v) == "Signal()"
        return False

    def _gen_if_code(code, ctx):
        ret = ast.parse("with m.If(cnd):\n    a = b").body[0]
        ret.items[0].context_expr.args[0] = code.test
        (ret.body, ctx) = nyanMigen._nyanify(code.body, ctx)
        if len(code.orelse) > 0:
            elseast = ast.parse("with m.Else():\n    a = b").body[0]
            (elseast.body, ctx) = nyanMigen._nyanify(code.orelse, ctx)
            ret = [ret, elseast]
        return ret

    def _can_convert_comb_assign(arg, ctx):
        if (not isinstance(arg[1], Call) and
            nyanMigen._is_type(ctx, arg[0], "Signal()")
        ):
            return True
        return False

    def _can_convert_sync_assign(arg, ctx):
        if (nyanMigen._is_type(ctx, arg[1], "Signal()")):
            return True
        return False

    def _is_type(ctx, m, t):
        if m in ctx:
            return nyanMigen._get_type(ctx, m) == t
        return False

    def _parse_comb_assign(code):
        if isinstance(code, Assign):
            if len(code.targets) == 1:
                target = code.targets[0].id
                value = code.value
        return (target, value)

    def _parse_sync_assign(code):
        if isinstance(code, Assign):
            if len(code.targets) == 1:
                domain = code.targets[0].value.id
                target = code.targets[0].attr
                value = code.value
        return (domain, target, value)

    def _dump_assign(m, d, t, v):
        if not d:
            d = "comb"
        ret = ast.parse("m.d.sync += t.eq(v)").body[0]
        ret.target.value.value.id = m
        ret.target.attr = d
        ret.value.func.value.id = t
        ret.value.args = [v]
        return ret

    @converter
    def _convert_branching(code, ctx):
        return None


