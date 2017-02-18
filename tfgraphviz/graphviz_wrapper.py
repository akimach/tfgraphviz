# coding: utf-8
import re
import uuid
import graphviz as gv


graph_pref = {
    'fontcolor': '#414141',
    'style': 'rounded',
}

name_scope_graph_pref = {
    'bgcolor': '#eeeeee',
    'color': '#aaaaaa',
    'penwidth': '2',
}

non_name_scope_graph_pref = {
    'fillcolor':  'white',
    'color': 'white',
}

node_pref = {
    'style': 'filled',
    'fillcolor': 'white',
    'color': '#aaaaaa',
    'penwidth': '2',
    'fontcolor': '#414141',
}

edge_pref = {
    'color': '#aaaaaa',
    'arrowsize': '1.2',
    'penwidth': '2.5',
}


def tf_digraph(name=None, name_scope=None, style=True):
    g = gv.Digraph(name=name)
    if name_scope:
        g.graph_attr['label'] = name_scope
    if style is False: return g

    if name_scope:
        g.graph_attr.update(name_scope_graph_pref)
    else:
        g.graph_attr.update(non_name_scope_graph_pref)
    g.graph_attr.update(graph_pref)
    g.node_attr.update(node_pref)
    g.edge_attr.update(edge_pref)
    return g


def nested_dict(dict_, keys, val):
    cloned = dict_.copy()
    if len(keys) == 1:
        cloned[keys[0]] = val
        return cloned
    dd = cloned[keys[0]]
    for k in keys[1:len(keys)-1]:
        dd = dd[k]
    last_key = keys[len(keys)-1]
    dd[last_key] = val
    return cloned


def node_abs_paths(op):
    node_names = op.name.split('/')
    return ['/'.join(node_names[0:i+1]) for i in range(len(node_names))]


def node_table(graph, depth=1):
    table = {}
    max_depth = depth
    ops = graph.get_operations()
    for depth_i in range(max_depth):
        for op in ops:
            abs_paths = node_abs_paths(op)
            if depth_i >= len(abs_paths): continue
            ps = abs_paths[:depth_i+1]
            if len(ps) == 1:
                key = '/'.join(abs_paths[0:depth_i+1])
                if not key in table: table[key] = {}
            else:
                table = nested_dict(table, ps, {})
    return table


def node_input_table(graph, depth=1):
    table = {}
    inpt_op_table = {}
    for op in graph.get_operations():
        op_name = op.name.split('/')[0:depth]
        opn = '/'.join(op_name)
        if not opn in inpt_op_table:
            inpt_op_table[opn] = []
        inpt_op_list = ['/'.join(inpt_op.split('/')[0:depth]) for inpt_op in op.node_def.input]
        inpt_op_table[opn].append(inpt_op_list)
    for opn in inpt_op_table.keys():
        t_l = []
        for ll in inpt_op_table[opn]:
            list.extend(t_l, ll)
        table[opn] = list(set(t_l))
    return table

# cluster index of subgraph
CLUSTER_INDEX = 0


def add_nodes(node_table, name=None, name_scope=None, style=True):
    global CLUSTER_INDEX
    if name:
        g = tf_digraph(name=name, name_scope=name_scope, style=style)
    else:
        g = tf_digraph(name=str(uuid.uuid4().get_hex().upper()[0:6]), name_scope=name_scope, style=style)
    graphs = []
    for key, value in node_table.items():
        if len(value) > 0:
            sg = add_nodes(value, name='cluster_%i' % CLUSTER_INDEX, name_scope=key.split('/')[-1], style=style)
            sg.node(key, key.split('/')[-1])
            CLUSTER_INDEX += 1
            graphs.append(sg)
        else:
            g.node(key, key.split('/')[-1])
    for tg in graphs:
        g.subgraph(tg)
    return g


def add_edges(node_inpt_table, g):
    for node, node_inputs in node_inpt_table.items():
        if re.match(r"\^", node): continue
        for ni in node_inputs:
            if ni == node: continue
            if re.match(r"\^", ni): continue
            g.edge(ni, node)
    return g


def board(tfgraph, depth=1, name='G', style=True):
    global CLUSTER_INDEX
    CLUSTER_INDEX = 0
    _node_table = node_table(tfgraph, depth=depth)
    _node_inpt_table = node_input_table(tfgraph, depth=depth)
    g = add_nodes(_node_table, name=name, style=style)
    g = add_edges(_node_inpt_table, g)
    return g
