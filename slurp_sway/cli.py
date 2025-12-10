from argparse import ArgumentParser, Namespace as Args

from slurp_sway import box
from slurp_sway import sway_tree
from slurp_sway import slurp_wrapper

def parse_args() -> Args:
    ap = ArgumentParser()

    slurp_wrapper.add_options(ap)

    # extensions and wrapped options
    ap.add_argument("-o", action="store_true", default=False, help="Select a display output") # wrapped
    ap.add_argument("-t", action="store_true", default=False, help="Select a visible window") # extension, implemented as boxes
    ap.add_argument("-f", default="%x,%y %wx%h\n", type=str, help="Set output format") # wrapped
    ap.add_argument("-x", action="store_true", default=False, help="Use xdg-desktop-portal-wlr format") # extension
    ap.add_argument("-R", action="store_true", default=False, help="Strip label if region is not an exact input region") # extension

    return ap.parse_args()

def main():
    args = parse_args()

    boxes = []
    if not args.p:
        boxes = input_boxes = box.parse_input_boxes()
        if args.o or args.t:
            boxes += sway_tree.get_tree_boxes(with_outputs=args.o, with_toplevels=args.t)

    slurp_result = slurp_wrapper.run_slurp(args, boxes)
    if args.R and slurp_result.region_box not in boxes:
        slurp_result.region_box.kind = None
        slurp_result.region_box.label = ""
    if args.x:
        print(slurp_result.format_xdpw(), end="")
    else:
        print(slurp_result.format(args.f), end="")

if __name__ == '__main__':
    main()
