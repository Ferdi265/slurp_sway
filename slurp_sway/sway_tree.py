from typing import Any, Generator
from dataclasses import dataclass
from subprocess import check_output
import json
from copy import copy
from .box import Box

@dataclass
class Region:
    output: str
    path: str
    name: str
    toplevel_handle: str | None
    box: Box

def get_tree_json() -> dict[str, Any]:
    return json.loads(check_output(["swaymsg", "-t", "get_tree"]))

def find_tree_regions(node: dict[str, Any], with_scratchpad: bool = False, path: str = "root", output: str | None = None) -> Generator[Region]:
    if node["type"] == "output" and node["name"] == "__i3" and not with_scratchpad:
        return

    if node["type"] == "output":
        assert output is None, f"found another output node within output {output}: {node}"
        output = node["name"]
        yield Region(output, path, output, None, Box.from_json(node["rect"]))

    if "nodes" in node:
        for i, inner_node in enumerate(node["nodes"]):
            yield from find_tree_regions(inner_node, with_scratchpad, f"{path}.{i}", output)

    if "floating_nodes" in node:
        for i, inner_node in enumerate(node["floating_nodes"]):
            yield from find_tree_regions(inner_node, with_scratchpad, f"{path}.f{i}", output)

    if "foreign_toplevel_identifier" in node:
        yield Region(output, path, node["name"], node["foreign_toplevel_identifier"], Box.from_json(node["rect"]))

def find_tree_boxes(tree: dict[str, Any], with_scratchpad: bool = False, with_outputs: bool = True, with_toplevels: bool = True) -> list[Box]:
    boxes = []

    for region in find_tree_regions(tree, with_scratchpad=with_scratchpad):
        region_box = copy(region.box)
        if with_outputs and region.toplevel_handle is None:
            region_box.label = region.name
            region_box.kind = "output"
            boxes.append(region_box)
        elif with_toplevels and region.toplevel_handle is not None:
            region_box.label = region.toplevel_handle
            region_box.kind = "toplevel"
            boxes.append(region_box)

    return boxes

def get_tree_boxes(with_scratchpad: bool = False, with_outputs: bool = True, with_toplevels: bool = True) -> list[Box]:
    tree = get_tree_json()
    return find_tree_boxes(tree, with_scratchpad=with_scratchpad, with_outputs=with_outputs, with_toplevels=with_toplevels)
