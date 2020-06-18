import re
import unidecode

class Slugifier:
    def __init__(self, queryable, name):
        self.name = name
        self.slug = re.sub(r'[\W_]+', '-', unidecode.unidecode(self.name).lower())
        self.queryable = queryable
        self.queryable_klazz = type(self.queryable)
        self.sort = self.queryable_klazz.id.desc()
        self.clause = self.queryable_klazz.slug.ilike(self.slug + '%')

    def call(self):        
        row = self.queryable.query.filter(self.clause).order_by(self.sort).first()

        if row is None: return self.slug

        count = row.slug.split('-').pop()
        if count.isdigit(): return (self.slug + '-' + str(int(count) + 1))
        return (self.slug + '-1')
