import ast
import inspect
from ast import Assign, AugAssign, Name, Load, Store, Call, If, Subscript, Num, Attribute, IfExp,  Str, With, withitem
from pprintast import pprintast as ppa
from astunparse import unparse


def nyanify(generics_file = None, print_ctx = False):
    def foo(cls):
        cls_src = classify(cls)
        classname = cls_src.body[0].name
        nyanMigen.add_heritage(cls_src)
        code = nyanMigen.parse(cls_src, "elaborate")
        (elaborate, ctx) = nyanMigen.fix(code)
        ports = nyanMigen.gen_ports(ctx)
        inputs = nyanMigen.gen_in_ports(ctx)
        outputs = nyanMigen.gen_out_ports(ctx)
        init = nyanMigen.gen_init(ctx)
        e = nyanMigen.gen_exec(cls_src, ctx, generics_file)
        cls_src.body[0].body = [e, init, ports, inputs, outputs, elaborate]
        imports = ast.parse("from nmigen import *\nfrom nmigen.cli import main").body
        imports.extend(cls_src.body)
        cls_src.body = imports
        s = nyanStatistics(cls, cls_src, ctx, classname)
        s.dump_statistics()
        if print_ctx:
            for i in ctx:
                print(i, ctx[i])
        nyanMigen.propagate_constants(cls_src, ctx)
        print(unparse(cls_src))
        ret = nyanMigen.compile(cls_src, classname)
        ret.main()
        return ret

    return foo

def classify(cls):
    if inspect.isclass(cls):
        cls_str = inspect.getsource(cls)
        cls_str = nyanMigen.fix_case(cls_str)
        cls_src = ast.parse(cls_str)
        return cls_src
    elif inspect.isfunction(cls):
        name = cls.__name__
        cls_str = "class " + name + ":\n    def elaborate(self, platform):\n        pass"
        ret = ast.parse(cls_str)

        s = inspect.getsource(cls)
        s = nyanMigen.fix_case(s)
        cls = ast.parse(s).body[0]
        cls.name = 'elaborate'
        cls.args = ast.parse("def foo(self, platform):\n    pass").body[0].args
        cls.decorator_list = []

        ret.body[0].body[0] = cls
        return ret
    else:
        raise Exception("nyanify can only accept class or function")

class nyanStatistics:
    def __init__(self, cls, cls_fixed, ctx, classname):
        def foo (a):
            return a + ": " + ctx[a]["type"]
        self.classname = classname
        self.statistics = {}
        self.statistics["source chars"] = len(inspect.getsource(cls))
        self.statistics["result chars"] = len(unparse(cls_fixed))
        self.statistics["decompression ratio"] = len(unparse(cls_fixed))/len(inspect.getsource(cls))
        self.statistics["inputs(" + str(len(nyanMigen._get_inputs(ctx))) +")"] = list(map(foo, nyanMigen._get_inputs(ctx)))
        self.statistics["outputs(" + str(len(nyanMigen._get_outputs(ctx))) + ")"] = list(map(foo, nyanMigen._get_outputs(ctx)))
        self.statistics["generics(" + str(len(nyanMigen._get_generics(ctx))) + ")"] = nyanMigen._get_generics(ctx)
        self.statistics["domains(" + str(len(self.domains(ctx))) + ")"] = self.domains(ctx)

    def domains(self, ctx):
        dl = []
        for i in ctx:
            try:
                d = ctx[i]["domain"]
                if d:
                    if d not in dl:
                        dl.append(d)
            except:
                pass
        return dl

    def dump_statistics(self):
        s = self.statistics
        stat = ""
        for i in s:
            stat += i + ": " + str(s[i]) + "\n"
        with open(self.classname + ".stat", 'w') as f:
            f.write(stat)

converters = []
def converter(foo):
    converters.append(foo)
    return foo

class Failure(Exception):
    pass

class Context:
    def __init__(self, ctx):
        self.ctx = ctx

    @property
    def python_constants(self):
        ret = []
        for i in self.ctx:
            if nyanMigen._is_type(self.ctx, i, "py_const"):
                ret.append(i)
        return ret

class nyanMigen:
    def fix_case(s):
        return s.replace("with switch", "with m.Switch").replace("with case", "with m.Case").replace("with default", "with m.Default()")

    def propagate_constants(cls_src, ctx):
        c = Context(ctx)
        consts = c.python_constants
        for i in consts:
            nyanMigen._expand_const(cls_src, i, ctx[i]["args"])

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
        (code.body, ctx) = nyanMigen._convert_fsms(code.body)
        nyanMigen._add_module(code)
        (code.body, ctx) = nyanMigen._nyanify(code.body, ctx)
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
        code = ast.parse("def __init__(self" + args_string + "):\n    pass").body[0]
        body = generics
        for i in nyanMigen._get_ports(ctx):
            if nyanMigen._is_type(ctx, i, "Signal()"):
                add = ast.parse("self.a = Signal()").body[0]
            elif nyanMigen._is_type(ctx, i, "Array()"):
                add = ast.parse("self.a = Array()").body[0]
            else:
                raise Failure("unknown signal type for signal " + i)
            add.targets[0].attr = i
            if ctx[i]["args"]:
                add.value.args = ctx[i]["args"]
            body.append(add)
        code.body.extend(body)
        return code

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
                "        generics = json.load(read_file)\n"
            )
            args_str = ', '.join(map(add_generics2str, generics))
        str = (
            "def main():\n" +
            generics_str +
            "    top = " + cls.body[0].name + "(" + args_str + ")\n" +
            "    main(top, name = \"" + cls.body[0].name + "\", ports = top.ports())"
        )
        code = ast.parse(str)
        return code.body[0]

    def _convert_fsms(body, ctx = []):
        fsms = {}
        for i in body:
            try:
                nyanMigen._parse_fsm_init(i, fsms)
            except:
                pass
        for i in body:
            try:
                nyanMigen._parse_fsm_states(i, fsms)
            except:
                pass

        ins = []
        for i in range(len(body)):
            try:
                add = nyanMigen._fix_fsm_init(body[i], fsms)
                if add:
                    ins.append((i, add))
            except:
                pass

        inc = 0
        for i in ins:
            j = i[0] + inc
            del body[j]
            body[j:j] = i[1]
            inc += len(i[1])-1

        for i in range(len(body)):
            try:
                body[i] = nyanMigen._fix_fsm_states(body[i], fsms)
            except:
                pass
        return (body, ctx)

    def _parse_fsm_init(code, fsms):
        if nyanMigen._is_fsm_init(code):
            names = []
            for i in code.targets:
                if isinstance(i, Name):
                    if isinstance(i.ctx, Store):
                        names.append(i.id)
            kw = code.value.keywords

            to_del = []
            enc = None
            for i in range(len(kw)):
                if kw[i].arg == 'encoding':
                    to_del.append(i)
                    enc = kw[i].value.s
                if kw[i].arg == 'init':
                    to_del.append(i)
                    init = kw[i].value.s

            for i in sorted(to_del, reverse = True):
                del kw[i]

            found = False
            for i in kw:
                if i.arg == 'domain':
                    found = True

            if not found:
                pass
#                kw.append(ast.parse("a = Signal(domain = sync)").body[0].value.keywords[0])

            for i in names:
                if i in fsms:
                    print("warning: redefining fsm", i)
                fsms[i] = {}
                fsms[i]['kws'] = kw
                fsms[i]['encoding'] = enc
                fsms[i]['init'] = init

    def _parse_fsm_states(code, fsms):
        n = nyanMigen._is_fsm_switch(code, fsms)
        if n:
            fsms[n]['values'] = nyanMigen._parse_fsm_states_from_cases(code)
            add = nyanMigen._parse_fsm_states_from_assigns(code, n)
            fsms[n]['values'] = fsms[n]['values'] + list(set(add) - set(fsms[n]['values']))

    def _parse_fsm_states_from_cases(code):
        ret = []
        for i in code.body:
            ret.append(i.items[0].context_expr.args[0].s)
        return ret

    def _parse_fsm_states_from_assigns(code, n):
        ret = []
        for i in code.body:
            for j in i.body:
                try:
                    for k in j.targets:
                        try:
                            check = k.id
                        except:
                            try:
                                check = k.attr
                            except:
                                pass
                        try:
                            if check == n:
                                ret.append(j.value.s)
                                break
                        except:
                            pass
                except:
                    pass
        return ret

    def _fix_fsm_init(code, fsms):
        if nyanMigen._is_fsm_init(code):
            ret = []
            for i in code.targets:
                try:
                    enc = fsms[i.id]['encoding']
                    vs = fsms[i.id]['values']
                    width = nyanMigen._get_fsm_state_width(enc, vs)
                    add = ast.parse("a = Signal(" + str(width) + ")").body[0]
                    add.targets = [i]
                    add.value.keywords = fsms[i.id]['kws']
                    if 'init' in fsms[i.id]:
                        init = nyanMigen._gen_fsm_states_dic(enc, vs)[fsms[i.id]['init']]
                        initkw = ast.parse("a = b (reset = " + str(init.n) + ")").body[0].value.keywords[0]
                        add.value.keywords.append(initkw)
                    ret.append(add)
                except:
                    pass
            return ret

    def _gen_fsm_states_dic(enc, vs):
        ret = {}
        if enc == 'onehot':
            for i in range(len(vs)):
                s = vs[i] + " = " + str(pow(2, i))
                ret[vs[i]] = ast.parse(s).body[0].value
            return ret

    def _get_fsm_state_width(encoding, values):
        if encoding == 'onehot':
            return str(len(values))

    def _fix_fsm_states(code, fsms):
        n = nyanMigen._is_fsm_switch(code, fsms)
        if n:
            enc = fsms[n]['encoding']
            vs = fsms[n]['values']
            dic = nyanMigen._gen_fsm_states_dic(enc, vs)
            for i in code.body:
                i.items[0].context_expr.args[0] = dic[i.items[0].context_expr.args[0].s]

                for j in i.body:
                    try:
                        for k in j.targets:
                            try:
                                check = k.id
                            except:
                                try:
                                    check = k.attr
                                except:
                                    pass
                            try:
                                if check == n:
                                    j.value = dic[j.value.s]
                                    break
                            except:
                                pass
                    except:
                        pass
        return code

    def _is_fsm_init(code):
        is_assign = isinstance(code, Assign)
        is_fsm = (
            isinstance(code.value, Call) and
            isinstance(code.value.func, Name) and
            isinstance(code.value.func.ctx, Load) and
            code.value.func.id == 'Fsm'
        )
        return is_assign and is_fsm

    def _is_fsm_switch(code, fsms):
        if (isinstance(code, With) and
            len(code.items) == 1 and
            isinstance(code.items[0], withitem) and
            isinstance(code.items[0].context_expr, Call) and
            isinstance(code.items[0].context_expr.func, Attribute) and
            isinstance(code.items[0].context_expr.func.value, Name) and
            isinstance(code.items[0].context_expr.func.value.ctx, Load) and
            code.items[0].context_expr.func.attr == 'Switch' and
            len(code.items[0].context_expr.args) == 1 and
            len(code.items[0].context_expr.keywords) == 0 and
            isinstance(code.items[0].context_expr.args[0], Name) and
            isinstance(code.items[0].context_expr.args[0].ctx, Load)
        ):
            n = code.items[0].context_expr.args[0].id
            if n in fsms:
                return n

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
        if not isinstance(code, list):
            code = [code]
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
                    if ii != None:
                        i = ii
                        converted = True
                        break
                except Failure:
                    raise
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
            ret = []
            if (
                code.value.func.id == "Signal" and
                isinstance(code.value.func.ctx, Load)
            ):
                fp = False
                if len(code.value.keywords) > 0:
                    kw = code.value.keywords
                    for i in range(len(kw)):
                        if kw[i].arg == "port" and kw[i].value.value == True:
                            fp = True
                for i in code.targets:
                    if isinstance(i, Name):
                        if isinstance(i.ctx, Store):
                            nyanMigen._set_type(ctx, i.id, "Signal()", code.value.args)
                            ctx[i.id]["forced_port"] = fp
                            nyanMigen._parse_deps(code.value.args, ctx)

                            add = ast.parse("a = b").body[0]
                            add.value = code.value
                            add.targets = [i]
                            ret.append(add)
                return ret
            elif (
                code.value.func.id == "Array" and
                isinstance(code.value.func.ctx, Load) and
                len(code.value.keywords) == 0
            ):
                for i in code.targets:
                    if isinstance(i, Name):
                        if isinstance(i.ctx, Store):
                            nyanMigen._set_type(ctx, i.id, "Array()", code.value.args)
                            ctx[i.id]["forced_port"] = False

                            add = ast.parse("a = b").body[0]
                            add.value = code.value
                            add.targets = [i]
                            ret.append(add)
                return ret

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
    def _convert_assign(code, ctx):
        slice = None
        (domain, target, value, slice) = i = nyanMigen._parse_assign(code, None, [])
        if isinstance(code.value, IfExp):
            return nyanMigen._convert_IfExp(code, ctx)
        module = nyanMigen._get_module(ctx)
        if not module:
            return
        add = False
        if not nyanMigen._has_type(ctx, target):
            add = nyanMigen._try_to_inherite_type(i,  ctx)
        if nyanMigen._can_convert_assign(i, ctx):
            nyanMigen._parse_deps(value, ctx)
            if slice:
                nyanMigen._parse_deps(slice, ctx)
            nyanMigen._add_target(target, ctx, domain = domain)
            if add:
                return [add, nyanMigen._dump_assign(module, domain, target, value, slice)]
            else:
                return nyanMigen._dump_assign(module, domain, target, value, slice)
        else:
            raise Exception()

    def _convert_IfExp(code, ctx):
        src = ast.parse("if a:\n    b()\nelse:\n    c()").body[0]
        src.test = code.value.test
        t0 = ast.parse("a = 0").body[0]
        t1 = ast.parse("a = 0").body[0]
        t0.targets = code.targets
        t0.value = code.value.body
        t1.targets = code.targets
        t1.value = code.value.orelse
        src.body = [t0]
        src.orelse = [t1]
        (ret, _) = nyanMigen._nyanify(src, ctx)
        return ret

    def _get_module(ctx):
        for i in list(ctx.keys()):
            if nyanMigen._is_type(ctx, i, "Module()"):
                return i
        return None

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

    @converter
    def _convert_for(code, ctx):
        target = code.target
        if not isinstance(target, Name):
            ppa(code)
            raise Failure("only one loop var is supported in for loops")
        nyanMigen._parse_deps(code.iter, ctx)
        nyanMigen._set_to_initialized(code.target.id, ctx)
        (code.body, _) = nyanMigen._nyanify(code.body, ctx)
        return code

    @converter
    def _convert_simple_assignment(code, ctx):
        if(
            isinstance(code, Assign) and
            len(code.targets) == 1 and
            isinstance(code.targets[0], Name) and
            isinstance(code.targets[0].ctx, Store)
        ):
            deps = nyanMigen._parse_deps(code.value, ctx)
            nyanMigen._set_type(ctx, code.targets[0].id, "py_const")
            ctx[code.targets[0].id]["args"] = code.value
            return []

    @converter
    def _convert_generic_with(code, ctx):
        nyanMigen._parse_deps(code.items, ctx)
        (code.body, _) = nyanMigen._nyanify(code.body, ctx)
        return code

    @converter
    def _memory_converter(code, ctx):
        def parse_signal(code):
            if isinstance(code, Attribute):
                return (code.attr, code.value.id)
            elif isinstance(code, Name):
                return (code.id, "comb")
        if (
            code.value.func.id == "Memory" and
            isinstance(code.value.func.ctx, Load)
        ):
            kws = code.value.keywords
            d = {}
            # get args
            for i in kws:
                if i.arg == "width" or i.arg == "depth" or i.arg == "init":
                    nyanMigen._parse_deps(i.value, ctx)
                    d[i.arg] = unparse(i.value)[:-1]
                if i.arg == "we" or i.arg == "wa" or i.arg == "wd" or i.arg == "ra" or i.arg == "rd":
                    d[i.arg] = parse_signal(i.value)
                    if d[i.arg][0] not in ctx:
                        raise Exception("invalid memory connection")
                    if d[i.arg][0] not in ctx:
                        raise Failure("mem generation failed: signal " + i.value.id + " is not known")
            # set driver and is_driven flags
            for i in ["we", "wa", "wd", "ra"]:
                ctx[d[i][0]]["driver"] = True
            ctx[d["rd"][0]]["is_driven"] = True
            # generate nMigen Memory instance
            try:
                nyanMigen.mem_n += 1
            except:
                nyanMigen.mem_n = 0
            mem_n = nyanMigen.mem_n
            rdp = "rdport" + str(mem_n)
            wrp = "wrport" + str(mem_n)
            initstr = ""
            if "init" in d:
                initstr = ", init = " + d["init"]
            try:
                s = (
                    "mem = Memory(width = " + d["width"] + ", depth = " + d["depth"] + initstr + ")\n" +
                    "m.submodules." + rdp + " = " + rdp + " = mem.read_port(domain = \"" + d["rd"][1] + "\")\n" +
                    "m.submodules." + wrp + " = " + wrp + " = mem.write_port(domain = \"" + d["wd"][1] + "\")\n" +
                    "m.d.comb += [\n" +
                    "    " + rdp + ".addr.eq(" + d["ra"][0] + "),\n" +
                    "    " + d["rd"][0] + ".eq(" + rdp + ".data),\n" +
                    "    " + wrp + ".addr.eq(" + d["wa"][0] + "),\n" +
                    "    " + wrp + ".data.eq(" + d["wd"][0] + "),\n" +
                    "    " + wrp + ".en.eq(" + d["we"][0] + "),\n" +
                    "]"
                )
            except Exception as e:
                print(e)
            ret = ast.parse(s).body
            return ret

    def _add_target(target, ctx, domain = None):
        if target in ctx:
            if nyanMigen._is_signal(ctx, target):
                ctx[target]["is_driven"] = True
                if "domain" in ctx[target]:
                    if domain != ctx[target]["domain"]:
                        print("warning: redefining signal", target, "domain")
                ctx[target]["domain"] = domain

    def _parse_deps(value, ctx = {}, is_func = False):
        ret = []
        if isinstance(value, list):
            for i in value:
                ret.extend(nyanMigen._parse_deps(i, ctx))
        else:
            try:
                if isinstance(value.ctx, Load):
                    if not is_func:
                        if value.id not in ctx:
                            ctx[value.id] = {}
                        ctx[value.id]["driver"] = True
                        ret.append(value.id)
                        if nyanMigen._get_type(ctx, value.id) == None:
                            nyanMigen._set_type(ctx, value.id, "other")
            except:
                try:
                    for i in value.__dict__.keys():
                        ret.extend(nyanMigen._parse_deps(getattr(value, i), ctx, i == "func"))
                except Exception as e:
                    pass
        return ret

    def _expand_const(src, n, v):
        if isinstance(src, list):
            for i in range(len(src)):
                ret = nyanMigen._expand_const(src[i], n, v)
                if ret:
                    src[i] = ret
        else:
            try:
                if isinstance(src.ctx, Load) and src.id == n:
                    return v
            except:
                try:
                    for i in src.__dict__.keys():
                        ret = nyanMigen._expand_const(getattr(src, i), n, v)
                        if ret:
                            setattr(src, i, v)
                except Exception as e:
                    pass

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
                if ctx[i]["driver"] == False or ctx[i]["forced_port"]:
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

    def _has_type(ctx, n):
        if n in ctx:
            return "type" in ctx[n]

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

    def _can_convert_assign(arg, ctx):
        s = arg[1]
        if (nyanMigen._is_signal(ctx, s)):
            return True
        return False

    def _try_to_inherite_type(arg, ctx):
        v = arg[2]
        s = arg[1]
        slice = arg[3]
        is_assign = False
        is_slice = False
        try:
            n = v.id
            is_assign = True
            t = ctx[n]['type']
            args = ctx[n]['args']
        except:
            try:
                n = v.value.id
                is_slice = True
                t = ctx[n]['type']
                if t == 'Signal()':
                    t = 'Signal()'
                    args = []
                else:
                    print("send me this code")
                    exit(1)
            except:
                print("couldn't inherit" + str(s) + "from" + str(v.id))
                exit(1)

        ctx[s]["initialized"] = ctx[n]["initialized"]
        ctx[s]["forced_port"] = ctx[n]["forced_port"]
        nyanMigen._set_type(ctx, s, t, args)

        # TODO: merge with gen init code
        i = s
        if nyanMigen._is_type(ctx, i, "Signal()"):
            add = ast.parse("a = Signal()").body[0]
        elif nyanMigen._is_type(ctx, i, "Array()"):
            add = ast.parse("a = Array()").body[0]
        else:
            raise Failure("unknown signal type for signal " + i)
        add.targets[0].id = i
        if ctx[i]["args"]:
            add.value.args = ctx[i]["args"]
        return add

    def _is_type(ctx, m, t):
        if m in ctx:
            return nyanMigen._get_type(ctx, m) == t
        return False

    def _parse_assign(code, value = None, s = []):
        if isinstance(code, Assign):
            if len(code.targets) == 1:
                return nyanMigen._parse_assign(code.targets[0], code.value, [])
            raise Exception()
        elif isinstance(code, Subscript):
            s.append(code.slice)
            return nyanMigen._parse_assign(code.value, value, s)
        elif isinstance(code, Name):
            return (None, code.id, value, s)
        elif isinstance(code, Attribute):
            return (code.value.id, code.attr, value, s)

    def _dump_assign(m, d, t, v, s = None):
        if not d:
            d = "comb"
        ret = ast.parse("m.d.sync += t.eq(v)").body[0]
        ret.value.func.value.id = t
        ret.value.args = [v]
        if s:
            if isinstance(s, list):
                for i in reversed(range(len(s))):
                    ret.value.func.value = nyanMigen._slice(ret.value.func.value, s[i])
            else:
                ret.value.func.value = nyanMigen._slice(ret.value.func.value, s)
        ret.target.value.value.id = m
        ret.target.attr = d
        return ret

    def _slice(code, s):
        new = ast.parse("a = b[c]").body[0].value
        new.value = code
        new.slice = s
        return new

    @converter
    def _convert_branching(code, ctx):
        return None


