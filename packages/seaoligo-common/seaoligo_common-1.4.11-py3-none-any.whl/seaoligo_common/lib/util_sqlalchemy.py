from datetime import datetime
from typing import Dict, Generic, List, Tuple, Union, TypeVar
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm.attributes import InstrumentedAttribute

from seaoligo_common.app import db


class ResourceMixin(object):
    # Keep track when records are created and updated.
    created_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), index=True, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, default=1)
    updated_by = db.Column(db.Integer)

    @classmethod
    def get_by_id(cls, id: Union[int, str, List[str]]) -> 'db.Model':
        try:
            return cls.query.get(id)
        except ValueError:
            return None

    @classmethod
    def get_all(cls) -> List['db.Model']:
        return cls.query.all()

    def save(self) -> 'db.Model':
        """
        Save a model instance.

        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self

    def update(self, update_obj) -> 'db.Model':
        """
        Update a model instance.

        :param update_obj: Model object containing updates
        :return: Model instance
        """
        updates = dict(x for x in update_obj.__dict__.items() if x[0] != '_sa_instance_state')
        for key, value in updates.items():
            setattr(self, key, value)
        self.save()

        return self

    def delete(self) -> None:
        """
        Delete a model instance.

        :return: db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()

    @classmethod
    def _bulk_insert(cls, data, label: str, dtype: str = '') -> None:
        """
        Bulk insert data to the model and log it. This is much more efficient than adding 1 row at a time in a loop.

        :param data: Data to be saved
        :type data: list
        :param dtype: Data type
        :type dtype: str
        :param label: Label for the output
        :type label: str
        :return: None
        """
        db.engine.execute(cls.__table__.insert(), data)
        print(f'Finished inserting {len(data):,} {(dtype + " ") if dtype else ""}{label}.')

        return None


def sort_query(model: db.Model, query: BaseQuery, sort_keys: Dict[str, InstrumentedAttribute],
               order_by: Tuple[str]) -> BaseQuery:
    """Sort list with order_by fields, append id_ASC/id_DESC if not present."""
    sort_list = [order.split('_') for order in order_by]
    query = query.order_by(*[sort_keys[sort_key].desc() if sort_order == 'DESC' else sort_keys[sort_key]
                             for (sort_key, sort_order) in sort_list if sort_key in sort_keys])
    if not ('id_ASC' in order_by or 'id_DESC' in order_by):
        query = query.order_by(model.id.desc() if sort_list[0][1] == 'DESC' else model.id)

    return query


T = TypeVar('T')


class RefseqMixin(Generic[T], object):
    @classmethod
    def find_by_refseq_id(cls, refseq_id: str) -> T:
        """
        Find a model by its RefSeq ID.
        """
        return cls.query.filter((cls.id == refseq_id) | (cls.acc == refseq_id)).first()
