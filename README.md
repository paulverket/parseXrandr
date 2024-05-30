# Read Me
I sometimes use X11 without a window manager. I use the following to size and position windows.

Parse the output of xrandr so one can adapt to different monitor setups. For example:

```sh
GEO=`xrandr --listactivemonitors| ./Monitors.py -l`
your-x-app -geometry $GEO
```
## Usage
```
usage: Monitors.py [-h] [-l]

Choose a monitor from xrandr output sent to stdin.

optional arguments:
  -h, --help     show this help message and exit
  -l, --largest  Pick the largest monitor, else the first monitor
```