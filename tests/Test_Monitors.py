import unittest
import sys

sys.path.insert(0, 'src')

from Monitors import Monitors

def read_monitor_info(filename : str) -> list:
  """Reads monitor information from a text file.

  Args:
    filename: The path to the text file.

  Returns:
    # A list of dictionaries containing monitor information. Each dictionary has keys:
    #   index: The monitor ID (e.g., "0", "1").
    #   mode: The dummy field (always "+").
    #   resolution: A string representing pixel width/height and mm width/height (e.g., "1920/309x1080/174").
    #   offset: A string representing the x and y offset (e.g., "+0+0").
    #   monitor_name: The name of the monitor (e.g., "eDP-1", "HDMI-1").
  """
  monitors = Monitors()
  with open(filename, 'r') as f:
    # Get the number of monitors
    num_monitors = int(f.readline().split(":")[1])

    # Loop through each monitor line
    for _ in range(num_monitors):
      line = f.readline()
      monitors.parse_xrandr(line)

  return monitors

class TestMonitors(unittest.TestCase):
  def test_xrandr_input(self):
    """
    Test the monitor parsing using 'tests/xrandr.txt'.

    This test verifies that the Monitors object is correctly
    instantiated and populated with data from 'tests/xrandr.txt'.
    It checks that:
    - The Monitors instance is not None and of type Monitors.
    - The number of monitors parsed is 2.
    - The default monitor geometry matches the expected
      value ("1920x1080+0+0").
    - The largest monitor geometry matches the expected
      value ("2560x1440+1920+0").
    """
    monitors = read_monitor_info("tests/xrandr.txt")
    self.assertIsNotNone(monitors)
    self.assertIsInstance(monitors, Monitors)

    num_monitors = monitors.get_num_monitors()
    self.assertEqual(num_monitors, 2)

    default_monitor = monitors.get_default_monitor()
    self.assertEqual(default_monitor, "1920x1080+0+0")

    largest_monitor = monitors.get_largest_monitor()
    self.assertEqual(largest_monitor, "2560x1440+1920+0")

  def test_xrandr1_input(self):
    """
    Test the monitor parsing using 'tests/xrandr1.txt'.

    This test verifies that the Monitors object is correctly
    instantiated and populated with data from 'tests/xrandr1.txt'.
    It checks that:
    - The Monitors instance is not None and of type Monitors.
    - The number of monitors parsed is 1.
    - The default and largest monitor geometries match the expected
      values ("2560x1440+1920+0").
    """
    monitors = read_monitor_info("tests/xrandr1.txt")
    self.assertIsNotNone(monitors)
    self.assertIsInstance(monitors, Monitors)

    num_monitors = monitors.get_num_monitors()
    self.assertEqual(num_monitors, 1)

    default_monitor = monitors.get_default_monitor()
    single_monitor = "2560x1440+1920+0"
    self.assertEqual(default_monitor, single_monitor)

    largest_monitor = monitors.get_largest_monitor()
    self.assertEqual(largest_monitor, single_monitor)

if __name__ == '__main__':
  unittest.main()
