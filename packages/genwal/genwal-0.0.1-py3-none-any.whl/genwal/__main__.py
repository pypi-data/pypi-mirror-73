import argparse
import re
import requests
import os

from cairosvg import svg2png

def color(color: str):
    if not re.match(r"#[0-9a-fA-F]{6}", color):
        raise argparse.ArgumentTypeError
    return color


parser = argparse.ArgumentParser(
    prog="genwal",
    description="Little python script to generate Gentoo wallpapers",
    add_help=True,
)

parser.add_argument("--bg", "--background", default="#4D4D4D", type=color)
parser.add_argument("--fg1", "--foreground1", default="#0D4F73", type=color)
parser.add_argument("--fg2", "--foreground2", default="#FFFFFF", type=color)
parser.add_argument("--fg3", "--foreground3", default="#007CBF", type=color)
parser.add_argument("--scale", default=1, type=int)

args = parser.parse_args()

replacements = {
    "{BACKGROUND}": args.bg,
    "{FOREGROUND1}": args.fg1,
    "{FOREGROUND2}": args.fg2,
    "{FOREGROUND3}": args.fg3,
}

response = requests.get("https://raw.githubusercontent.com/GrbavaCigla/genwal/master/wallpaper.svg")
if response.status_code == 200:
    svg_content = response.text

    for k, v in replacements.items():
        svg_content = re.sub(k, v, svg_content)

    svg2png(
        bytestring=svg_content, 
        write_to="wallpaper.png",
        scale=args.scale,
    )
else:
    print("Failed to fetch the wallpaper.svg")
    exit(1)
