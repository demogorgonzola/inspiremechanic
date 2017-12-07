# BDD for other systems:
#   want: have a reference to game-logic entities
#   want: interact with other systems subsets
#   want: store info that is important to this system
#   want:

import unittest
import math
import random
from src.util import SubsetBase

# s = self
# test naming convention: test_<methodname>_<aspect>
class TestSubsetEntityDatabse(unittest.TestCase):
    def setUp(s):
        superset_path = 'tests/test-superset.pdl'
        subset_path = 'tests/test-subset.pdl'
        osubset_path = 'tests/test-osubset.pdl'

        superset = SubsetBase(superset_path)
        subset = SubsetBase(subset_path)
        osubset = SubsetBase(osubset_path)

        superset.create('super1','super2',mode='override')
        subset.create('val1','val2',superset=superset,mode='override')
        osubset.create('oval1','oval2',superset=superset,mode='override')

        s.superset = superset
        s.subset = subset
        s.osubset = osubset

    def tearDown(s):
        s.superset.delete(s.superset)
        s.subset.delete(s.subset)
        s.osubset.delete(s.osubset)

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

    def test_GetItem_usesRef(s):
        super_entry1 = s.superset.insert()
        super_entry2 = s.superset.insert()
        entry1 = s.subset.insert(super_entry2)
        entry2 = s.subset.insert(super_entry1)

        expected_super_entry1 = super_entry1
        expected_entry1 = entry1
        expected_entry2 = entry2

        result_super_entry1 = s.superset[super_entry1]
        result_entry1 = s.subset[entry1]
        result_entry2 = s.subset[entry2]

        s.assertEqual(expected_super_entry1,result_super_entry1['ref'])
        s.assertEqual(expected_entry1,result_entry1['ref'])
        s.assertEqual(expected_entry2,result_entry2['ref'])

    def test_AuxData_inserted(s):
        r_id1 = s.superset.insert()
        r_id2 = s.superset.insert()
        s.subset.insert(r_id2,'hello','world')
        s.subset.insert(ref=r_id1,val1='goodbye',val2='hell')

        expected_hello = r_id2
        expected_hell = r_id1

        result_hello = next(iter(s.subset(val1='hello')))['ref']
        result_hell = next(iter(s.subset(val2='hell')))['ref']

        s.assertIs(expected_hello,result_hello)
        s.assertIs(expected_hell,result_hell)




if __name__ == '__main__':
    unittest.main()
