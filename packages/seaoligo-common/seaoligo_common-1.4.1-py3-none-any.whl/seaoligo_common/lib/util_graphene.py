from graphene import AbstractType, Enum, Int
from flask import g


class Counts(AbstractType):
    total_count = Int()
    def resolve_total_count(root, info):
        return g.total_count

    filtered_count = Int()
    def resolve_filtered_count(root, info):
        return g.filtered_count


class OrganismSelect(Enum):
    HUMAN = 'human'
    MOUSE = 'mouse'
    RAT = 'rat'


class AssemblySelect(Enum):
    hg38 = 'hg38'
    mm10 = 'mm10'
    rn6 = 'rn6'
