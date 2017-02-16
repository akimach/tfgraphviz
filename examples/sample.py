#!/usr/bin/env python
import tensorflow as tf
import tfgraphviz as tfg

a = tf.constant(1, name="a")
b = tf.constant(2, name="b")
c = tf.add(a, b, name="add")
g = tfg.board(tf.get_default_graph())
g.view()