# -*- coding: utf-8 -*-

# Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
# License: BSD-3-Clause


from typing import Union, List
from pathlib import Path
import pandas as pd
import webbrowser


class network(object):
    def __init__(self, title="Interactive Network Analysis", width: str = '1024px', height: str = '768px', *args, **kwargs) -> None:
      super().__init__(*args, **kwargs)
      self.title = title
      self.width = width
      self.height = height
      self.nodes_hashmap = dict()

    def add_node(self, node_id: Union[float, int, str] = None, shape: str = 'circle'):
      if node_id not in self.nodes_hashmap:
        self.nodes_hashmap[node_id] = {'shape': shape, 'to': dict()}

    def add_edge(self, from_node_id: Union[float, int, str] = None, to_node_id: Union[float, int, str] = None):
      if to_node_id not in self.nodes_hashmap[from_node_id]['to']:
        self.nodes_hashmap[from_node_id]['to'][to_node_id] = {'weight': 1.0,}

    def add_df(self, nodes_df: pd.DataFrame, edges_df: pd.DataFrame) -> None:
      for idx, row in nodes_df.iterrows():
        self.add_node(node_id = row['label'])
      for idx, row in edges_df.iterrows():
        self.add_edge(from_node_id=row['from'], to_node_id=row['to'])
      return self

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
      for idx, node_id in enumerate(self.nodes_hashmap):
        label_to_id_hashmap[node_id] = idx+1
        id_part = f"id: {idx+1}, "
        label_part = f"label: \"{node_id}\""
        self.html += f"""
    {{ {id_part}{label_part} }},"""
      self.html += f"""
  ]);
  // create an array with edges
  var edges = new vis.DataSet(["""
      for from_node_id in self.nodes_hashmap:
        from_part = f"from: {label_to_id_hashmap[from_node_id]}, "
        for to_node_id in self.nodes_hashmap[from_node_id]['to']:
          to_part = f"to: {label_to_id_hashmap[to_node_id]}"
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



