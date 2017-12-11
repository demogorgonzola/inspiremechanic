from pydblite import Base

## Issue 11: SubsetBase

#   should act like a database, with added functions
#   speciality:
#       adds info only about exisitng entitys
#   added functions:
#       check if entity exists
#       find intersection of two subsets

#   allow superset(ESDB) to reflect deletion of entity

# speciality database, works off exising database
# new field: eid = entity id, this is an id reflected from the local edb

class SubsetBase(Base):
    REF = 'ref'


    def create(self,*fields,**kw):
        self.superset = kw['superset'] if 'superset' in kw else None
        super(SubsetBase,self).create(SubsetBase.REF,*fields,**kw)
        super(SubsetBase,self).create_index(SubsetBase.REF)
        return self


    def insert(self,*args,**kw):
        if self.superset:
            if SubsetBase.REF not in kw and len(args) <= 0:
                raise ValueError('Ref not included for subset')
            else:
                ref_id = kw[SubsetBase.REF] if SubsetBase.REF in kw else args[0]
                if ref_id not in self.superset:
                    raise ValueError('Id does not exist in the Superset')
                elif ref_id in self:
                    raise ValueError('Cannot insert duplicates in subset')
        else:
            if SubsetBase.REF in kw:
                raise ValueError('Ref not included for non-subset')

        if self.superset:
            ref_id = kw[SubsetBase.REF] if SubsetBase.REF in kw else args[0]
            super(SubsetBase,self).insert(*args,**kw)
            return ref_id
        else:
            return super(SubsetBase,self).insert(self.next_id,*args,**kw)


    def update(self,records,**kw):
        if SubsetBase.REF in kw:
            raise ValueError('Ref cannot be modified')
        return super(SubsetBase,self).update(records,**kw)


    def __getitem__(self,key):
        record = self.indices[SubsetBase.REF][key][0]
        return super(SubsetBase,self).__getitem__(record)


    def __contains__(self,ref_id):
        return ref_id in self.indices[SubsetBase.REF]


    # aux functions
    def intersection(self,other):
        intersect = []
        for ref in [ r[SubsetBase.REF] for r in self ]:
            if ref in other: #extensibility issue, self ref
                intersect.append(ref)
        return set(intersect)


    # bug fixes
    def __call__(self, *args, **kw):
        """
        Selection by field values

        db(key=value) returns the list of records where r[key] = value

        Args:
            - args (list): A field to filter on.
            - kw (dict): pairs of field and value to filter on.

        Returns:
            - When args supplied, return a Filter object that filters on
            the specified field.
            - When kw supplied, return all the records where field values matches the
            key/values in kw.
        """

        if args and kw:
            raise SyntaxError("Can't specify positional AND keyword arguments")

        if args:
            if len(args) > 1:
                raise SyntaxError("Only one field can be specified")
            elif (type(args[0]) is PyDbExpressionGroup or type(args[0]) is PyDbFilter):
                return args[0].apply_filter(self.records)
            elif args[0] not in self.fields:
                raise ValueError("%s is not a field" % args[0])
            else:
                return PyDbFilter(self, args[0])
        if not kw:
            return self.records.values()  # db() returns all the values

        # indices and non-indices
        keys = kw.keys()
        ixs = set(keys) & set(self.indices.keys())
        no_ix = set(keys) - ixs
        if ixs:
            # fast selection on indices
            ix = ixs.pop()
            res = set(self.indices[ix].get(kw[ix], []))
            if not res:
                return []
            while ixs:
                ix = ixs.pop()
                res = res & set(self.indices[ix].get(kw[ix], []))
        else:
            # if no index, initialize result with test on first field
            field = no_ix.pop()
            res = set([r["__id__"] for r in self if r[field] == kw[field]])
        # selection on non-index fields
        for field in no_ix:
            res = res & set([_id for _id in res if self.records[_id][field] == kw[field]])
        return [self.records[_id] for _id in res]
