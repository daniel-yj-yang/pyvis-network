.. -*- mode: rst -*-

|BuildTest|_ |PyPi|_ |License|_ |Downloads|_ |PythonVersion|_

.. |BuildTest| image:: https://travis-ci.com/daniel-yj-yang/pyvis-network.svg?branch=main
.. _BuildTest: https://app.travis-ci.com/github/daniel-yj-yang/pyvis-network

.. |PythonVersion| image:: https://img.shields.io/badge/python-3.8%20%7C%203.9-blue
.. _PythonVersion: https://img.shields.io/badge/python-3.8%20%7C%203.9-blue

.. |PyPi| image:: https://img.shields.io/pypi/v/pyvis-network
.. _PyPi: https://pypi.python.org/pypi/pyvis-network

.. |Downloads| image:: https://pepy.tech/badge/pyvis-network
.. _Downloads: https://pepy.tech/project/pyvis-network

.. |License| image:: https://img.shields.io/pypi/l/pyvis-network
.. _License: https://pypi.python.org/pypi/pyvis-network


===================================
Interactive Network Visualizations
===================================

This tool leverages the amazing vis-network library (https://visjs.github.io/vis-network/docs/network/) to provide interactive visualizations.


Installation
------------

.. code-block::

   pip install pyvis-network


Sample Usage
------------

>>> from pyvis_network import network, dataset
>>> nodes_df, edges_df = dataset().load_as_df("Example1")
>>> graph1 = network(title="Example1").add_df(nodes_df=nodes_df,edges_df=edges_df)
>>> graph1.show("example1.html")
>>> graph2 = graph1.clone_graph()
>>> graph2.show("example1_cloned.html")

>>> from pyvis_network import network, dataset
>>> nodes_df, edges_df = dataset().load_as_df("Machine_Learning")
>>> network(title="Machine Learning").add_df(nodes_df=nodes_df,edges_df=edges_df).show("ml.html")


Sample Screenshot
-----------------
Example1

|image1|


.. |image1| image:: https://github.com/daniel-yj-yang/pyvis-network/raw/main/pyvis_network/examples/images/Example1.png



Other Similar Tools
-------------------

https://pyvis.readthedocs.io/en/latest/
https://pyviz.org/
