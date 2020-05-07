""" Testing for the nhgisxwalk.
"""

import unittest
import numpy

import nhgisxwalk


class Test_GeoCrossWalk(unittest.TestCase):
    def setUp(self):
        # set class attributes for testing

        self.df = nhgisxwalk.example_crosswalk_data()

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


class Test_upper_level_functions(unittest.TestCase):
    def setUp(self):
        self.df = nhgisxwalk.example_crosswalk_data()

    def tearDown(self):
        # OK to leave blank
        pass

    def test_example_crosswalk_data(self):
        known_type = "dataframe"
        observed_type = self.df._typ
        self.assertEqual(known_type, observed_type)

    def test_calculate_atoms(self):
        known = numpy.array(
            [
                ["A", "X", 0.5625, 0.5692307692307692],
                ["A", "Y", 0.4375, 0.4307692307692308],
                ["B", "X", 0.38461538461538464, 0.4],
                ["B", "Y", 0.6153846153846154, 0.6],
            ]
        )
        observed = nhgisxwalk.calculate_atoms(
            self.df,
            weight="wt",
            input_var=["pop_1990", "hh_1990"],
            weight_var=["pop", "hh"],
            weight_prefix="wt_",
            source_id="bgp1990",
            groupby_cols=["bgp1990", "trt2010"],
        )
        k1, o1 = known[:, :2], observed.values[:, :2]
        numpy.testing.assert_array_equal(k1, o1)
        k2, o2 = known[:, 2:].astype(float), observed.values[:, 2:].astype(float)
        numpy.testing.assert_allclose(k2, o2, atol=4)

    def test_str_types(self):
        known = {"test_name_1": str, "test_name_2": str}
        observed = nhgisxwalk.str_types(["test_name_1", "test_name_2"])
        self.assertEqual(known, observed)

    def test_valid_geo_shorthand(self):
        known_sn = {
            "blk": "block",
            "bgp": "block group part",
            "bkg": "block group",
            "trt": "tract",
            "cty": "county",
        }
        observed_sn = nhgisxwalk.valid_geo_shorthand(shorthand_name=True)
        self.assertEqual(known_sn, observed_sn)

        known_ns = {
            "block": "blk",
            "block group part": "bgp",
            "block group": "bkg",
            "tract": "trt",
            "county": "cty",
        }
        observed_ns = nhgisxwalk.valid_geo_shorthand(shorthand_name=False)
        self.assertEqual(known_ns, observed_ns)


if __name__ == "__main__":
    unittest.main()
