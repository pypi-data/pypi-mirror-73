# genwal
Little python script to generate Gentoo wallpapers

## Notice
__**wallpaper.svg is modified version of [gentoo logo](https://www.gentoo.org/inside-gentoo/artwork/gentoo-logo.html), I added background and modular color  
wallpaper.svg is licensed CC-BY-SA/2.5**__

## Install
Install from git:
```
python -m pip install git+https://github.com/GrbavaCigla/genwal
```
Install from pypi (coming soon):
```
python -m pip install genwal
```

## Usage

Without any parametars, default png is generated

```
usage: genwal [-h] [--bg BG] [--fg1 FG1] [--fg2 FG2] [--fg3 FG3]
              [--scale SCALE]

Little python script to generate Gentoo wallpapers

optional arguments:
  -h, --help            show this help message and exit
  --bg BG, --background BG
  --fg1 FG1, --foreground1 FG1
  --fg2 FG2, --foreground2 FG2
  --fg3 FG3, --foreground3 FG3
  --scale SCALE
```

## TODO
- Add more distros
- Add option to change scale of logo
- Support other aspect ratios
