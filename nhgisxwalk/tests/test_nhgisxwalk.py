""" Testing for the nhgisxwalk.
"""

import unittest
import numpy

import nhgisxwalk


class TestGenericName(unittest.TestCase):
    def setUp(self):
        # set class attributes for testing
        pass

    def tearDown(self):
        # OK to leave blank
        pass

    def test_generic_function_assertEqual(self):
        # testing exact equality
        known = "thing"
        observed = "thing"
        self.assertEqual(known, observed)

    def test_generic_function_assertAlmostEqual(self):
        # testing approximate equality
        known = 0.01
        observed = 0.0100000001
        self.assertAlmostEqual(known, observed, places=3)

    def test_generic_function_assertIn(self):
        # testing membership
        known = "thing"
        observed = ["thing", "stuff"]
        self.assertIn(known, observed)

    def test_network_failures_assertRaises(self):
        # testing for triggered errors
        with self.assertRaises(NameError):
            I_AM_SAM
            # self.thing_that_should_raise_TypeError()

    def test_generic_function_numpy_array_equality(self):
        # testing membership
        known = numpy.array([0.0])
        observed = numpy.array([0.0])

        # all close
        numpy.testing.assert_allclose(known, observed)


if __name__ == "__main__":
    unittest.main()
