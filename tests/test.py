# -*- coding: utf-8 -*-

# Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
# License: BSD-3-Clause

from pyvis_network import network, dataset

nodes_df, edges_df = dataset().load_as_df('Example1')
network().add_df(nodes_df=nodes_df, edges_df=edges_df).write_html('Example1.html')
