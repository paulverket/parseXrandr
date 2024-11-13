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

class TestXrandrTxt(unittest.TestCase):
    
    def setUp(self):
        """
        Setup the test: read monitors from 'tests/xrandr.txt' and
        store them in the 'monitors' attribute.
        """
        self.monitors = read_monitor_info("tests/xrandr.txt")

    def test_xrandr_input(self):
        """
        Test the monitor parsing using 'tests/xrandr.txt'.

        This test verifies that the Monitors object is correctly
        instantiated and populated with data from 'tests/xrandr.txt'.
        """
        self.assertIsNotNone(self.monitors)
        self.assertIsInstance(self.monitors, Monitors)

    def test_xrandr_input_has_two_monitors(self):
        """
        Verify that two monitors are found in 'tests/xrandr.txt'.
        """
        num_monitors = self.monitors.get_num_monitors()
        self.assertEqual(num_monitors, 2)

    def test_xrandr_default_monitor(self):
        """
        Verify that the default monitor geometry matches the expected
        value ("1920x1080+0+0").
        """
        default_monitor = self.monitors.get_default_monitor()
        self.assertEqual(default_monitor, "1920x1080+0+0")

    def test_xrandr_largest_monitor(self):
        """
        Verify that the largest monitor geometry matches the expected
        value ("2560x1440+1920+0").
        """
        largest_monitor = self.monitors.get_largest_monitor()
        self.assertEqual(largest_monitor, "2560x1440+1920+0")


class TestXrandr1Txt(unittest.TestCase):
    
    def setUp(self):
        """
        Setup the test: read monitors from 'tests/xrandr1.txt' and
        store them in the 'monitors' attribute.
        """
        self.monitors = read_monitor_info("tests/xrandr1.txt")

    def test_xrandr1_input(self):
        """
        Test the monitor parsing using 'tests/xrandr1.txt'.

        This test verifies that the Monitors object is correctly
        instantiated and populated with data from 'tests/xrandr1.txt'.
        """
        self.assertIsNotNone(self.monitors)
        self.assertIsInstance(self.monitors, Monitors)

    def test_xrandr1_input_has_one_monitor(self):
        """
        Verify that one monitor is found in 'tests/xrandr1.txt'.
        """
        num_monitors = self.monitors.get_num_monitors()
        self.assertEqual(num_monitors, 1)

    def test_xrandr1_default_monitor(self):
        """
        Verify that the default monitor geometry matches the expected
        value ("2560x1440+1920+0").
        """
        default_monitor = self.monitors.get_default_monitor()
        single_monitor = "2560x1440+1920+0"
        self.assertEqual(default_monitor, single_monitor)

    def test_xrandr1_largest_monitor(self):
        """
        Verify that the largest monitor geometry matches the expected
        value ("2560x1440+1920+0").
        """
        largest_monitor = self.monitors.get_largest_monitor()
        single_monitor = "2560x1440+1920+0"
        self.assertEqual(largest_monitor, single_monitor)

if __name__ == '__main__':
  unittest.main(verbosity=1)
