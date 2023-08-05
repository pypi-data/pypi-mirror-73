# BSD 3-Clause License; see https://github.com/scikit-hep/uproot4/blob/master/LICENSE

import ast

import numpy

import uproot4.compute


def _expression_to_node(expression, file_path, object_path):
    try:
        node = ast.parse(expression)
    except SyntaxError as err:
        raise SyntaxError(
            err.args[0] + "\nin file {0}\nin object {1}".format(file_path, object_path),
            err.args[1],
        )

    if len(node.body) != 1 or not isinstance(node.body[0], ast.Expr):
        raise SyntaxError(
            "expected a single expression\nin file {0}\nin object {1}".format(
                file_path, object_path
            )
        )

    return node


def _attribute_to_dotted_name(node):
    if isinstance(node, ast.Attribute):
        tmp = _attribute_to_dotted_name(node.value)
        if tmp is None:
            return None
        else:
            return tmp + "." + node.attr

    elif isinstance(node, ast.Name):
        return node.id

    else:
        return None


def _walk_ast_yield_symbols(node, keys, aliases, functions, getter):
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == getter
    ):
        if len(node.args) == 1 and isinstance(node.args[0], ast.Str):
            yield node.args[0].s
        else:
            raise TypeError(
                "expected a constant string as the only argument of {0}; "
                "found {1}".format(repr(getter), ast.dump(node.args))
            )

    elif isinstance(node, ast.Name):
        if node.id in keys or node.id in aliases:
            yield node.id
        elif node.id in functions or node.id == getter:
            pass
        else:
            raise KeyError(node.id)

    elif isinstance(node, ast.Attribute):
        name = _attribute_to_dotted_name(node)
        if name is None:
            for y in _walk_ast_yield_symbols(
                node.value, keys, aliases, functions, getter
            ):
                yield y
        elif name in keys or name in aliases:
            yield name
        else:
            # implicitly means functions and getter can't have dots in their names
            raise KeyError(name)

    elif isinstance(node, ast.AST):
        for field_name in node._fields:
            x = getattr(node, field_name)
            for y in _walk_ast_yield_symbols(x, keys, aliases, functions, getter):
                yield y

    elif isinstance(node, list):
        for x in node:
            for y in _walk_ast_yield_symbols(x, keys, aliases, functions, getter):
                yield y

    else:
        pass


def _ast_as_branch_expression(node, keys, aliases, functions, getter):
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == getter
        and len(node.args) == 1
        and isinstance(node.args[0], ast.Str)
    ):
        return node

    elif isinstance(node, ast.Name):
        if node.id in keys or node.id in aliases:
            return ast.parse("get({0})".format(repr(node.id))).body[0].value
        elif node.id in functions:
            return ast.parse("function[{0}]".format(repr(node.id))).body[0].value
        else:
            raise KeyError(node.id)

    elif isinstance(node, ast.Attribute):
        name = _attribute_to_dotted_name(node)
        if name is None:
            value = _ast_as_branch_expression(
                node.value, keys, aliases, functions, getter
            )
            new_node = ast.Attribute(value, node.attr, node.ctx)
            new_node.lineno = getattr(node, "lineno", 1)
            new_node.col_offset = getattr(node, "col_offset", 0)
            return new_node
        elif name in keys or name in aliases:
            return ast.parse("get({0})".format(repr(name))).body[0].value
        else:
            # implicitly means functions and getter can't have dots in their names
            raise KeyError(name)

    elif isinstance(node, ast.AST):
        args = []
        for field_name in node._fields:
            field_value = getattr(node, field_name)
            args.append(
                _ast_as_branch_expression(field_value, keys, aliases, functions, getter)
            )
        new_node = type(node)(*args)
        new_node.lineno = getattr(node, "lineno", 1)
        new_node.col_offset = getattr(node, "col_offset", 0)
        return new_node

    elif isinstance(node, list):
        return [
            _ast_as_branch_expression(x, keys, aliases, functions, getter) for x in node
        ]

    else:
        return node


def _expression_to_function(
    expression, keys, aliases, functions, getter, scope, file_path, object_path
):
    node = _expression_to_node(expression, file_path, object_path)
    try:
        expr = _ast_as_branch_expression(
            node.body[0].value, keys, aliases, functions, getter
        )
    except KeyError as err:
        raise uproot4.KeyInFileError(
            err.args[0],
            keys=sorted(keys) + list(aliases),
            file_path=file_path,
            object_path=object_path,
        )

    function = ast.parse("lambda: None").body[0].value
    function.body = expr
    expression = ast.Expression(function)
    expression.lineno = getattr(function, "lineno", 1)
    expression.col_offset = getattr(function, "col_offset", 0)
    return eval(compile(expression, "<dynamic>", "eval"), scope)


def _vectorized_erf(complement):
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911

    def erf(values):
        t = 1.0 / (numpy.absolute(values) * p + 1)
        y = 1.0 - ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * numpy.exp(
            numpy.negative(numpy.square(values))
        )
        if complement:
            return 1.0 - numpy.copysign(y, values)
        else:
            return numpy.copysign(y, values)

    return erf


def _vectorized_gamma(logarithm):
    cofs = (
        76.18009173,
        -86.50532033,
        24.01409822,
        -1.231739516e0,
        0.120858003e-2,
        -0.536382e-5,
    )
    stp = 2.50662827465

    def lgamma(values):
        x = values - 1.0
        tmp = x + 5.5
        with numpy.errstate(invalid="ignore"):
            tmp = (x + 0.5) * numpy.log(tmp) - tmp
        ser = 1.0
        with numpy.errstate(divide="ignore"):
            for cof in cofs:
                x = x + 1.0
                ser = ser + cof / x
        with numpy.errstate(invalid="ignore"):
            return tmp + numpy.log(stp * ser)

    if logarithm:
        return lgamma
    else:
        return lambda values: numpy.exp(lgamma(values))


_lgamma = _vectorized_gamma(True)


class ComputePython(uproot4.compute.Compute):
    default_functions = {
        "abs": numpy.absolute,
        "absolute": numpy.absolute,
        "acos": numpy.arccos,
        "arccos": numpy.arccos,
        "acosh": numpy.arccosh,
        "arccosh": numpy.arccosh,
        "asin": numpy.arcsin,
        "arcsin": numpy.arcsin,
        "asinh": numpy.arcsinh,
        "arcsinh": numpy.arcsinh,
        "atan": numpy.arctan,
        "atan2": numpy.arctan2,
        "arctan": numpy.arctan,
        "arctan2": numpy.arctan2,
        "atanh": numpy.arctanh,
        "arctanh": numpy.arctanh,
        "cbrt": numpy.cbrt,
        "ceil": numpy.ceil,
        "conj": numpy.conjugate,
        "conjugate": numpy.conjugate,
        "copysign": numpy.copysign,
        "cos": numpy.cos,
        "cosh": numpy.cosh,
        "erf": _vectorized_erf(False),
        "erfc": _vectorized_erf(True),
        "exp": numpy.exp,
        "exp2": numpy.exp2,
        "expm1": numpy.expm1,
        "fabs": numpy.fabs,
        "factorial": lambda x: numpy.round(numpy.exp(_lgamma(numpy.round(x) + 1))),
        "floor": numpy.floor,
        "fmax": numpy.fmax,
        "fmin": numpy.fmin,
        "gamma": _vectorized_gamma(False),
        "hypot": numpy.hypot,
        "imag": numpy.imag,
        "isfinite": numpy.isfinite,
        "isinf": numpy.isinf,
        "isnan": numpy.isnan,
        "lgamma": _lgamma,
        "log": numpy.log,
        "log10": numpy.log10,
        "log1p": numpy.log1p,
        "log2": numpy.log2,
        "logical_and": numpy.logical_and,
        "logical_or": numpy.logical_or,
        "neg": numpy.negative,
        "nextafter": numpy.nextafter,
        "real": numpy.real,
        "rint": numpy.rint,
        "round": numpy.round,
        "signbit": numpy.signbit,
        "sin": numpy.sin,
        "sinh": numpy.sinh,
        "sqrt": numpy.sqrt,
        "tan": numpy.tan,
        "tanh": numpy.tanh,
        "tgamma": lambda x: numpy.exp(_lgamma(x)),
        "trunc": numpy.trunc,
        "where": numpy.where,
    }

    def __init__(self, functions=None, getter="get"):
        if functions is None:
            self._functions = self.default_functions
        else:
            self._functions = dict(functions)
        self._getter = getter

    @property
    def functions(self):
        return self._functions

    @property
    def getter(self):
        return self._getter

    def free_symbols(self, expression, keys, aliases, file_path, object_path):
        node = _expression_to_node(expression, file_path, object_path)
        try:
            return list(
                _walk_ast_yield_symbols(
                    node, keys, aliases, self._functions, self._getter
                )
            )
        except KeyError as err:
            raise uproot4.KeyInFileError(
                err.args[0], file_path, object_path=object_path
            )

    def compute_expressions(
        self, arrays, expression_context, keys, aliases, file_path, object_path
    ):
        values = {}

        def getter(name):
            if name not in values:
                values[name] = _expression_to_function(
                    aliases[name],
                    keys,
                    aliases,
                    self._functions,
                    self._getter,
                    scope,
                    file_path,
                    object_path,
                )()
            return values[name]

        scope = {self._getter: getter, "function": self._functions}
        for expression, context in expression_context:
            branch = context.get("branch")
            if branch is not None:
                values[expression] = arrays[id(branch)]

        output = {}
        for expression, context in expression_context:
            if context["is_primary"] and not context["is_cut"]:
                output[expression] = _expression_to_function(
                    expression,
                    keys,
                    aliases,
                    self._functions,
                    self._getter,
                    scope,
                    file_path,
                    object_path,
                )()

        cut = None
        for expression, context in expression_context:
            if context["is_primary"] and context["is_cut"]:
                cut = _expression_to_function(
                    expression,
                    keys,
                    aliases,
                    self._functions,
                    self._getter,
                    scope,
                    file_path,
                    object_path,
                )()
                break

        if cut is not None:
            cut = cut != 0
            for name in output:
                output[name] = output[name][cut]

        return output
