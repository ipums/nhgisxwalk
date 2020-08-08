""" Testing for the nhgisxwalk.
"""

import nhgisxwalk
import numpy
import os
import pandas
import shutil
import unittest

CSV = "csv"
ZIP = "zip"
PKL = "pkl"


# use sample data for all empirical tests
data_dir = "./testing_data_subsets/"
tabular_data_path = data_dir + "/%s_block.%s.%s"
supplement_data_path_90 = data_dir + "/%s_blck_grp_598_103.%s.%s"

# shorthand for geographies
blk, bgp, bg, tr, co = "blk", "bgp", "bg", "tr", "co"

# shorthand for years
_90, _00, _10 = "1990", "2000", "2010"

# tagged names for variables
input_var_tags = ["pop", "fam", "hh", "hu"]

# state-level values to use for subset -- Delaware
stfips = "10"

# NHGIS standard geographic abbreviation
gj = "gj"


def fetch_base_xwalk(sg, tg, sy, ty):
    base_xwalk_name = "nhgis_%s%s_%s%s_gj" % (sg, sy, tg, ty)
    data_types = nhgisxwalk.str_types(["GJOIN%s" % sy, "GJOIN%s" % ty])
    from_csv_kws = {"path": data_dir, "archived": True, "remove_unpacked": True}
    read_csv_kws = {"dtype": data_types}
    base_xwalk = nhgisxwalk.xwalk_df_from_csv(
        base_xwalk_name, **from_csv_kws, **read_csv_kws
    )
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
tab_data_path_1990 = tabular_data_path % (_90, CSV, ZIP)
# supplementary empirical tabular data path (only for 1990)
supplement_data_path_90 = supplement_data_path_90 % (_90, CSV, ZIP)

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
tab_data_path_2000 = tabular_data_path % (_00, CSV, ZIP)


class Test_GeoCrossWalk(unittest.TestCase):

    # 1990 bgp to 2010 tr through 1990 blk to 2010 blk
    def test_xwalk_full_bgp1990_tr2010(self):
        knw_str_vals = numpy.array(
            [
                [
                    "G100001090444999990421009999999219012",
                    "G1000010042100",
                    "10001042100",
                ],
                [
                    "G100001090444999990421009999999999921",
                    "G1000010042100",
                    "10001042100",
                ],
                [
                    "G100001090444999990421009999999999921",
                    "G1000010042201",
                    "10001042201",
                ],
                [
                    "G100001090444999990421009999999999922",
                    "G1000010042100",
                    "10001042100",
                ],
            ]
        )
        knw_num_vals = numpy.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.99766436, 0.99716625, 0.99714829, 0.99727768],
                [0.00233564, 0.00283375, 0.00285171, 0.00272232],
                [1.0, 1.0, 1.0, 1.0],
            ]
        )
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk1990_blk2010,
            source_year=_90,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_1990,
            supp_source_table=supplement_data_path_90,
            input_var=input_vars_1990,
            weight_var=input_var_tags,
        )
        ix1, ix2 = 13, 17
        id_cols = ["bgp1990gj", "tr2010gj", "tr2010ge"]
        obs_str_vals = obs_xwalk.xwalk[id_cols][ix1:ix2].values
        wgt_cols = ["wt_pop", "wt_fam", "wt_hh", "wt_hu"]
        obs_num_vals = obs_xwalk.xwalk[wgt_cols][ix1:ix2].values
        numpy.testing.assert_equal(knw_str_vals, obs_str_vals)
        numpy.testing.assert_allclose(knw_num_vals, obs_num_vals, atol=6)

    def test_xwalk_state_bgp1990_tr2010(self,):
        knw_str_vals = numpy.array(
            [
                [
                    "G100001090444999990421009999999219012",
                    "G1000010042100",
                    "10001042100",
                ],
                [
                    "G100001090444999990421009999999999921",
                    "G1000010042100",
                    "10001042100",
                ],
                [
                    "G100001090444999990421009999999999921",
                    "G1000010042201",
                    "10001042201",
                ],
                [
                    "G100001090444999990421009999999999922",
                    "G1000010042100",
                    "10001042100",
                ],
            ]
        )
        knw_num_vals = numpy.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.99766436, 0.99716625, 0.99714829, 0.99727768],
                [0.00233564, 0.00283375, 0.00285171, 0.00272232],
                [1.0, 1.0, 1.0, 1.0],
            ]
        )
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk1990_blk2010,
            source_year=_90,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_1990,
            supp_source_table=supplement_data_path_90,
            input_var=input_vars_1990,
            weight_var=input_var_tags,
            stfips=stfips,
            vectorized=False,
            keep_base=False,
        )
        ix1, ix2 = 13, 17
        id_cols = ["bgp1990gj", "tr2010gj", "tr2010ge"]
        obs_str_vals = obs_xwalk.xwalk[id_cols][ix1:ix2].values
        wgt_cols = ["wt_pop", "wt_fam", "wt_hh", "wt_hu"]
        obs_num_vals = obs_xwalk.xwalk[wgt_cols][ix1:ix2].values
        numpy.testing.assert_equal(knw_str_vals, obs_str_vals)
        numpy.testing.assert_allclose(knw_num_vals, obs_num_vals, atol=6)

    def test_xwalk_bgp1990_tr2010_no_supp_error(self):
        with self.assertRaises(RuntimeError):
            obs_xwalk = nhgisxwalk.GeoCrossWalk(
                base_xwalk_blk1990_blk2010,
                source_year=_90,
                target_year=_10,
                source_geo=bgp,
                target_geo=tr,
                base_source_table=tab_data_path_1990,
                supp_source_table=None,
                input_var=input_vars_1990,
                weight_var=input_var_tags,
                stfips=stfips,
                vectorized=False,
                keep_base=False,
            )

    def test_xwalk_extract_state_bgp1990_tr2010(self):
        known_target_nan_xwalk = numpy.empty((0, 7))
        known_source_nan_xwalk = numpy.array(
            [[numpy.nan, "G1000050990000", "10005990000", 0.0, 0.0, 0.0, 0.0]],
            dtype=object,
        )
        known_target_nan_base = numpy.empty((0, 6))
        known_source_nan_base_shape = (149, 6)
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk1990_blk2010,
            source_year=_90,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_1990,
            supp_source_table=supplement_data_path_90,
            input_var=input_vars_1990,
            weight_var=input_var_tags,
            keep_base=True,
        )
        obs_target_nan_xwalk = nhgisxwalk.extract_state(
            obs_xwalk.xwalk, "nan", obs_xwalk.xwalk_name, obs_xwalk.target
        ).values
        numpy.testing.assert_array_equal(known_target_nan_xwalk, obs_target_nan_xwalk)
        obs_source_nan_xwalk = nhgisxwalk.extract_state(
            obs_xwalk.xwalk, "nan", obs_xwalk.xwalk_name, obs_xwalk.source
        ).values
        numpy.testing.assert_array_equal(
            known_source_nan_xwalk[0, 0], obs_source_nan_xwalk[0, 0]
        )
        numpy.testing.assert_array_equal(
            known_source_nan_xwalk[0, 1:3], obs_source_nan_xwalk[0, 1:3]
        )
        obs_target_nan_base = nhgisxwalk.extract_state(
            obs_xwalk.base, "nan", obs_xwalk.xwalk_name, obs_xwalk.base_target_col
        ).values
        numpy.testing.assert_array_equal(known_target_nan_base, obs_target_nan_base)
        obs_source_nan_base = nhgisxwalk.extract_state(
            obs_xwalk.base, "nan", obs_xwalk.xwalk_name, obs_xwalk.base_source_col
        ).values
        self.assertEqual(known_source_nan_base_shape, obs_source_nan_base.shape)

    def test_xwalk_extract_state_failure_bgp1990_tr2010(self):
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk1990_blk2010,
            source_year=_90,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_1990,
            supp_source_table=supplement_data_path_90,
            input_var=input_vars_1990,
            weight_var=input_var_tags,
            keep_base=True,
            stfips=stfips,
        )
        with self.assertRaises(RuntimeError):
            obs_target_nan_xwalk = nhgisxwalk.extract_state(
                obs_xwalk.xwalk, "nan", obs_xwalk.xwalk_name, obs_xwalk.target
            )
        with self.assertRaises(RuntimeError):
            obs_source_nan_xwalk = nhgisxwalk.extract_state(
                obs_xwalk.xwalk, "nan", obs_xwalk.xwalk_name, obs_xwalk.source
            )
        with self.assertRaises(RuntimeError):
            obs_target_nan_base = nhgisxwalk.extract_state(
                obs_xwalk.base, "nan", obs_xwalk.xwalk_name, obs_xwalk.base_target_col
            )
        with self.assertRaises(RuntimeError):
            obs_source_nan_base = nhgisxwalk.extract_state(
                obs_xwalk.base, "nan", obs_xwalk.xwalk_name, obs_xwalk.base_source_col
            )

    def test_xwalk_extract_unique_stfips_cls_bgp1990_tr2010(self):
        known_target_fips = set(["10"])
        known_source_fips = set(["10", "34", "nan"])
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk1990_blk2010,
            source_year=_90,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_1990,
            supp_source_table=supplement_data_path_90,
            input_var=input_vars_1990,
            weight_var=input_var_tags,
            keep_base=False,
            stfips=stfips,
        )
        obs_target_fips = nhgisxwalk.extract_unique_stfips(
            cls=obs_xwalk, endpoint="target"
        )
        self.assertEqual(known_target_fips, obs_target_fips)
        obs_source_fips = nhgisxwalk.extract_unique_stfips(
            cls=obs_xwalk, endpoint="source"
        )
        self.assertEqual(known_source_fips, obs_source_fips)

    def test_xwalk_extract_unique_stfips_df_bgp1990_tr2010(self):
        known_target_fips = set(["10"])
        known_source_fips = set(["10", "34", "nan"])
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk1990_blk2010,
            source_year=_90,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_1990,
            supp_source_table=supplement_data_path_90,
            input_var=input_vars_1990,
            weight_var=input_var_tags,
            keep_base=False,
            stfips=stfips,
        )
        obs_target_fips = nhgisxwalk.extract_unique_stfips(
            df=obs_xwalk.xwalk, endpoint="tr2010gj"
        )
        self.assertEqual(known_target_fips, obs_target_fips)
        obs_source_fips = nhgisxwalk.extract_unique_stfips(
            df=obs_xwalk.xwalk, endpoint="bgp1990gj"
        )
        self.assertEqual(known_source_fips, obs_source_fips)

    # 2000 bgp to 2010 tr through 2000 blk to 2010 blk
    def test_xwalk_full_bgp2000_tr2010_unrounded(self):
        knw_str_vals = numpy.array(
            [
                ["G10000509355299999051304R1", "G1000050051305", "10005051305"],
                ["G10000509355299999051304R1", "G1000050051306", "10005051306"],
                ["G10000509355299999051304R1", "G1000050051400", "10005051400"],
                ["G10000509355299999051304R2", "G1000050051305", "10005051305"],
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
            target_geo=tr,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            weights_precision=None,
        )
        ix1, ix2 = 1025, 1029
        id_cols = ["bgp2000gj", "tr2010gj", "tr2010ge"]
        obs_str_vals = obs_xwalk.xwalk[id_cols][ix1:ix2].values
        wgt_cols = ["wt_pop", "wt_fam", "wt_hh", "wt_hu"]
        obs_num_vals = obs_xwalk.xwalk[wgt_cols][ix1:ix2].values
        numpy.testing.assert_equal(knw_str_vals, obs_str_vals)
        numpy.testing.assert_allclose(knw_num_vals, obs_num_vals)

    def test_xwalk_state_bgp2000_tr2010_unrounded(self):
        knw_str_vals = numpy.array(
            [
                ["G10000509355299999051304R1", "G1000050051305", "10005051305"],
                ["G10000509355299999051304R1", "G1000050051306", "10005051306"],
                ["G10000509355299999051304R1", "G1000050051400", "10005051400"],
                ["G10000509355299999051304R2", "G1000050051305", "10005051305"],
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
            target_geo=tr,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            stfips=stfips,
            vectorized=False,
            keep_base=False,
            weights_precision=None,
        )
        ix1, ix2 = 1025, 1029
        id_cols = ["bgp2000gj", "tr2010gj", "tr2010ge"]
        obs_str_vals = obs_xwalk.xwalk[id_cols][ix1:ix2].values
        wgt_cols = ["wt_pop", "wt_fam", "wt_hh", "wt_hu"]
        obs_num_vals = obs_xwalk.xwalk[wgt_cols][ix1:ix2].values
        numpy.testing.assert_equal(knw_str_vals, obs_str_vals)
        numpy.testing.assert_allclose(knw_num_vals, obs_num_vals)

    def test_xwalk_extract_state_bgp2000_tr2010(self):
        known_target_nan_xwalk = numpy.empty((0, 7))
        known_source_nan_xwalk = numpy.empty((0, 7))
        known_target_nan_base = numpy.empty((0, 6))
        known_source_nan_base = numpy.empty((0, 6))
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            keep_base=True,
        )
        obs_target_nan_xwalk = nhgisxwalk.extract_state(
            obs_xwalk.xwalk, "nan", obs_xwalk.xwalk_name, obs_xwalk.target
        ).values
        numpy.testing.assert_array_equal(known_target_nan_xwalk, obs_target_nan_xwalk)
        obs_source_nan_xwalk = nhgisxwalk.extract_state(
            obs_xwalk.xwalk, "nan", obs_xwalk.xwalk_name, obs_xwalk.source
        ).values
        numpy.testing.assert_array_equal(known_source_nan_xwalk, obs_source_nan_xwalk)
        obs_target_nan_base = nhgisxwalk.extract_state(
            obs_xwalk.base, "nan", obs_xwalk.xwalk_name, obs_xwalk.base_target_col
        ).values
        numpy.testing.assert_array_equal(known_target_nan_base, obs_target_nan_base)
        obs_source_nan_base = nhgisxwalk.extract_state(
            obs_xwalk.base, "nan", obs_xwalk.xwalk_name, obs_xwalk.base_source_col
        ).values
        numpy.testing.assert_array_equal(known_source_nan_base, obs_source_nan_base)

    def test_xwalk_extract_state_failure_bgp2000_tr2010(self):
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            keep_base=True,
            stfips=stfips,
        )
        with self.assertRaises(RuntimeError):
            obs_target_nan_xwalk = nhgisxwalk.extract_state(
                obs_xwalk.xwalk, "nan", obs_xwalk.xwalk_name, obs_xwalk.target
            )
        with self.assertRaises(RuntimeError):
            obs_source_nan_xwalk = nhgisxwalk.extract_state(
                obs_xwalk.xwalk, "nan", obs_xwalk.xwalk_name, obs_xwalk.source
            )
        with self.assertRaises(RuntimeError):
            obs_target_nan_base = nhgisxwalk.extract_state(
                obs_xwalk.base, "nan", obs_xwalk.xwalk_name, obs_xwalk.base_target_col
            )
        with self.assertRaises(RuntimeError):
            obs_source_nan_base = nhgisxwalk.extract_state(
                obs_xwalk.base, "nan", obs_xwalk.xwalk_name, obs_xwalk.base_source_col
            )

    def test_xwalk_extract_unique_stfips_cls_bgp2000_tr2010(self):
        known_target_fips = set(["10"])
        known_source_fips = set(["10", "34"])
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            keep_base=False,
            stfips=stfips,
        )
        obs_target_fips = nhgisxwalk.extract_unique_stfips(
            cls=obs_xwalk, endpoint="target"
        )
        self.assertEqual(known_target_fips, obs_target_fips)
        obs_source_fips = nhgisxwalk.extract_unique_stfips(
            cls=obs_xwalk, endpoint="source"
        )
        self.assertEqual(known_source_fips, obs_source_fips)

    def test_xwalk_extract_unique_stfips_df_bgp2000_tr2010(self):
        known_target_fips = set(["10"])
        known_source_fips = set(["10", "34"])
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            keep_base=False,
            stfips=stfips,
        )
        obs_target_fips = nhgisxwalk.extract_unique_stfips(
            df=obs_xwalk.xwalk, endpoint="tr2010gj"
        )
        self.assertEqual(known_target_fips, obs_target_fips)
        obs_source_fips = nhgisxwalk.extract_unique_stfips(
            df=obs_xwalk.xwalk, endpoint="bgp2000gj"
        )
        self.assertEqual(known_source_fips, obs_source_fips)

    # 1990 bgp to 2010 bg through 2000 blk to 2010 blk
    def test_xwalk_full_bgp2000_bg2010(self):
        knw_str_vals = numpy.array(
            [
                [
                    "G100001090444999990421009999999219012",
                    "G10000100421002",
                    "100010421002",
                ],
                [
                    "G100001090444999990421009999999999921",
                    "G10000100421001",
                    "100010421001",
                ],
                [
                    "G100001090444999990421009999999999921",
                    "G10000100422013",
                    "100010422013",
                ],
                [
                    "G100001090444999990421009999999999922",
                    "G10000100421002",
                    "100010421002",
                ],
            ]
        )
        knw_num_vals = numpy.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.99766436, 0.99716625, 0.99714829, 0.99727768],
                [0.00233564, 0.00283375, 0.00285171, 0.00272232],
                [1.0, 1.0, 1.0, 1.0],
            ]
        )
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk1990_blk2010,
            source_year=_90,
            target_year=_10,
            source_geo=bgp,
            target_geo=bg,
            base_source_table=tab_data_path_1990,
            supp_source_table=supplement_data_path_90,
            input_var=input_vars_1990,
            weight_var=input_var_tags,
        )
        ix1, ix2 = 13, 17
        id_cols = ["bgp1990gj", "bg2010gj", "bg2010ge"]
        obs_str_vals = obs_xwalk.xwalk[id_cols][ix1:ix2].values
        wgt_cols = ["wt_pop", "wt_fam", "wt_hh", "wt_hu"]
        obs_num_vals = obs_xwalk.xwalk[wgt_cols][ix1:ix2].values
        numpy.testing.assert_equal(knw_str_vals, obs_str_vals)
        numpy.testing.assert_allclose(knw_num_vals, obs_num_vals, atol=6)

    def test_xwalk_state_bgp2000_bg2010(self):
        knw_str_vals = numpy.array(
            [
                [
                    "G100001090444999990421009999999219012",
                    "G10000100421002",
                    "100010421002",
                ],
                [
                    "G100001090444999990421009999999999921",
                    "G10000100421001",
                    "100010421001",
                ],
                [
                    "G100001090444999990421009999999999921",
                    "G10000100422013",
                    "100010422013",
                ],
                [
                    "G100001090444999990421009999999999922",
                    "G10000100421002",
                    "100010421002",
                ],
            ]
        )
        knw_num_vals = numpy.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.99766436, 0.99716625, 0.99714829, 0.99727768],
                [0.00233564, 0.00283375, 0.00285171, 0.00272232],
                [1.0, 1.0, 1.0, 1.0],
            ]
        )
        obs_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk1990_blk2010,
            source_year=_90,
            target_year=_10,
            source_geo=bgp,
            target_geo=bg,
            base_source_table=tab_data_path_1990,
            supp_source_table=supplement_data_path_90,
            input_var=input_vars_1990,
            weight_var=input_var_tags,
            stfips=stfips,
        )
        ix1, ix2 = 13, 17
        id_cols = ["bgp1990gj", "bg2010gj", "bg2010ge"]
        obs_str_vals = obs_xwalk.xwalk[id_cols][ix1:ix2].values
        wgt_cols = ["wt_pop", "wt_fam", "wt_hh", "wt_hu"]
        obs_num_vals = obs_xwalk.xwalk[wgt_cols][ix1:ix2].values
        numpy.testing.assert_equal(knw_str_vals, obs_str_vals)
        numpy.testing.assert_allclose(knw_num_vals, obs_num_vals, atol=6)

    # non-year, geography specific ---------------------------------------------
    def test_xwalk_write_read_csv_from_class(self):
        write_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            keep_base=False,
            stfips=stfips,
        )
        nhgisxwalk.xwalk_df_to_csv(cls=write_xwalk)
        read_xwalk = nhgisxwalk.xwalk_df_from_csv(write_xwalk.xwalk_name)
        known_values = write_xwalk.xwalk["wt_pop"].values
        observed_values = read_xwalk["wt_pop"].values
        numpy.testing.assert_allclose(known_values, observed_values)

    def test_xwalk_write_read_csv_from_df(self):
        write_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            keep_base=False,
            stfips=stfips,
        )
        nhgisxwalk.xwalk_df_to_csv(
            dfkwds={
                "df": write_xwalk.xwalk,
                "stfips": stfips,
                "xwalk_name": write_xwalk.xwalk_name,
            }
        )
        read_xwalk = nhgisxwalk.xwalk_df_from_csv(write_xwalk.xwalk_name)
        known_values = write_xwalk.xwalk["wt_pop"].values
        observed_values = read_xwalk["wt_pop"].values
        numpy.testing.assert_allclose(known_values, observed_values)

    def test_xwalk_write_read_csv_from_df_no_stfips(self):
        write_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
            base_source_table=tab_data_path_2000,
            input_var=input_vars_2000_SF1b,
            weight_var=input_var_tags,
            keep_base=False,
            stfips=stfips,
        )
        nhgisxwalk.xwalk_df_to_csv(
            dfkwds={"df": write_xwalk.xwalk, "xwalk_name": write_xwalk.xwalk_name}
        )
        read_xwalk = nhgisxwalk.xwalk_df_from_csv(write_xwalk.xwalk_name)
        known_values = write_xwalk.xwalk["wt_pop"].values
        observed_values = read_xwalk["wt_pop"].values
        numpy.testing.assert_allclose(known_values, observed_values)

    def test_xwalk_write_read_pickle(self):
        write_xwalk = nhgisxwalk.GeoCrossWalk(
            base_xwalk_blk2000_blk2010,
            source_year=_00,
            target_year=_10,
            source_geo=bgp,
            target_geo=tr,
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
                target_geo=tr,
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
                target_geo=tr,
                base_source_table=tab_data_path_1990,
                input_var=input_vars_1990,
                weight_var=input_var_tags,
            )

    def test_xwalk_source_code_bg(self):
        # testing for triggered errors
        with self.assertRaises(AttributeError):
            observed_xwalk = nhgisxwalk.GeoCrossWalk(
                base_xwalk_blk1990_blk2010,
                source_year=_90,
                target_year=_10,
                source_geo=bg,
                target_geo=tr,
                base_source_table=tab_data_path_1990,
                input_var=input_vars_1990,
                weight_var=input_var_tags,
            )

    def test_xwalk_source_code_tr(self):
        # testing for triggered errors
        with self.assertRaises(AttributeError):
            observed_xwalk = nhgisxwalk.GeoCrossWalk(
                base_xwalk_blk1990_blk2010,
                source_year=_90,
                target_year=_10,
                source_geo=tr,
                target_geo=tr,
                base_source_table=tab_data_path_1990,
                input_var=input_vars_1990,
                weight_var=input_var_tags,
            )

    def test_xwalk_source_code_co(self):
        # testing for triggered errors
        with self.assertRaises(AttributeError):
            observed_xwalk = nhgisxwalk.GeoCrossWalk(
                base_xwalk_blk1990_blk2010,
                source_year=_90,
                target_year=_10,
                source_geo=co,
                target_geo=tr,
                base_source_table=tab_data_path_1990,
                input_var=input_vars_1990,
                weight_var=input_var_tags,
            )


class Test_upper_level_functions(unittest.TestCase):
    def setUp(self):
        self.example_df = nhgisxwalk.example_crosswalk_data()

    def test_prepare_data_product(self):
        """
        """

        pass

    def test_generate_data_product(self):
        """
        """

        pass

    def test_regenerate_blk_blk_xwalk(self):
        """
        """

        pass

    def test_split_blk_blk_xwalk(self):
        known_ids = numpy.array(
            [
                "G10000100401001000",
                "G10000100401001001",
                "G10000100401001002",
                "G10000100401001003",
                "G10000100401001003",
            ]
        )
        xwalk_name = "nhgis_%s%s_%s%s_%s" % (blk, _90, blk, _10, gj)
        xwalk_path = data_dir + xwalk_name + "_state"
        # ensure directory exists
        if not os.path.exists(xwalk_path):
            os.mkdir(xwalk_path)
        sorter = nhgisxwalk.SORT_BYS[xwalk_name]
        nhgisxwalk.split_blk_blk_xwalk(
            base_xwalk_blk1990_blk2010,
            "GJOIN2010",
            xwalk_name,
            gj,
            fpath=xwalk_path,
            sort_by=sorter,
        )

        # read in the crosswalk
        gjoin = "GJOIN%s"
        gj_src, gj_trg = gjoin % _90, gjoin % _10
        data_types = nhgisxwalk.str_types([gj_src, gj_trg])
        from_csv_kws = {
            "path": xwalk_path + "/",
            "archived": True,
            "remove_unpacked": True,
        }
        read_csv_kws = {"dtype": data_types}
        read_xwalk = nhgisxwalk.xwalk_df_from_csv(
            xwalk_name + "_%s" % stfips, **from_csv_kws, **read_csv_kws
        )

        observed_ids = read_xwalk["GJOIN2010"].head().values
        numpy.testing.assert_array_equal(known_ids, observed_ids)

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
            groupby_cols=["bgp1990", "tr2010"],
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
            groupby_cols=["bgp1990", "tr2010"],
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
            groupby_cols=["bgp1990", "tr2010"],
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
            groupby_cols=["bgp1990", "tr2010"],
        )
        k1, o1 = known[:, :2], observed.values[:, :2]
        numpy.testing.assert_array_equal(k1, o1)
        k2, o2 = known[:, 2:].astype(float), observed.values[:, 2:].astype(float)
        numpy.testing.assert_allclose(k2, o2, atol=4)

    def test_round_weights(self):
        known = numpy.array(
            [
                ["A", "X", 0.56, 0.57],
                ["A", "Y", 0.44, 0.43],
                ["B", "X", 0.38, 0.4],
                ["B", "Y", 0.62, 0.6],
            ]
        )
        observed = nhgisxwalk.calculate_atoms(
            self.example_df,
            weight="wt",
            input_var=["pop_1990", "hh_1990"],
            weight_var=["pop", "hh"],
            source_id="bgp1990",
            groupby_cols=["bgp1990", "tr2010"],
        )
        observed = nhgisxwalk.round_weights(observed, decimals=2)
        k1, o1 = known[:, :2], observed.values[:, :2]
        numpy.testing.assert_array_equal(k1, o1)
        k2, o2 = known[:, 2:].astype(float), observed.values[:, 2:].astype(float)
        numpy.testing.assert_allclose(k2, o2, atol=4)

    def test__state(self):
        from nhgisxwalk.geocrosswalk import _state

        known = "99"
        observed = _state("99000001", code="ge")
        self.assertEqual(known, observed)

    def test_str_types(self):
        known = {"test_name_1": str, "test_name_2": str}
        observed = nhgisxwalk.str_types(["test_name_1", "test_name_2"])
        self.assertEqual(known, observed)

    def test_valid_geo_shorthand(self):
        known_sn = {
            blk: "block",
            bgp: "block group part",
            bg: "block group",
            tr: "tract",
            co: "county",
        }
        observed_sn = nhgisxwalk.valid_geo_shorthand(shorthand_name=True)
        self.assertEqual(known_sn, observed_sn)

        known_ns = {
            "block": blk,
            "block group part": bgp,
            "block group": bg,
            "tract": tr,
            "county": co,
        }
        observed_ns = nhgisxwalk.valid_geo_shorthand(shorthand_name=False)
        self.assertEqual(known_ns, observed_ns)


class Test_id_codes_functions(unittest.TestCase):
    def test_generate_geoid_nan(self):
        known_value = numpy.nan
        observed_value = nhgisxwalk.id_codes.generate_geoid(numpy.nan)
        self.assertEqual(numpy.isnan(known_value), numpy.isnan(observed_value))

    def test_generate_geoid_digit_int_str(self):
        with self.assertRaises(TypeError):
            nhgisxwalk.id_codes.generate_geoid("1")

    def test_generate_geoid_digit_int(self):
        with self.assertRaises(TypeError):
            nhgisxwalk.id_codes.generate_geoid(1)

    def test_generate_geoid_digit_float_str(self):
        with self.assertRaises(TypeError):
            nhgisxwalk.id_codes.generate_geoid("1.1")

    def test_generate_geoid_digit_float(self):
        with self.assertRaises(TypeError):
            nhgisxwalk.id_codes.generate_geoid(1.1)

    def test_generate_geoid_digit_unkown_float_str(self):
        with self.assertRaises(ValueError):
            nhgisxwalk.id_codes.generate_geoid("1.1.1")

    def test_generate_geoid_bad_char_int(self):
        with self.assertRaises(ValueError):
            nhgisxwalk.id_codes.generate_geoid("X1")

    def test_generate_geoid_bad_char_float(self):
        with self.assertRaises(ValueError):
            nhgisxwalk.id_codes.generate_geoid("X1.1")

    def test_tr_gj_no_G(self):
        with self.assertRaises(ValueError):
            nhgisxwalk.id_codes.tr_gj("2010", "X1.1")

    def test_tr_gj_bad_year(self):
        with self.assertRaises(ValueError):
            nhgisxwalk.id_codes.tr_gj("0000", "G123456789123456789")

    def test_co_gj(self):
        known_value = "G1000010"
        observed_value = nhgisxwalk.id_codes.co_gj("2010", "G1000010999999999")
        self.assertEqual(known_value, observed_value)

    def test_co_gj_no_G(self):
        with self.assertRaises(ValueError):
            nhgisxwalk.id_codes.tr_gj("2010", "X1.1")

    def test_co_gj_bad_year(self):
        with self.assertRaises(ValueError):
            nhgisxwalk.id_codes.tr_gj("0000", "G123456789123456789")


class Test_remove_generated_data(unittest.TestCase):
    def test_remove_generated_data(self):
        # remove 2000-2010 written test data
        xwalk_name = "nhgis_%s%s_%s%s_%s" % (bgp, _00, tr, _10, stfips)
        os.remove(xwalk_name + "." + CSV)
        os.remove(xwalk_name + "." + PKL)

        # remove state data
        xwalk_name = "nhgis_%s%s_%s%s_%s" % (blk, _90, blk, _10, gj)
        xwalk_path = data_dir + xwalk_name + "_state"
        shutil.rmtree(xwalk_path)


if __name__ == "__main__":
    unittest.main()
