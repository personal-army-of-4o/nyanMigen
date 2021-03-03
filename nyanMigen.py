import ast
import inspect
from ast import Assign, AugAssign, Name, Load, Store, Call, If, Subscript
from pprintast import pprintast as ppa
from astunparse import unparse


def nyanify(generics_file = None):
    def foo(cls):
        cls_str = inspect.getsource(cls)
        cls_src = ast.parse(cls_str)
        classname = cls_src.body[0].name
        nyanMigen.add_heritage(cls_src)
        print("```python\n" + cls_str + "\n```")
        l = len(cls_str)
        code = nyanMigen.parse(cls_src, "elaborate")
        (elaborate, ctx) = nyanMigen.fix(code)
        ports = nyanMigen.gen_ports(ctx)
        inputs = nyanMigen.gen_in_ports(ctx)
        outputs = nyanMigen.gen_out_ports(ctx)
        init = nyanMigen.gen_init(ctx)
        e = nyanMigen.gen_exec(cls_src, ctx, generics_file)
        cls_src.body[0].body = [e, init, ports, inputs, outputs, elaborate]
        imports = ast.parse("from nmigen import Elaboratable").body
        imports.extend(cls_src.body)
        cls_src.body = imports
        print(" ->\n```python\n" + unparse(cls_src) + "\n```")
        print(l, "chars ->", len(unparse(cls_src)), "chars")
        for i in ctx:
            print(i, ctx[i])
        return nyanMigen.compile(cls_src, classname)
    return foo

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
            raise Exception("can't find `" + fn + "` method on class", cls.body[0].name)
        return ast.parse(code)

    def add_heritage(cls):
        code = ast.parse("class foo(Elaboratable):\n    pass")
        cls.body[0].bases = code.body[0].bases

    def compile(thing, name = None):
        code = compile(filename="fakename", source=thing, mode="exec")
        mod = {}
        exec(code, mod)
        if not name:
            name = thing.body[0].name
        return mod[name]

    def fix(code):
        nyanMigen._add_module(code)
        (code.body, ctx) = nyanMigen._nyanify(code.body)
        nyanMigen._add_elab_imports(code)
        nyanMigen._replace_ports_assigns(code.body, ctx)
        nyanMigen._add_return_module(code.body)
        nyanMigen._add_generics_to_elaborate(code, ctx)
        return (code, ctx)

    def gen_ports(ctx):
        return nyanMigen._gen_ports(ctx, "ports", nyanMigen._get_ports)

    def gen_in_ports(ctx):
        return nyanMigen._gen_ports(ctx, "inputs", nyanMigen._get_inputs)

    def gen_out_ports(ctx):
        return nyanMigen._gen_ports(ctx, "outputs", nyanMigen._get_outputs)

    def gen_init(ctx):
        gnames = nyanMigen._get_generics(ctx)
        args_string = ""
        generics = []
        for i in gnames:
            args_string += ", " + i
            generics.append(ast.parse("self." + i + " = " + i).body[0])
        code = ast.parse("def __init__(self" + args_string + "):\n" +
            "    from nmigen import Module, Signal, Array\n"
        ).body[0]
        body = generics
        for i in nyanMigen._get_ports(ctx):
            add = ast.parse("self.a = Signal()").body[0]
            add.targets[0].attr = i
            if ctx[i]["args"]:
                add.value.args = ctx[i]["args"]
            body.append(add)
        code.body.extend(body)
        return code

    def _add_elab_imports(code):
        add = ast.parse("from nmigen import Module, Signal, Array").body
        add.extend(code.body)
        code.body = add

    def gen_exec(cls, ctx, generics_file):

        def add_generics2str(string):
            return "generics[\"" + string + "\"]"

        generics_str = ""
        args_str = ""
        generics = nyanMigen._get_generics(ctx)
        if len(generics) > 0 and generics_file:
            generics_str = (
                "    import json\n" +
                "    with open('" + generics_file + "', 'r') as read_file:\n" +
                "        generics = json.load(read_file)\n" +
                "    print(generics)\n"
            )
            args_str = ', '.join(map(add_generics2str, generics))
        str = (
            "def main():\n" +
            generics_str +
            "    top = " + cls.body[0].name + "(" + args_str + ")\n" +
            "    from nmigen.cli import main\n" +
            "    main(top, name = \"" + cls.body[0].name + "\", ports = top.ports())"
        )
        code = ast.parse(str)
        return code.body[0]

    def _add_generics_to_elaborate(body, ctx):
        generics = []
        gnames = nyanMigen._get_generics(ctx)
        for i in gnames:
            add = ast.parse(i + " = self." + i).body[0]
            generics.append(add)
        generics.extend(body.body)
        body.body = generics

    def _get_generics(ctx):
        generics = []
        for i in ctx:
            if nyanMigen._is_type(ctx, i, "other") and not nyanMigen._is_initialized(ctx, i):
                generics.append(i)
        return generics

    def _add_return_module(code):
        add = ast.parse("return m").body[0]
        code.append(add)

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
            converted = False
            for f in converters:
                try:
                    if isinstance(i, Assign):
                        for j in i.targets:
                            try:
                                nyanMigen._set_to_initialized(j.id, ctx)
                            except:
                                pass
                except:
                    pass
                try:
                    ii = f(i, ctx)
                    if ii:
                        i = ii
                        converted = True
                        break
                except Exception as e:
                    pass
            if not converted:
                print("failed to convert line")
                ppa(i)
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
                            nyanMigen._set_type(ctx, i.id, "Signal()", code.value.args)
                            nyanMigen._parse_deps(code.value.args, ctx)
                            return code
            elif (
                code.value.func.id == "Array" and
                isinstance(code.value.func.ctx, Load) and
                len(code.value.keywords) == 0
            ):
                for i in code.targets:
                    if isinstance(i, Name):
                        if isinstance(i.ctx, Store):
                            nyanMigen._set_type(ctx, i.id, "Array()", code.value.args)
                            return code

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
                            return code

    @converter
    def _convert_comb_assign(code, ctx):
        (target, value) = i = nyanMigen._parse_comb_assign(code)
        module = nyanMigen._get_module(ctx)
        if not module:
            return
        if nyanMigen._can_convert_comb_assign(i, ctx):
            nyanMigen._parse_deps(value, ctx)
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
        slice = None
        try:
            (domain, target, value) = i = nyanMigen._parse_sync_assign(code)
        except:
            (domain, target, value, slice) = i = nyanMigen._parse_sync_assign_slice(code)
        module = nyanMigen._get_module(ctx)
        if nyanMigen._can_convert_sync_assign(i, ctx):
            nyanMigen._parse_deps(value, ctx)
            if slice:
                nyanMigen._parse_deps(slice, ctx)
            nyanMigen._add_target(target, ctx)
            return nyanMigen._dump_assign(module, domain, target, value, slice)
        else:
            raise Exception()

    @converter
    def _convert_if(code, ctx):
        if isinstance(code, If):
            deps = nyanMigen._parse_deps(code.test, ctx)
            nyanMigen._add_drivers_to_ctx(deps, ctx)
            doit = nyanMigen._is_signal(ctx, deps)
            if doit:
                return nyanMigen._gen_if_code(code, ctx)
            else:
                (code.body, ctx) = nyanMigen._nyanify(code.body, ctx)
                if len(code.orelse) > 0:
                    (code.orelse, ctx) = nyanMigen._nyanify(code.orelse, ctx)
                return code

    def _add_target(target, ctx):
        if target in ctx:
            if nyanMigen._is_signal(ctx, target):
                ctx[target]["is_driven"] = True

    def _parse_deps(value, ctx):
        ret = []
        if isinstance(value, list):
            for i in value:
                ret.extend(nyanMigen._parse_deps(i, ctx))
        else:
            try:
                if isinstance(value.ctx, Load):
                    if value.id not in ctx:
                        ctx[value.id] = {}
                    ctx[value.id]["driver"] = True
                    ret.append(value.id)
                    if nyanMigen._get_type(ctx, value.id) == None:
                        nyanMigen._set_type(ctx, value.id, "other")
            except:
                try:
                    for i in value.__dict__.keys():
                        ret.extend(nyanMigen._parse_deps(getattr(value, i), ctx))
                except Exception as e:
                    pass
        return ret

    def _get_ports(ctx):
        ret = nyanMigen._get_inputs(ctx)
        ret.extend(nyanMigen._get_outputs(ctx))
        return ret

    def _get_inputs(ctx):
        ret = []
        for i in ctx:
            if nyanMigen._is_signal(ctx, i):
                if ctx[i]["is_driven"] == False:
                    if ctx[i]["driver"]:
                        ret.append(i)
        return ret

    def _get_outputs(ctx):
        ret = []
        for i in ctx:
            if nyanMigen._is_signal(ctx, i):
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

    def _set_to_initialized(n, ctx):
        if n not in ctx:
            ctx[n] = {}
        ctx[n]["initialized"] = True

    def _is_initialized(ctx, n):
        try:
            return ctx[n]["initialized"]
        except:
            return False

    def _set_type(ctx, n, v, args = None):
        if not n in ctx:
            ctx[n] = {}
        if "type" in ctx[n]:
            print("warning: redefining type on", n)
        ctx[n]["type"] = v
        if v != "Module()":
            ctx[n]["driver"] = False
            ctx[n]["is_driven"] = False
            ctx[n]["args"] = args

    def _get_type(ctx, n):
        if n in ctx:
            if "type" in ctx[n]:
                return ctx[n]["type"]

    def _is_signal(ctx, v):
        if isinstance(v, list):
            for i in v:
                if nyanMigen._is_signal(ctx, i):
                    return True
        else:
            return ((nyanMigen._get_type(ctx, v) == "Array()") or (nyanMigen._get_type(ctx, v) == "Signal()"))
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
            nyanMigen._is_signal(ctx, arg[0])
        ):
            return True
        return False

    def _can_convert_sync_assign(arg, ctx):
        if (nyanMigen._is_signal(ctx, arg[1])):
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

    def _parse_sync_assign_slice(code):
        if isinstance(code, Assign):
            if len(code.targets) == 1:
                domain = code.targets[0].value.value.id
                target = code.targets[0].value.attr
                slice = code.targets[0].slice
                value = code.value
        return (domain, target, value, slice)

    def _dump_assign(m, d, t, v, s = None):
        if not d:
            d = "comb"
        if s:
            ret = ast.parse("m.d.sync += t[s].eq(v)").body[0]
            ret.value.func.value.value.id = t
            ret.value.func.value.slice = s
            ret.value.args = [v]
        else:
            ret = ast.parse("m.d.sync += t.eq(v)").body[0]
            ret.value.func.value.id = t
            ret.value.args = [v]
        ret.target.value.value.id = m
        ret.target.attr = d
        return ret

    @converter
    def _convert_branching(code, ctx):
        return None


