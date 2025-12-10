from __future__ import annotations
from argparse import ArgumentParser, Namespace as Args
from dataclasses import dataclass
from subprocess import Popen, PIPE
from copy import copy
import sys
from .box import Box

ARG_OPTIONS: list[str] = ["b", "c", "s", "B", "F", "w", "a"]
FLAG_OPTIONS: list[str] = ["d", "p", "r"]

def add_options(ap: ArgumentParser):
    ap.add_argument("-b", default=None, type=str, help="Set background color (#rrggbbaa)")
    ap.add_argument("-c", default=None, type=str, help="Set border color (#rrggbbaa)")
    ap.add_argument("-s", default=None, type=str, help="Set selection color (#rrggbbaa)")
    ap.add_argument("-B", default=None, type=str, help="Set option box color (#rrggbbaa)")
    ap.add_argument("-d", action="store_true", default=False, help="Display dimensions of selection")
    ap.add_argument("-F", default=None, type=str, help="Set the font family for the dimensions")
    ap.add_argument("-w", default=None, type=int, help="Set border weight")
    ap.add_argument("-p", action="store_true", default=False, help="Select a single point")
    ap.add_argument("-r", action="store_true", default=False, help="Restrict selection to predefined boxes")
    ap.add_argument("-a", default=None, type=str, help="Force aspect ration (w:h)")

def format_slurp_cmdline(args: Args) -> list[str]:
    cmd: list[str] = ["slurp"]

    for opt in ARG_OPTIONS:
        arg = getattr(args, opt)
        if arg:
            cmd += [f"-{opt}", arg]

    for opt in FLAG_OPTIONS:
        arg = getattr(args, opt)
        if arg:
            cmd += [f"-{opt}"]

    cmd += ["-f", "%x,%y %wx%h %l\n%X,%Y %Wx%H %o\n"]

    return cmd

@dataclass
class SlurpResult:
    region_box: Box
    output_box: Box

    @staticmethod
    def parse(s: str) -> SlurpResult:
        line0, line1 = s.rstrip("\n").split("\n")
        return SlurpResult(
            Box.parse_with_kind(line0),
            Box.parse(line1),
        )

    def format(self, fmt: str) -> str:
        result = ""

        is_fmt_seq = False
        for c in fmt:
            next_is_fmt_seq = False
            match (is_fmt_seq, c):
                case (False, "%"):
                    next_is_fmt_seq = True
                case (False, _):
                    result += c
                case (True, "%"):
                    result += c
                case (True, "x"):
                    result += f"{self.region_box.x}"
                case (True, "y"):
                    result += f"{self.region_box.y}"
                case (True, "w"):
                    result += f"{self.region_box.w}"
                case (True, "h"):
                    result += f"{self.region_box.h}"
                case (True, "l"):
                    result += f"{self.region_box.label}"
                case (True, "X"):
                    result += f"{self.output_box.x}"
                case (True, "Y"):
                    result += f"{self.output_box.y}"
                case (True, "W"):
                    result += f"{self.output_box.w}"
                case (True, "H"):
                    result += f"{self.output_box.h}"
                case (True, "o"):
                    result += f"{self.output_box.label}"
            is_fmt_seq = next_is_fmt_seq

        return result

    def format_xdpw(self) -> str:
        if self.region_box.kind == "output":
            return f"Monitor: {self.region_box.label}\n"
        elif self.region_box.kind == "toplevel":
            return f"Window: {self.region_box.label}\n"
        else:
            raise ValueError("non-monitor/window regions are not supported by xdg-desktop-portal-wlr yet")

def run_slurp(args: Args, boxes: list[Box]) -> SlurpResult:
    cmd = format_slurp_cmdline(args)

    formatted_boxes = "".join(f"{box.format()}\n" for box in boxes)
    with Popen(cmd, stdin=PIPE, stdout=PIPE) as p:
        p.stdin.write(formatted_boxes.encode())
        p.stdin.close()
        p.wait()
        result_str = p.stdout.read().decode()

        if p.returncode != 0:
            sys.exit(p.returncode)

    return SlurpResult.parse(result_str)
