from __future__ import annotations
from dataclasses import dataclass
import sys
import re

@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int
    label: str
    kind: str | None = None

    @staticmethod
    def parse(s: str, kind: str | None = None) -> Box:
        m = re.match("([0-9]+),([0-9]+) ([0-9]+)x([0-9]+)( (.*))?", s)
        if m is None:
            raise ValueError(f"invalid box format: {s}")
        return Box(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(6) or "", kind=kind)

    @staticmethod
    def parse_with_kind(s: str) -> Box:
        m = re.match("([0-9]+),([0-9]+) ([0-9]+)x([0-9]+) ([^:]+):(.*)", s)
        if m is None:
            raise ValueError(f"invalid box format: {s}")
        return Box(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(6), kind=m.group(5))

    @staticmethod
    def from_json(node: dict[str, int]) -> Box:
        return Box(
            node["x"], node["y"], node["width"], node["height"], ""
        )

    def format(self, with_label: bool = True) -> str:
        label = ""
        if self.kind is not None:
            label += self.kind + ":"
        if with_label:
            label += self.label
        if len(label) != 0:
            label = " " + label

        return f"{self.x},{self.y} {self.w}x{self.h}{label}"

def parse_input_boxes() -> list[Box]:
    boxes = []

    if not sys.stdin.isatty():
        for line in sys.stdin.readline():
            if line == "":
                continue

            line = line.rstrip("\n")
            boxes.append(Box.parse(line, "input"))

    return boxes
