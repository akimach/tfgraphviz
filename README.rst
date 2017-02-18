
tfgraphviz
================

A simple graphviz wrapper to visualize a graph like TensorBoard

tfgraphviz is a module to create a TensorBoard-ish graph in the DOT language of the Graphviz. tfgraphviz provides a visualization of tensorflow graph on Jupyter Notebook without TensorBoard.

Links
-----

- GitHub: http://github.com/akimach/tfgraphviz
- PyPI: https://pypi.python.org/pypi/tfgraphviz

Installation
------------

Use pip to install:

.. code-block:: bash

    $ pip install tfgraphviz

The only dependency is  Graphviz.

Quickstart
----------

.. code-block:: python

    import tensorflow as tf
    import tfgraphviz as tfg
    a = tf.constant(1, name="a")
    b = tf.constant(2, name="b")
    c = tf.add(a, b, name="add")
    g = tfg.board(tf.get_default_graph())
    g.view()

.. image:: https://raw.githubusercontent.com/akimach/tfgraphviz/master/img/graph.jpg
    :align: center

License
-------

This package is distributed under the MIT license.
