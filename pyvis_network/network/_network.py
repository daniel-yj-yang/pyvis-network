# -*- coding: utf-8 -*-

# Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
# License: BSD-3-Clause


from typing import Union
from pathlib import Path
import pandas as pd
import webbrowser


class Edge(dict):
  def __init__(self, source_node: 'Node' = None, to_node: 'Node' = None, weight: float = 1.0, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self['source_node'] = source_node
    self['to_node'] = to_node
    self['weight'] = weight


class Node(dict):
  def __init__(self, label: str = '', shape: str = 'circle', *args, **kwargs):
    super().__init__(*args, **kwargs)
    self['label'] = label
    self['shape'] = shape
    self['edges'] = dict() # key: to_Node['label'], value: Edge
  
  def add_edge(self, to_node: 'Node' = None):
    if to_node['label'] not in self['edges']:
      self['edges'][to_node['label']] = Edge(source_node=self, to_node=to_node)


class network(object):
    def __init__(self, title="Interactive Network Analysis", width: str = '1024px', height: str = '768px', *args, **kwargs) -> None:
      super().__init__(*args, **kwargs)
      self.title = title
      self.width = width
      self.height = height
      self.nodes = dict() # key: label, value = Node

    def add_node(self, label: Union[float, int, str] = None):
      if label not in self.nodes:
        self.nodes[label] = Node(label = label)

    def add_edge(self, source_label: Union[float, int, str] = None, to_label: Union[float, int, str] = None):
      if source_label in self.nodes and to_label in self.nodes:
        self.nodes[source_label].add_edge(to_node = self.nodes[to_label])
      else:
        print('Error: the nodes are not created yet')

    def add_df(self, nodes_df: pd.DataFrame, edges_df: pd.DataFrame) -> None:
      for idx, row in nodes_df.iterrows():
        self.add_node(label = row['label'])
      for idx, row in edges_df.iterrows():
        self.add_edge(source_label=row['source'], to_label=row['to'])
      return self

    def clone_graph(self):
      new_graph = network()
      original_to_clone_mapping = {} # key: id() of original node, value: cloned node
      def clone_node(node: 'Node' = None) -> 'Node':
        nonlocal original_to_clone_mapping, new_graph
        if not node:
          return None
        if id(node) in original_to_clone_mapping:
          return original_to_clone_mapping[id(node)]
        cloned_node = Node(label=node['label'], shape=node['shape'])
        new_graph.nodes[cloned_node['label']] = cloned_node
        original_to_clone_mapping[id(node)] = cloned_node
        if node['edges']:
          for this_to_node_label in node['edges']:
            cloned_node.add_edge(to_node=clone_node(self.nodes[this_to_node_label]))
        return cloned_node
      if self.nodes:
        clone_node(list(self.nodes.values())[0])
      return new_graph

    def _generate_html(self) -> None:
      """
      see also: https://visjs.org/
      """
      self.html = f"""<!DOCTYPE HTML>
<html>
<head>
  <title>{self.title}</title>
  <style type="text/css">
    body, html {{
      font-family: sans-serif;
    }}
    #mynetwork {{
        width: {self.width};
        height: {self.height};
        border: 1px solid lightgray;
    }}
  </style>
<script type="text/javascript" src="https://unpkg.com/vis-data@7.1.2/peer/umd/vis-data.min.js"></script>
<script type="text/javascript" src="https://unpkg.com/vis-network@9.1.0/peer/umd/vis-network.min.js"></script>
<link rel="stylesheet" type="text/css" href="https://unpkg.com/vis-network/styles/vis-network.min.css" />
<!-- Include other packages like Vis Timeline or Vis Graph3D here. -->
<div id="mynetwork"></div>
<script type="text/javascript">
  // create an array with nodes
  var nodes = new vis.DataSet(["""
      label_to_id_hashmap = {}
      for idx, node_label in enumerate(self.nodes):
        label_to_id_hashmap[node_label] = idx+1
        id_part = f"id: {idx+1}, "
        label_part = f"label: \"{node_label}\""
        self.html += f"""
    {{ {id_part}{label_part} }},"""
      self.html += f"""
  ]);
  // create an array with edges
  var edges = new vis.DataSet(["""
      for source_label in self.nodes:
        from_part = f"from: {label_to_id_hashmap[source_label]}, "
        for to_node_label in self.nodes[source_label]['edges']:
          to_part = f"to: {label_to_id_hashmap[to_node_label]}"
          self.html += f"""
    {{ {from_part}{to_part} }},"""
      self.html += f"""
  ]);
  // create a network
  var container = document.getElementById("mynetwork");
  var data = {{
    nodes: nodes,
    edges: edges
  }};
  var options = {{}};
  var network = new vis.Network(container, data, options);
</script>
</body>
</html>"""

    def write_html(self, filename: Union[Path, str]) -> None:
      self._generate_html()
      output_path = filename
      if not isinstance(output_path, Path):
        output_path = Path(output_path)
      output_path.write_text(self.html)

    def show(self, filename: Union[Path, str]) -> None:
      output_path = filename
      if not isinstance(output_path, Path):
        output_path = Path(output_path)
      self.write_html(filename=output_path)
      webbrowser.open(output_path.resolve().as_uri(), new = 2)



