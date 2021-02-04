# coding: utf-8
import re
import uuid
import graphviz as gv

from collections import defaultdict
from .graphviz_style import *


# index of subgraph
CLUSTER_INDEX = 0
ADD_DIGRAPH_FUNC = None
ADD_DIGRAPH_NODE_FUNC = None
ADD_DIGRAPH_EDGE_FUNC = None

def add_digraph(name=None, name_scope=None, style=True):
    """
    Return graphviz.dot.Digraph with TensorBoard-like style.
    @param  name
    @param  name_scope
    @param  style
    @return graphviz.dot.Digraph object
    """
    digraph = gv.Digraph(name=name)
    if name_scope:
        digraph.graph_attr['label'] = name_scope
        digraph.graph_attr['tooltip'] = name_scope

    if style is False: return digraph

    if name_scope:
        digraph.graph_attr.update(name_scope_graph_pref)
    else:
        digraph.graph_attr.update(non_name_scope_graph_pref)
    digraph.graph_attr.update(graph_pref)
    digraph.node_attr.update(node_pref)
    digraph.edge_attr.update(edge_pref)
    return digraph


def add_digraph_node(digraph, name, op, attributes=None):
    """
    Adds a node to digraph.
    @param  digraph
    @param  name
    @param  op
    @param  attributes
    """
    label = name.split('/')[-1]
    tooltip = name
    # For possible attribute values see:
    # https://graphviz.org/doc/info/attrs.html
    if attributes is None:
        attributes = []
    if op is not None:
        tooltip += ':' + op.type
        if 'PartitionedCall' in op.type:
            try:
                label = '{}\n{}:{}'.format(label, 'f', op.get_attr('f').name)
            except ValueError:
                pass
            # For example:
            # attributes.append(('fillcolor', 'green'))
    digraph.node(name, label=label, tooltip=tooltip, _attributes=attributes)


def add_digraph_edge(digraph, from_node, to_node, label=None, attributes=None):
    """
    Adds an edge to digraph.
    @param  digraph
    @param  from_node
    @param  to_node
    @param  label
    @param  attributes
    """
    if attributes is None:
        attributes = []
    digraph.edge(from_node, to_node, label=label, _attributes=attributes)


def nested_dict(dict_, keys, val):
    """
    Assign value to dictionary.
    @param  dict_
    @param  keys
    @param  val
    @return dictionary
    """
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


def node_abs_paths(node):
    """
    Return absolute node path name.
    @param  node
    @return string
    """
    node_names = node.name.split('/')
    return ['/'.join(node_names[0:i+1]) for i in range(len(node_names))]


def node_table(tfgraph, depth=1, name_regex=''):
    """
    Return dictionary of node.
    @param  tfgraph
    @param  depth
    @param  name_regex
    @return dictionary
    """
    table = {}
    ops_table = {}
    max_depth = depth
    ops = tfgraph.get_operations()
    for depth_i in range(max_depth):
        for op in ops:
            abs_paths = node_abs_paths(op)
            if depth_i >= len(abs_paths): continue
            if name_regex and not re.match(name_regex, op.name): continue
            ops_table[op.name] = op
            ps = abs_paths[:depth_i+1]
            if len(ps) == 1:
                key = '/'.join(abs_paths[0:depth_i+1])
                if not key in table: table[key] = {}
            else:
                table = nested_dict(table, ps, {})
    return table, ops_table


def node_shape(tfnode, depth=1):
    """
    Return node and the children.
    @param  tfnode
    @param  depth
    @return string, list
    """
    outpt_name = tfnode.name
    if len(outpt_name.split('/')) < depth: return None
    on = '/'.join(outpt_name.split('/')[:depth]) # output node
    result = re.match(r"(.*):\d*$", on)
    if not result: return None
    on = result.groups()[0]
    if tfnode.shape.ndims is None:
        return on, []
    else:
        return on, tfnode.shape.as_list()


def node_input_table(tfgraph, depth=1, name_regex=''):
    """
    Return table of operations
    @param  tfgraph
    @param  depth
    @param  name_regex
    @return dictionary, table of operations
    """
    table = {}
    inpt_op_table = {}
    inpt_op_shape_table = {}
    for op in tfgraph.get_operations():
        if name_regex and not re.match(name_regex, op.name): continue
        op_name = op.name.split('/')[0:depth]
        opn = '/'.join(op_name)
        if not opn in inpt_op_table:
            inpt_op_table[opn] = []
        inpt_op_list = ['/'.join(inpt_op.split('/')[0:depth]) \
            for inpt_op in op.node_def.input if not name_regex or re.match(name_regex, inpt_op)]
        inpt_op_table[opn].append(inpt_op_list)
        for output in op.outputs:
            for i in range(depth):
                shape = node_shape(output, depth=i+1)
                if shape: inpt_op_shape_table[shape[0]] = shape[1]
    for opn in inpt_op_table.keys():
        t_l = []
        for ll in inpt_op_table[opn]:
            list.extend(t_l, ll)
        table[opn] = list(set(t_l))
    return table, inpt_op_shape_table


def add_nodes(node_table, ops_table, name=None, name_scope=None, style=True):
    """
    Add TensorFlow graph's nodes to graphviz.dot.Digraph.
    @param  node_table
    @param  ops_table
    @param  name
    @param  name_scope
    @param  style
    @return graphviz.dot.Digraph object
    """
    global CLUSTER_INDEX
    global ADD_DIGRAPH_FUNC
    global ADD_DIGRAPH_NODE_FUNC
    if name:
        digraph = ADD_DIGRAPH_FUNC(name=name, name_scope=name_scope, style=style)
    else:
        digraph = ADD_DIGRAPH_FUNC(name=str(uuid.uuid4().get_hex().upper()[0:6]), name_scope=name_scope, style=style)
    graphs = []
    for key, value in node_table.items():
        if len(value) > 0:
            sg = add_nodes(value, ops_table, name='cluster_%i' % CLUSTER_INDEX, name_scope=key.split('/')[-1], style=style)
            op = ops_table.get(key, None)
            ADD_DIGRAPH_NODE_FUNC(sg, key, op)
            CLUSTER_INDEX += 1
            graphs.append(sg)
        else:
            op = ops_table.get(key, None)
            label = key.split('/')[-1]
            ADD_DIGRAPH_NODE_FUNC(digraph, key, op)

    for tg in graphs:
        digraph.subgraph(tg)
    return digraph


def edge_label(shape):
    """
    Returen texts of graph's edges.
    @param  shape
    @return
    """
    if len(shape) == 0: return ''
    if shape[0] is None: label = "?"
    else: label = "%i" % shape[0]
    for s in shape[1:]:
        if s is None: label += "×?"
        else: label += u"×%i" % s
    return label


def add_edges(digraph, node_inpt_table, node_inpt_shape_table):
    """
    Add TensorFlow graph's edges to graphviz.dot.Digraph.
    @param  dirgraph
    @param  node_inpt_table
    @param  node_inpt_shape_table
    @return  graphviz.dot.Digraph
    """
    global ADD_DIGRAPH_EDGE_FUNC
    for node, node_inputs in node_inpt_table.items():
        if re.match(r"\^", node): continue
        for ni in node_inputs:
            if ni == node: continue
            if re.match(r"\^", ni): continue
            if not ni in node_inpt_shape_table:
                ADD_DIGRAPH_EDGE_FUNC(digraph, ni, node)
            else:
                shape = node_inpt_shape_table[ni]
                ADD_DIGRAPH_EDGE_FUNC(digraph, ni, node, label=edge_label(shape))
    return digraph


def board(tfgraph,
          depth=1,
          name='G',
          style=True,
          name_regex='',
          add_digraph_func=None,
          add_digraph_node_func=None,
          add_digraph_edge_func=None
         ):
    """
    Return graphviz.dot.Digraph object with TensorFlow's Graphs.
    @param  depth
    @param  name
    @param  style
    @param  name_regex
    @return  graphviz.dot.Digraph
    """
    global ADD_DIGRAPH_FUNC
    global ADD_DIGRAPH_NODE_FUNC
    global ADD_DIGRAPH_EDGE_FUNC
    global CLUSTER_INDEX
    CLUSTER_INDEX = 0
    ADD_DIGRAPH_FUNC = add_digraph_func if add_digraph_func is not None else add_digraph
    ADD_DIGRAPH_NODE_FUNC = add_digraph_node_func if add_digraph_node_func is not None else add_digraph_node
    ADD_DIGRAPH_EDGE_FUNC = add_digraph_edge_func if add_digraph_edge_func is not None else add_digraph_edge

    _node_table, _ops_table = node_table(tfgraph, depth=depth, name_regex=name_regex)
    _node_inpt_table, _node_inpt_shape_table = node_input_table(tfgraph, depth=depth, name_regex=name_regex)
    digraph = add_nodes(_node_table, _ops_table, name=name, style=style)
    digraph = add_edges(digraph, _node_inpt_table, _node_inpt_shape_table)
    return digraph
