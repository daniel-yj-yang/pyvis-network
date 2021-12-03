# -*- coding: utf-8 -*-

# Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
# License: BSD-3-Clause


from typing import Union
from pathlib import Path
import pandas as pd
import webbrowser
import sys


class network(object):
    def __init__(self, title="Interactive Network Analysis", width: str = '1024px', height: str = '768px', *args, **kwargs) -> None:
      super().__init__(*args, **kwargs)
      self.title = title
      self.width = width
      self.height = height
      self.nodes_df = pd.DataFrame(columns=['label'])
      self.edges_df = pd.DataFrame(columns=['from','to'])

    def add_df(self, nodes_df: pd.DataFrame, edges_df: pd.DataFrame) -> None:
      self.nodes_df = nodes_df.copy()
      self.edges_df = edges_df.copy()
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
      for idx, row in self.nodes_df.iterrows():
        label_to_id_hashmap[row['label']] = idx+1
        id_part = f"id: {idx+1}, "
        label_part = f"label: \"{row['label']}\""
        self.html += f"""
    {{ {id_part}{label_part} }},"""
      self.html += f"""
  ]);
  // create an array with edges
  var edges = new vis.DataSet(["""
      for idx, row in self.edges_df.iterrows():
        from_part = f"from: {label_to_id_hashmap[row['from']]}, "
        to_part = f"to: {label_to_id_hashmap[row['to']]}"
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



