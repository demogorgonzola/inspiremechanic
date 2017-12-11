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
        superset_path = ':memory:'
        subset_path = ':memory:'
        other_path = ':memory:'
        subsubset_path = ':memory:'

        superset = SubsetBase(superset_path)
        subset = SubsetBase(subset_path)
        other = SubsetBase(other_path)
        subsubset = SubsetBase(subsubset_path)

        superset.create('f1','f2',mode='override')
        subset.create('f1','f2',superset=superset,mode='override')
        other.create('f1','f2',superset=superset,mode='override')
        subsubset.create('f1','f2',superset=subset,mode='override')

        s.superset = superset
        s.subset = subset
        s.other = other
        s.subsubset = subsubset


    def tearDown(s):
        s.superset.delete(s.superset)
        s.subset.delete(s.subset)
        s.other.delete(s.other)
        s.subsubset.delete(s.subsubset)


    # Method: __getitem__,[]
    def test_GetItem_usesRefNotId(s):
        #setup
        ref1 = s.superset.insert()
        ref2 = s.superset.insert()
        ref3 = s.superset.insert()
        subref1 = s.subset.insert(ref3)

        #expected
        expected_ref1 = ref1
        expected_subref1 = ref3

        #execute
        result_ref1 = s.superset[ref1]
        result_subref1 = s.subset[ref3]

        #extracted(optional)
        extracted_ref1 = result_ref1['ref']
        extracted_subref1 = result_subref1['ref']

        #assert
        s.assertEqual(expected_ref1,extracted_ref1)
        s.assertEqual(expected_subref1,extracted_subref1)
    #


    # Method: __contains__,in
    def test_Contains_usesRef(s):
        #setup
        ref1 = s.superset.insert()
        ref2 = s.superset.insert()
        ref3 = s.superset.insert()
        subref1 = s.subset.insert(ref3)

        #expected
        expected = ref3

        #assert
        s.assertIn(expected,s.subset)
    #


    # Method: Insert
    def test_Insert_validInsert(s):
        #setup
        ref = s.superset.insert()

        #expected/execute/assert
        s.subset.insert(ref)


    def test_Insert_invalidInsert(s):
        #setup
        ref = s.superset.insert()

        #expected/execute/assert
        with s.assertRaises(ValueError):
            s.subset.insert(ref-1)


    def test_Insert_duplicateInsert(s):
        #setup
        ref = s.superset.insert()
        s.subset.insert(ref)

        #expected/execute/assert
        with s.assertRaises(ValueError):
            s.subset.insert(ref)


    def test_Insert_returnsRefNotId(s):
        #setup
        ref1 = s.superset.insert()
        ref2 = s.superset.insert()

        #expected
        expected = ref2

        #execute
        result = s.subset.insert(ref2)

        #assert
        s.assertEqual(expected,result)
    #


    # Method: Update
    def test_Update_refDoesntUpdate(s):
        #setup
        r_id = s.superset.insert()
        s_r_id = s.subset.insert(r_id)

        #expected/execute/assert
        with s.assertRaises(ValueError):
            s.superset.update(r_id,ref=r_id+1)
        with s.assertRaises(ValueError):
            s.subset.update(s_r_id,ref=r_id+1)
    #


    # Method:Intersection
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
                s.other.insert(ref)


    def test_Intersection_subsetVsOsubset(s):
        #setup
        s.setUp_Intersection()
        subset_refs = [ r['ref'] for r in s.subset ]
        other_refs = [ r['ref'] for r in s.other ]

        #expected
        expected = set(subset_refs).intersection(other_refs)

        #execute
        result = s.subset.intersection(s.other)
        reverse = s.other.intersection(s.subset)

        #assert
        s.assertEqual(expected,result)
        s.assertEqual(expected,reverse)


    def test_Intersection_subsetVsSuperset(s):
        #setup
        s.setUp_Intersection()
        subset_refs = [ r['ref'] for r in s.subset ]

        #expected
        expected = set(subset_refs)

        #execute
        result = s.subset.intersection(s.superset)
        reverse = s.superset.intersection(s.subset)

        #assert
        s.assertEqual(expected,result)
        s.assertEqual(expected,reverse)
    #


    # Method: Insert, with Aux Data
    def test_AuxData_insertedSubset(s):
        #setup
        r_id1 = s.superset.insert()
        r_id2 = s.superset.insert()
        s.subset.insert(r_id2,'hello','world')
        s.subset.insert(ref=r_id1,f1='goodbye',f2='hell')

        #expected
        expected_hello = r_id2
        expected_hell = r_id1

        #execute
        result_hello = next(iter(s.subset(f1='hello')))['ref']
        result_hell = next(iter(s.subset(f2='hell')))['ref']

        #assert
        s.assertIs(expected_hello,result_hello)
        s.assertIs(expected_hell,result_hell)
    #



if __name__ == '__main__':
    unittest.main()
