
tfgraphviz
================

.. image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat 

tfgraphviz is a module to visualize a TensorFlow's data flow graph like TensorBoard using Graphviz. tfgraphviz enables to provide a visualization of tensorflow graph on Jupyter Notebook without TensorBoard.

Links
-----

- GitHub: http://github.com/akimach/tfgraphviz
- PyPI: https://pypi.python.org/pypi/tfgraphviz
- Jupyter Notebook: https://nbviewer.jupyter.org/github/akimach/tfgraphviz/blob/master/examples/jupyter_sample.ipynb

Installation
------------

Use pip to install:

.. code-block:: bash

    $ pip install graphviz
    $ pip install tfgraphviz

The only dependency is  Graphviz.

macOS:

.. code-block:: bash

    $ brew install graphviz

Ubuntu:

.. code-block:: bash

    $ apt-get install graphviz

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

This package is distributed under the `MIT license <https://raw.githubusercontent.com/akimach/tfgraphviz/master/LICENSE>`_.

Author
-------

`Akimasa KIMURA <https://github.com/akimach>`_
