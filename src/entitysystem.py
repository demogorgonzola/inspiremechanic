import pydblite

from pydblite import Base

_local_db = Base('inspire.pdl')  #The Local Entity Database
_local_db.create('name',mode='override')
#change .create() mode to 'open' after testing
# 'override' provides fresh dbs for testing

db = _local_db

## Issue 11: Subset

#   should act like a database, with added functions
#   speciality:
#       adds info only about exisitng entitys
#   added functions:
#       check if entity exists
#       find intersection of two subsets

#   allow superset(ESDB) to reflect deletion of entity

# speciality database, works off exising database
# new field: eid = entity id, this is an id reflected from the local edb
class Subset(Base):
    REF = 'ref'

    def create(self,*fields,**kw):
        self.superset = kw['superset'] if 'superset' in kw else None
        super(Subset,self).create(Subset.REF,*fields,**kw)
        super(Subset,self).create_index(Subset.REF)
        return self

    def insert(self,*args,**kw):
        ref_id = kw[Subset.REF] if Subset.REF in kw else args[0] if len(args) > 0 else None
        if (not self.superset) or (ref_id in self.superset and ref_id not in self):
            if self.superset:
                return super(Subset,self).insert(*args,**kw)
            else:
                r_id = super(Subset,self).insert(None,*args,**kw)
                super(Subset,self).update(self[r_id],ref=r_id)
                return r_id
        else:
            raise ValueError('Id does not exist in the Superset')

    def update(self,records,**kw):
        if Subset.REF in kw:
            raise ValueError('Ref cannot be modified')
        return super(Subset,self).update(records,**kw)

    #aux functions

    def intersection(self,other):
        intersect = []
        for ref in [ r[Subset.REF] for r in self ]:
            if other(ref=ref):
                intersect.append(ref)
        return set(intersect)



##
