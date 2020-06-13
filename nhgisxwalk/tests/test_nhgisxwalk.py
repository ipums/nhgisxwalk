""" Testing for the nhgisxwalk.
"""

import unittest
import numpy
import pandas

import nhgisxwalk

# use sample data for all empirical tests
data_dir = "./testing_data_subsets"
tabular_data_path = data_dir + "/%s_block.csv.zip"
supplement_data_path_90 = data_dir + "/%s_blck_grp_598_103.csv.zip"

# shorthand for geographies
blk, bgp, bkg, trt, cty = "blk", "bgp", "bkg", "trt", "cty"

# shorthand for years
_90, _00, _10 = "1990", "2000", "2010"

# tagged names for variables
input_var_tags = ["pop", "fam", "hh", "hu"]

# state-level values to use for subset -- Delaware
stfips = "10"


def fetch_base_xwalk(sg, tg, sy, ty):
    base_xwalk_name = "/nhgis_%s%s_%s%s_gj.csv.zip" % (sg, sy, tg, ty)
    base_xwalk_file = data_dir + base_xwalk_name
    data_types = nhgisxwalk.str_types(["GJOIN%s" % sy, "GJOIN%s" % ty])
    base_xwalk = pandas.read_csv(base_xwalk_file, index_col=0, dtype=data_types)
    return base_xwalk


# 1990 blocks to 2010 blocks ---------------------------------------------------
base_xwalk_blk1990_blk2010 = fetch_base_xwalk(blk, blk, _90, _10)
# input variables
input_vars_1990 = [
    nhgisxwalk.desc_code_1990["Persons"]["Total"],
    nhgisxwalk.desc_code_1990["Families"]["Total"],
    nhgisxwalk.desc_code_1990["Households"]["Total"],
    nhgisxwalk.desc_code_1990["Housing Units"]["Total"],
]
# empirical tabular data path
tab_data_path_1990 = tabular_data_path % _90
# supplementary empirical tabular data path (only for 1990)
supplement_data_path_90 = tabular_data_path % _90

# 2000 blocks to 2010 blocks ---------------------------------------------------
base_xwalk_blk2000_blk2010 = fetch_base_xwalk(blk, blk, _00, _10)
# input variables
input_vars_2000_SF1b = [
    nhgisxwalk.desc_code_2000_SF1b["Persons"]["Total"],
    nhgisxwalk.desc_code_2000_SF1b["Families"]["Total"],
    nhgisxwalk.desc_code_2000_SF1b["Households"]["Total"],
    nhgisxwalk.desc_code_2000_SF1b["Housing Units"]["Total"],
]
# empirical tabular data path
tab_data_path_2000 = tabular_data_path % _00


class Test_GeoCrossWalk(unittest.TestCase):

    """
    # 1990 bgp to 2010 trt through 1990 blk to 2010 blk ------------------------ ############################### will need to redo following NO DATA --Delaware
    def test_xwalk_full_blk1990_blk2010(self):
        knw_str_vals = numpy.array(
            [
                ["G11000105000050000009806989999999884011", "G1100010009811"],
                ["G11000105000050000009806989999999884012", "G1100010009810"],
                ["G11000105000050000009806989999999884012", "G1100010009811"],
                ["G11000105000050000009807989999999884011", "G1100010009807"],
            ]
        )
        knw_num_vals = numpy.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.41477113, 0.41545353, 0.39687267, 0.39506995],
                [0.58522887, 0.58454647, 0.60312733, 0.60493005],
                [1.0, 1.0, 1.0, 1.0],
            ]
        )
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk1990_blk2010,
            source_year=_90,
            target_year=_10,
            source_geo=bgp,
            target_geo=trt,
            base_source_table=tab_data_path_1990,
            input_var=input_vars_1990,
            weight_var=input_var_tags,
        )
        ix1, ix2 = 688, 692
        id_cols = ["bgp1990", "trt2010"]
        obs_str_vals = obs_xwalk.xwalk[id_cols][ix1:ix2].values
        wgt_cols = ["wt_pop", "wt_fam", "wt_hh", "wt_hu"]
        obs_num_vals = obs_xwalk.xwalk[wgt_cols][ix1:ix2].values
        numpy.testing.assert_equal(knw_str_vals, obs_str_vals)
        numpy.testing.assert_allclose(knw_num_vals, obs_num_vals)
    """

    """
    def test_xwalk_state_blk1990_blk2010(self): # ------------------------ ############################### will need to redo following NO DATA --Delaware
        knw_str_vals = numpy.array(
            [
                ["G11000105000050000009806989999999884011", "G1100010009811"],
                ["G11000105000050000009806989999999884012", "G1100010009810"],
                ["G11000105000050000009806989999999884012", "G1100010009811"],
                ["G11000105000050000009807989999999884011", "G1100010009807"],
            ]
        )
        knw_num_vals = numpy.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.41477113, 0.41545353, 0.39687267, 0.39506995],
                [0.58522887, 0.58454647, 0.60312733, 0.60493005],
                [1.0, 1.0, 1.0, 1.0],
            ]
        )
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk1990_blk2010,
            source_year=_90,
            target_year=_10,
            source_geo=bgp,
            target_geo=trt,
            base_source_table=tab_data_path_1990,
            input_var=input_vars_1990,
            weight_var=input_var_tags,
            stfips=stfips,
            vectorized=False,
            keep_base=False,
        )
        ix1, ix2 = 688, 692
        id_cols = ["bgp1990", "trt2010"]
        obs_str_vals = obs_xwalk.xwalk[id_cols][ix1:ix2].values
        wgt_cols = ["wt_pop", "wt_fam", "wt_hh", "wt_hu"]
        obs_num_vals = obs_xwalk.xwalk[wgt_cols][ix1:ix2].values
        numpy.testing.assert_equal(knw_str_vals, obs_str_vals)
        numpy.testing.assert_allclose(knw_num_vals, obs_num_vals)
    """

    # 2000 bgp to 2010 trt through 2000 blk to 2010 blk
    def test_xwalk_full_blk2000_blk2010(self):
        knw_str_vals = numpy.array(
            [
                ["G10000509355299999051304R1", "G1000050051305"],
                ["G10000509355299999051304R1", "G1000050051306"],
                ["G10000509355299999051304R1", "G1000050051400"],
                ["G10000509355299999051304R2", "G1000050051305"],
            ]
        )
        knw_num_vals = numpy.array(
            [
                [6.80605382e-01, 6.33909150e-01, 6.57366450e-01, 6.59501671e-01],
                [3.19167389e-01, 3.65781711e-01, 3.42281879e-01, 3.40110906e-01],
                [2.27229039e-04, 3.09138740e-04, 3.51671251e-04, 3.87423412e-04],
                [8.02660754e-01, 8.17567568e-01, 8.20895522e-01, 8.36236934e-01],
            ]
        )
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=trt,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
        )
        ix1, ix2 = 1025, 1029
        id_cols = ["bgp2000gj", "trt2010gj"]
        obs_str_vals = obs_xwalk.xwalk[id_cols][ix1:ix2].values
        wgt_cols = ["wt_pop", "wt_fam", "wt_hh", "wt_hu"]
        obs_num_vals = obs_xwalk.xwalk[wgt_cols][ix1:ix2].values
        numpy.testing.assert_equal(knw_str_vals, obs_str_vals)
        numpy.testing.assert_allclose(knw_num_vals, obs_num_vals)

    def test_xwalk_state_blk2000_blk2010(self):
        knw_str_vals = numpy.array(
            [
                ["G10000509355299999051304R1", "G1000050051305"],
                ["G10000509355299999051304R1", "G1000050051306"],
                ["G10000509355299999051304R1", "G1000050051400"],
                ["G10000509355299999051304R2", "G1000050051305"],
            ]
        )
        knw_num_vals = numpy.array(
            [
                [6.80605382e-01, 6.33909150e-01, 6.57366450e-01, 6.59501671e-01],
                [3.19167389e-01, 3.65781711e-01, 3.42281879e-01, 3.40110906e-01],
                [2.27229039e-04, 3.09138740e-04, 3.51671251e-04, 3.87423412e-04],
                [8.02660754e-01, 8.17567568e-01, 8.20895522e-01, 8.36236934e-01],
            ]
        )
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=trt,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            stfips=stfips,
            vectorized=False,
            keep_base=False,
        )
        ix1, ix2 = 1025, 1029
        id_cols = ["bgp2000gj", "trt2010gj"]
        obs_str_vals = obs_xwalk.xwalk[id_cols][ix1:ix2].values
        wgt_cols = ["wt_pop", "wt_fam", "wt_hh", "wt_hu"]
        obs_num_vals = obs_xwalk.xwalk[wgt_cols][ix1:ix2].values
        numpy.testing.assert_equal(knw_str_vals, obs_str_vals)
        numpy.testing.assert_allclose(knw_num_vals, obs_num_vals)

    # non-year, geography specific ---------------------------------------------
    def test_xwalk_write_read_csv(self):
        write_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=trt,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            keep_base=False,
            stfips=stfips,
        )
        write_xwalk.xwalk_to_csv()
        read_xwalk = nhgisxwalk.GeoCrossWalk.xwalk_from_csv(write_xwalk.xwalk_name)
        known_values = write_xwalk.xwalk["wt_pop"].values
        observed_values = read_xwalk["wt_pop"].values
        numpy.testing.assert_allclose(known_values, observed_values)

    def test_xwalk_write_read_pickle(self):
        write_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=trt,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            keep_base=False,
            stfips=stfips,
        )
        write_xwalk.xwalk_to_pickle()
        read_xwalk = nhgisxwalk.GeoCrossWalk.xwalk_from_pickle(write_xwalk.xwalk_name)
        known_values = write_xwalk.xwalk["wt_pop"].values
        observed_values = read_xwalk.xwalk["wt_pop"].values
        numpy.testing.assert_allclose(known_values, observed_values)

    def test_xwalk_uneven_input(self):
        # testing for triggered errors
        with self.assertRaises(RuntimeError):
            observed_xwalk = nhgisxwalk.GeoCrossWalk(
                base_xwalk_blk2000_blk2010,
                source_year=_00,
                target_year=_10,
                source_geo=bgp,
                target_geo=trt,
                base_source_table=tab_data_path_2000,
                input_var=input_vars_2000_SF1b,
                weight_var=["one", "two"],
                stfips=stfips,
            )

    def test_xwalk_source_code_blk(self):
        # testing for triggered errors
        with self.assertRaises(RuntimeError):
            observed_xwalk = nhgisxwalk.GeoCrossWalk(
                base_xwalk_blk1990_blk2010,
                source_year=_90,
                target_year=_10,
                source_geo=blk,
                target_geo=trt,
                base_source_table=tab_data_path_1990,
                input_var=input_vars_1990,
                weight_var=input_var_tags,
            )

    def test_xwalk_source_code_bkg(self):
        # testing for triggered errors
        with self.assertRaises(AttributeError):
            observed_xwalk = nhgisxwalk.GeoCrossWalk(
                base_xwalk_blk1990_blk2010,
                source_year=_90,
                target_year=_10,
                source_geo=bkg,
                target_geo=trt,
                base_source_table=tab_data_path_1990,
                input_var=input_vars_1990,
                weight_var=input_var_tags,
            )

    def test_xwalk_source_code_trt(self):
        # testing for triggered errors
        with self.assertRaises(AttributeError):
            observed_xwalk = nhgisxwalk.GeoCrossWalk(
                base_xwalk_blk1990_blk2010,
                source_year=_90,
                target_year=_10,
                source_geo=trt,
                target_geo=trt,
                base_source_table=tab_data_path_1990,
                input_var=input_vars_1990,
                weight_var=input_var_tags,
            )

    def test_xwalk_source_code_cty(self):
        # testing for triggered errors
        with self.assertRaises(AttributeError):
            observed_xwalk = nhgisxwalk.GeoCrossWalk(
                base_xwalk_blk1990_blk2010,
                source_year=_90,
                target_year=_10,
                source_geo=cty,
                target_geo=trt,
                base_source_table=tab_data_path_1990,
                input_var=input_vars_1990,
                weight_var=input_var_tags,
            )


class Test_upper_level_functions(unittest.TestCase):
    def setUp(self):
        self.example_df = nhgisxwalk.example_crosswalk_data()

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
            blk: "block",
            bgp: "block group part",
            bkg: "block group",
            trt: "tract",
            cty: "county",
        }
        observed_sn = nhgisxwalk.valid_geo_shorthand(shorthand_name=True)
        self.assertEqual(known_sn, observed_sn)

        known_ns = {
            "block": blk,
            "block group part": bgp,
            "block group": bkg,
            "tract": trt,
            "county": cty,
        }
        observed_ns = nhgisxwalk.valid_geo_shorthand(shorthand_name=False)
        self.assertEqual(known_ns, observed_ns)


if __name__ == "__main__":
    unittest.main()
