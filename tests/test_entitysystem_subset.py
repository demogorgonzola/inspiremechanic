# BDD for other systems:
#   want: have a reference to game-logic entities
#   want: interact with other systems subsets
#   want: store info that is important to this system
#   want:

import unittest
import math
import random
import src.entitysystem as es

# s = self
# test naming convention: test_<methodname>_<aspect>
class TestSubsetEntityDatabse(unittest.TestCase):
    def setUp(s):
        superset_path = 'tests/test-superset.pdl'
        subset_path = 'tests/test-subset.pdl'
        osubset_path = 'tests/test-osubset.pdl'

        superset = es.Subset(superset_path)
        subset = es.Subset(subset_path)
        osubset = es.Subset(osubset_path)

        superset.create(mode='override')
        subset.create('val1','val2',superset=superset,mode='override')
        osubset.create('oval1','oval2',superset=superset,mode='override')

        s.superset = superset
        s.subset = subset
        s.osubset = osubset

    def tearDown(s):
        s.superset.delete(s.superset)
        s.subset.delete(s.subset)
        s.osubset.delete(s.osubset)
        s.superset = None
        s.subset = None
        s.osubset = None

    def test_Create_reffieldIncluded(s):
        s.assertIn('ref',s.subset.fields)

    def test_Create_supersetIncluded(s):
        s.assertIs(s.subset.superset,s.superset)

    def test_Insert_validInsert(s):
        r_id = s.superset.insert()
        s.subset.insert(r_id)

    def test_Insert_invalidInsert(s):
        r_id = s.superset.insert()
        with s.assertRaises(ValueError):
            s.subset.insert(r_id-1)

    def test_Insert_duplicateInsert(s):
        r_id = s.superset.insert()
        s.subset.insert(r_id)
        with s.assertRaises(ValueError):
            s.subset.insert(r_id)

    def test_Update_refDoesntUpdate(s):
        r_id = s.superset.insert()
        s_r_id = s.subset.insert(ref=r_id)
        with s.assertRaises(ValueError):
            s.superset.update(r_id,ref=r_id+1)
        with s.assertRaises(ValueError):
            s.subset.update(s_r_id,ref=r_id+1)

    def setUp_Intersection(s):
        n = 100
        intersection_percent = 0.2   # between 0 and 1
        thresh = math.ceil(n*(intersection_percent/2 + 0.5))
        start = n-thresh
        end = thresh
        for i in range(n):
            ref = s.superset.insert()
            if i <= end:
                s.subset.insert(ref)
            if start <= ref:
                s.osubset.insert(ref)

    def test_Intersection_subsetVsOsubset(s):
        s.setUp_Intersection()

        subset_refs = [ r['ref'] for r in s.subset ]
        osubset_refs = [ r['ref'] for r in s.osubset ]

        expected = set(subset_refs).intersection(osubset_refs)

        result = s.subset.intersection(s.osubset)
        reverse = s.osubset.intersection(s.subset)

        s.assertEqual(expected,result)
        s.assertEqual(expected,reverse)

    def test_Intersection_subsetVsSuperset(s):
        s.setUp_Intersection()

        subset_refs = [ r['ref'] for r in s.subset ]

        expected = set(subset_refs)

        result = s.subset.intersection(s.superset)
        reverse = s.superset.intersection(s.subset)

        s.assertEqual(expected,result)
        s.assertEqual(expected,reverse)


if __name__ == '__main__':
    unittest.main()
