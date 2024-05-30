#!/usr/bin/python3

"""
Parse the output of xrandr so one can adapt to different monitor setups. For example:

GEO=`xrandr --listactivemonitors| ./Monitors.py -l`
your-x-app -geometry $GEO
----------------------------
usage: Monitors.py [-h] [-l]

Choose a monitor from xrandr output sent to stdin.

optional arguments:
  -h, --help     show this help message and exit
  -l, --largest  Pick the largest monitor, else the first monitor
"""

import re
from collections import namedtuple

class Monitors:
  """Collect a set of monitor pixel sizes and offsets."""
  
  def __init__(self) -> None:
    """Initialize a parsing regular expression and a list of one or more monitor specs"""

    # ex: " 0: +*eDP-1 "
    index_re = r"\s*(\d+):\s*\S*\s*"
    # ex: 1920/309x1080/174+0+0
    geom_size_re = r"(\d+)/\d+x(\d+)/\d+\+(\d+)\+(\d+)"
    # ex: "  eDP-1"
    interface_re = r"\s*(\S*)\s*"

    self.regex = re.compile(index_re + geom_size_re + interface_re)
    self.monitor_tuple = namedtuple("Monitor", ["index", "hpixels", "vpixels", "hoffset",
                                    "voffset", "interface"])
    self.monitor_list = []

  def parse_xrandr(self, line: str) -> None:
    """Parse a xrandr line into sizes and offsets"""

    tokens = self.regex.split(line)[1:7] # Drop leading/trailing ''
    monitor = self.monitor_tuple(*tokens) 
    self.monitor_list.append(monitor)

  def geometry_str(self, monitor: namedtuple) -> str:
    """Return an X geometry spec for a monitor named tuple"""

    return f'{monitor.hpixels}x{monitor.vpixels}+{monitor.hoffset}+{monitor.voffset}'

  def get_largest_monitor(self) -> str:
    """Return the X geometry for the largest monitor"""

    largest = self.monitor_list[0]
    for candidate in self.monitor_list[1:]:
      current_pixels = int(largest.hpixels) * int(largest.vpixels)
      if int(candidate.hpixels) * int(candidate.vpixels) > current_pixels:
        largest = candidate
    return self.geometry_str(largest)
  
  def get_default_monitor(self) -> str:
    """Return the X geometry for the first monitor"""

    return self.geometry_str(self.monitor_list[0])
  
  def get_num_monitors(self) -> int:
    """Return how many monitors were parsed from the input"""
    return len(self.monitor_list)

if __name__ == '__main__':
  monitors = Monitors()
  # Parse the argv
  import argparse
  argparser = argparse.ArgumentParser(
    description='Choose a monitor from xrandr output sent to stdin.')
  argparser.add_argument('-l', '--largest', action='store_true', 
                         help='Pick the largest monitor, else the first monitor')
  args = argparser.parse_args()
  import sys
  # Get xrandr input from stdin
  i = 0
  for line in sys.stdin:
    if i: # Skip the #monitors line
      monitors.parse_xrandr(line)
    i += 1
  if 0 == monitors.get_num_monitors():
    print('1920x1080+0+0') # No monitor input found, return default
    exit()
  if args.largest:
    print(monitors.get_largest_monitor())
  else:
    print(monitors.get_default_monitor())
