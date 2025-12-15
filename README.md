# slurp-sway

Wrapper around slurp that adds Sway-specific features such as toplevel selection.

## Features

- Compatible with all slurp command line options (as of slurp 1.5.0)
- Support for selecting visible windows with `-t`
  - Current window positions and toplevel identifiers are read using `swaymsg -t get_tree`
- Support for `xdg-desktop-portal-wlr 0.8.1` output format with `-x` (`Monitor: ` and `Window: `)
- Support for additional **FORMAT** sequences:
  - `%k` region kind (`output` for outputs, `toplevel` for toplevels, `input` for stdin regions, and `region` for freeform regions)
  - `%K` xdg-desktop-portal-wlr compatible region kind (`Monitor` for outputs, `Window` for toplevels, and as an extension `Ìnput` for stdin regions and `Region` for freeform regions)
  - `%L` label of the region, but use the region coordinates and size for regions without a label (format `%x,%y %wx%h`)
- Support for not associating freeform regions with output/toplevel/stdin region labels with `-R`
  - This is intended to be used with the `%L` format

## Usage

```
usage: slurp-sway [-h] [-d] [-b #rrggbbaa] [-c #rrggbbaa] [-s #rrggbbaa] [-B #rrggbbaa] [-F s] [-w n] [-f s] [-o] [-p] [-r] [-a w:h]
                  [-t] [-x] [-R]

Wrapper around slurp that adds Sway-specific features such as toplevel selection.

options:
  -h, --help    show this help message and exit
  -d            Display dimensions of selection
  -b #rrggbbaa  Set background color
  -c #rrggbbaa  Set border color
  -s #rrggbbaa  Set selection color
  -B #rrggbbaa  Set option box color
  -F s          Set the font family for the dimensions
  -w n          Set border weight
  -f s          Set output format (wrapped)
  -o            Select a display output (wrapped)
  -p            Select a single point
  -r            Restrict selection to predefined boxes
  -a w:h        Force aspect ration
  -t            Select a visible window (extension)
  -x            Use xdg-desktop-portal-wlr format (extension)
  -R            Strip label if region is not an exact input region (extension)

Options marked (extension) are specific to slurp-sway. Options marked (wrapped) are reimplemented and not passed to slurp.
```

## Installation

- `pipx install .` (or `--editable .` for a development install)
