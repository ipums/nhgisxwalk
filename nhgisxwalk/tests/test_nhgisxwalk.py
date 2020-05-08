""" Testing for the nhgisxwalk.
"""

import unittest
import numpy
import pandas

import nhgisxwalk


# use sample data for all empirical tests
data_dir = "./testing_data_subsets/"
# 1990 blocks to 2010 blocks
source_year, target_year = "1990", "2010"
base_xwalk_name = "/nhgis_blk%s_blk%s_gj.csv.zip" % (source_year, target_year)
base_xwalk_file = data_dir + base_xwalk_name
data_types = nhgisxwalk.str_types(["GJOIN%s" % source_year, "GJOIN%s" % target_year])
base_xwalk = pandas.read_csv(base_xwalk_file, index_col=0, dtype=data_types)
# input variables
input_vars = [
    nhgisxwalk.desc_code_1990["Persons"]["Total"],
    nhgisxwalk.desc_code_1990["Families"]["Total"],
    nhgisxwalk.desc_code_1990["Households"]["Total"],
    nhgisxwalk.desc_code_1990["Housing Units"]["Total"],
]
input_var_tags = ["pop", "fam", "hh", "hu"]

# empirical tabular data path
tab_data_path = data_dir + "/%s_block.csv.zip" % source_year

# state to use for subset -- Wyoming
stfips = "56"


class Test_GeoCrossWalk(unittest.TestCase):
    def setUp(self):
        self.base_xwalk = base_xwalk
        self.tab_data_path = tab_data_path
        self.source_year, self.target_year = source_year, target_year
        self.input_vars, self.input_var_tags = input_vars, input_var_tags
        self.stfips = stfips
        # self.

    def tearDown(self):
        # OK to leave blank
        pass

    def test_xwalk_full(self):
        known_values = numpy.array([1.0, 0.10763114, 0.89236886, 1.0])
        observed_xwalk = nhgisxwalk.GeoCrossWalk(
            self.base_xwalk,
            source_year=self.source_year,
            target_year=self.target_year,
            source_geo="bgp",
            target_geo="trt",
            base_source_table=self.tab_data_path,
            input_var=self.input_vars,
            weight_var=self.input_var_tags,
        )
        observed_values = observed_xwalk.xwalk["wt_pop"].tail(15).values[3:7]
        numpy.testing.assert_allclose(known_values, observed_values)

    def test_xwalk_state(self):
        known_values = numpy.array([1.0, 0.10763114, 0.89236886, 1.0])
        observed_xwalk = nhgisxwalk.GeoCrossWalk(
            self.base_xwalk,
            source_year=self.source_year,
            target_year=self.target_year,
            source_geo="bgp",
            target_geo="trt",
            base_source_table=self.tab_data_path,
            input_var=self.input_vars,
            weight_var=self.input_var_tags,
            stfips=self.stfips,
            vectorized=False,
            keep_base=False,
        )
        observed_values = observed_xwalk.xwalk["wt_pop"].tail(15).values[3:7]
        numpy.testing.assert_allclose(known_values, observed_values)

    def test_xwalk_write_read_csv(self):
        write_xwalk = nhgisxwalk.GeoCrossWalk(
            self.base_xwalk,
            source_year=self.source_year,
            target_year=self.target_year,
            source_geo="bgp",
            target_geo="trt",
            base_source_table=self.tab_data_path,
            input_var=self.input_vars,
            weight_var=self.input_var_tags,
            keep_base=False,
            stfips=self.stfips,
        )
        write_xwalk.xwalk_to_csv()
        read_xwalk = nhgisxwalk.GeoCrossWalk.xwalk_from_csv(write_xwalk.xwalk_name)
        known_values = write_xwalk.xwalk["wt_pop"].values
        observed_values = read_xwalk["wt_pop"].values
        numpy.testing.assert_allclose(known_values, observed_values)

    def test_xwalk_write_read_pickle(self):
        write_xwalk = nhgisxwalk.GeoCrossWalk(
            self.base_xwalk,
            source_year=self.source_year,
            target_year=self.target_year,
            source_geo="bgp",
            target_geo="trt",
            base_source_table=self.tab_data_path,
            input_var=self.input_vars,
            weight_var=self.input_var_tags,
            keep_base=False,
            stfips=self.stfips,
        )
        write_xwalk.xwalk_to_pickle()
        read_xwalk = nhgisxwalk.GeoCrossWalk.xwalk_from_pickle(write_xwalk.xwalk_name)
        known_values = write_xwalk.xwalk["wt_pop"].values
        observed_values = read_xwalk.xwalk["wt_pop"].values
        numpy.testing.assert_allclose(known_values, observed_values)

    def test_xwalk_code_type_ge(self):
        # testing for triggered errors
        with self.assertRaises(RuntimeError):
            observed_xwalk = nhgisxwalk.GeoCrossWalk(
                self.base_xwalk,
                source_year=self.source_year,
                target_year=self.target_year,
                source_geo="bgp",
                target_geo="trt",
                base_source_table=self.tab_data_path,
                input_var=self.input_vars,
                weight_var=self.input_var_tags,
                stfips=self.stfips,
                code_type="ge",
            )

    def test_xwalk_code_type_NAN(self):
        # testing for triggered errors
        with self.assertRaises(RuntimeError):
            observed_xwalk = nhgisxwalk.GeoCrossWalk(
                self.base_xwalk,
                source_year=self.source_year,
                target_year=self.target_year,
                source_geo="bgp",
                target_geo="trt",
                base_source_table=self.tab_data_path,
                input_var=self.input_vars,
                weight_var=self.input_var_tags,
                stfips=self.stfips,
                code_type="NAN",
            )

    def test_xwalk_uneven_input(self):
        # testing for triggered errors
        with self.assertRaises(RuntimeError):
            observed_xwalk = nhgisxwalk.GeoCrossWalk(
                self.base_xwalk,
                source_year=self.source_year,
                target_year=self.target_year,
                source_geo="bgp",
                target_geo="trt",
                base_source_table=self.tab_data_path,
                input_var=self.input_vars,
                weight_var=["one", "two"],
                stfips=self.stfips,
            )

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
        self.example_df = nhgisxwalk.example_crosswalk_data()

    def tearDown(self):
        # OK to leave blank
        pass

    def test_example_crosswalk_data(self):
        known_type = "dataframe"
        observed_type = self.example_df._typ
        self.assertEqual(known_type, observed_type)

    def test_calculate_atoms_single_prefix(self):
        known = numpy.array(
            [
                ["A", "X", 0.5625],
                ["A", "Y", 0.4375],
                ["B", "X", 0.38461538461538464],
                ["B", "Y", 0.6153846153846154],
            ]
        )
        observed = nhgisxwalk.calculate_atoms(
            self.example_df,
            weight="wt",
            input_var="pop_1990",
            weight_var="pop",
            weight_prefix="wt_",
            source_id="bgp1990",
            groupby_cols=["bgp1990", "trt2010"],
        )
        k1, o1 = known[:, :2], observed.values[:, :2]
        numpy.testing.assert_array_equal(k1, o1)
        k2, o2 = known[:, 2:].astype(float), observed.values[:, 2:].astype(float)
        numpy.testing.assert_allclose(k2, o2, atol=4)

    def test_calculate_atoms_single_no_prefix(self):
        known = numpy.array(
            [
                ["A", "X", 0.5625],
                ["A", "Y", 0.4375],
                ["B", "X", 0.38461538461538464],
                ["B", "Y", 0.6153846153846154],
            ]
        )
        observed = nhgisxwalk.calculate_atoms(
            self.example_df,
            weight="wt",
            input_var="pop_1990",
            weight_var="pop",
            source_id="bgp1990",
            groupby_cols=["bgp1990", "trt2010"],
        )
        k1, o1 = known[:, :2], observed.values[:, :2]
        numpy.testing.assert_array_equal(k1, o1)
        k2, o2 = known[:, 2:].astype(float), observed.values[:, 2:].astype(float)
        numpy.testing.assert_allclose(k2, o2, atol=4)

    def test_calculate_atoms_multi_prefix(self):
        known = numpy.array(
            [
                ["A", "X", 0.5625, 0.5692307692307692],
                ["A", "Y", 0.4375, 0.4307692307692308],
                ["B", "X", 0.38461538461538464, 0.4],
                ["B", "Y", 0.6153846153846154, 0.6],
            ]
        )
        observed = nhgisxwalk.calculate_atoms(
            self.example_df,
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

    def test_calculate_atoms_multi_no_prefix(self):
        known = numpy.array(
            [
                ["A", "X", 0.5625, 0.5692307692307692],
                ["A", "Y", 0.4375, 0.4307692307692308],
                ["B", "X", 0.38461538461538464, 0.4],
                ["B", "Y", 0.6153846153846154, 0.6],
            ]
        )
        observed = nhgisxwalk.calculate_atoms(
            self.example_df,
            weight="wt",
            input_var=["pop_1990", "hh_1990"],
            weight_var=["pop", "hh"],
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
