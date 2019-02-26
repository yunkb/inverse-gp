import unittest

import torch

from simulators import HeavySimulator


class TestHeavySimulator(unittest.TestCase):
    def test_call(self) -> None:
        simulator = HeavySimulator()
        x = torch.linspace(0, 1, 20)
        y = simulator(x)
        self.assertEqual(x.shape, y.shape)


if __name__ == "__main__":
    unittest.main()
