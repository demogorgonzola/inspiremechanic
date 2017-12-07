import unittest
import src.entitysystem as es

# s = self
class TestEntitySystem(unittest.TestCase):
    def setUp(s):
        s.db = es.db

    def tearDown(s):
        s.db.delete(r for r in s.db)

    def test_DBExists(s):
        s.assertIsNotNone(s.db)

    def test_NameFieldExists(s):
        s.db.add_field('mood',default='feels')
        s.assertIn('mood',s.db.fields)
        #chances 'unittest' is never a actual field name
        s.assertNotIn('unittest',s.db.fields)

    def test_InsertSingle(s):
        tname = 'hey'
        s.db.insert(name=tname)
        record = next(iter(s.db))
        print(record)
        s.assertIs(record['name'],tname)

    def test_InsertMany(s):
        tname1 = 'a' ; tname2 = 'b' ; tname3 = 'c'
        s._insertmany([tname1],[tname2],[tname3])
        s.assertEqual(len(s.db),3)

    def test_Delete(s):
        tname1 = 'a' ; tname2 = 'b' ; tname3 = 'c'
        s._insertmany([tname1],[tname2],[tname3])
        before_len = len(s.db)
        #delete 1
        s.db.delete(r for r in s.db('name').ilike('a'))
        after_len = len(s.db)
        s.assertLess(after_len,before_len)
        records = [ r['name'][0] for r in s.db('name') ]
        s.assertNotIn('a',records)
        s.assertIn('b',records)
        s.assertIn('c',records)




    def _insertmany(s,*many):
        for r in many:
            s.db.insert(r)




if __name__ == '__main__':
    unittest.main()
