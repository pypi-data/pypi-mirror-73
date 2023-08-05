import ast

import astcheck
import astsearch

from ..code import Parameter

__all__ = ['extract_definitions', 'build_definitions']

def check_fillable_node(node, path):
    if isinstance(node, (ast.Num, ast.Str)):
        return
    elif isinstance(node, ast.NameConstant) and (node.value in (True, False)):
        return
    elif isinstance(node, ast.List):
        for n in node.elts:
            check_fillable_node(n, path)
        return
    elif isinstance(node, ast.Dict):
        for n in node.keys:
            check_fillable_node(n, path)
        for n in node.values:
            check_fillable_node(n, path)
        return
    
    raise astcheck.ASTMismatch(path, node, 'number, string or boolean')

definition_pattern = ast.Assign(targets=[ast.Name()], value=check_fillable_node)

def type_and_value(node):
    if isinstance(node, ast.Num):
        # int or float
        return type(node.n), node.n
    elif isinstance(node, ast.Str):
        return str, node.s
    elif isinstance(node, ast.NameConstant) and (node.value in (True, False)):
        return (bool, node.value)
    elif isinstance(node, ast.List):
        return (list, [type_and_value(n)[1] for n in node.elts])
    elif isinstance(node, ast.Dict):
        return (dict, {type_and_value(node.keys[i])[1]: type_and_value(node.values[i])[1] for i in range(len(node.keys))})

    raise NotImplementedError()

def extract_definitions(cell):
    cell_ast = ast.parse(cell)
    for assign in astsearch.ASTPatternFinder(definition_pattern).scan_ast(cell_ast):
        yield Parameter(assign.targets[0].id, *type_and_value(assign.value))

def build_definitions(inputs):
    return "\n".join("{0.name} = {0.value!r}".format(i) for i in inputs)
