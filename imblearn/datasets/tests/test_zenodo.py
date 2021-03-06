"""Test the datasets loader.

Skipped if datasets is not already downloaded to data_home.
"""
# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Christos Aridas
# License: MIT

from imblearn.datasets import fetch_datasets
from sklearn.utils.testing import (assert_equal, assert_allclose,
                                   assert_raises_regex, SkipTest)

DATASET_SHAPE = {'ecoli': (336, 7),
                 'optical_digits': (5620, 64),
                 'satimage': (6435, 36),
                 'pen_digits': (10992, 16),
                 'abalone': (4177, 10),
                 'sick_euthyroid': (3163, 42),
                 'spectrometer': (531, 93),
                 'car_eval_34': (1728, 21),
                 'isolet': (7797, 617),
                 'us_crime': (1994, 100),
                 'yeast_ml8': (2417, 103),
                 'scene': (2407, 294),
                 'libras_move': (360, 90),
                 'thyroid_sick': (3772, 52),
                 'coil_2000': (9822, 85),
                 'arrhythmia': (452, 278),
                 'solar_flare_m0': (1389, 32),
                 'oil': (937, 49),
                 'car_eval_4': (1728, 21),
                 'wine_quality': (4898, 11),
                 'letter_img': (20000, 16),
                 'yeast_me2': (1484, 8),
                 'webpage': (34780, 300),
                 'ozone_level': (2536, 72),
                 'mammography': (11183, 6),
                 'protein_homo': (145751, 74),
                 'abalone_19': (4177, 10)}


def fetch(*args, **kwargs):
    return fetch_datasets(*args, download_if_missing=True, **kwargs)


def test_fetch():
    try:
        datasets1 = fetch(shuffle=True, random_state=42)
    except IOError:
        raise SkipTest("Zenodo dataset can not be loaded.")

    datasets2 = fetch(shuffle=True, random_state=37)

    for k in DATASET_SHAPE.keys():

        X1, X2 = datasets1[k].data, datasets2[k].data
        assert_equal(DATASET_SHAPE[k], X1.shape)
        assert_equal(X1.shape, X2.shape)

        y1, y2 = datasets1[k].target, datasets2[k].target
        assert_equal((X1.shape[0],), y1.shape)
        assert_equal((X1.shape[0],), y2.shape)


def test_fetch_filter():
    try:
        datasets1 = fetch(filter_data=tuple([1]), shuffle=True,
                          random_state=42)
    except IOError:
        raise SkipTest("Zenodo dataset can not be loaded.")

    datasets2 = fetch(filter_data=tuple(['ecoli']), shuffle=True,
                      random_state=37)

    X1, X2 = datasets1['ecoli'].data, datasets2['ecoli'].data
    assert_equal(DATASET_SHAPE['ecoli'], X1.shape)
    assert_equal(X1.shape, X2.shape)

    assert_allclose(X1.sum(), X2.sum())

    y1, y2 = datasets1['ecoli'].target, datasets2['ecoli'].target
    assert_equal((X1.shape[0],), y1.shape)
    assert_equal((X1.shape[0],), y2.shape)


def test_fetch_error():
    assert_raises_regex(ValueError, 'is not a dataset available.',
                        fetch_datasets, filter_data=tuple(['rnd']))
    assert_raises_regex(ValueError, 'dataset with the ID=',
                        fetch_datasets, filter_data=tuple([-1]))
    assert_raises_regex(ValueError, 'dataset with the ID=',
                        fetch_datasets, filter_data=tuple([100]))
    assert_raises_regex(ValueError, 'value in the tuple',
                        fetch_datasets, filter_data=tuple([1.00]))
