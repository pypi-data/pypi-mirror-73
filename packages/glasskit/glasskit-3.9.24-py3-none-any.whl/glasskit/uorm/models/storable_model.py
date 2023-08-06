import logging
from functools import partial
from time import time
from .base_model import BaseModel
from ..db import db
from ..utils import save_required, resolve_id, ObjectId
from ..errors import ModelDestroyed
from glasskit.errors import NotFound
from glasskit import ctx


class StorableModel(BaseModel):
    @property
    def _db(self):
        return db.meta

    def _save_to_db(self):
        self._db.save_obj(self)

    def update(self, data, skip_callback=False, invalidate_cache=True):
        for field in self.__fields__:
            if (
                field in data
                and field not in self.__rejected_fields__
                and field != "_id"
            ):
                self.__dict__[field] = data[field]
        self.save(skip_callback=skip_callback, invalidate_cache=invalidate_cache)

    @save_required
    def db_update(self, update, when=None, reload=True, invalidate_cache=True):
        """
                :param update: MongoDB update query
                :param when: filter query. No update will happen if it does not match
                :param reload: Load the new stat into the object (Caution: if you do not do this
                               the next save() will overwrite updated fields)
                :return: True if the document was updated. Otherwise - False
                """
        new_data = self._db.find_and_update_obj(self, update, when)
        if invalidate_cache and new_data:
            self.invalidate()

        if reload and new_data:
            tmp = self.__class__(new_data)
            self._reload_from_obj(tmp)

        return bool(new_data)

    def _delete_from_db(self):
        self._db.delete_obj(self)

    def _refetch_from_db(self):
        return self.find_one({"_id": self._id})

    def reload(self):
        if self.is_new:
            return
        tmp = self._refetch_from_db()
        if tmp is None:
            raise ModelDestroyed("model has been deleted from db")
        self._reload_from_obj(tmp)

    @classmethod
    # E.g. override if you want model to always return a subset of documents in its collection
    def _preprocess_query(cls, query):
        return query

    @classmethod
    def find(cls, query=None, **kwargs):
        if not query:
            query = {}
        return db.meta.get_objs(
            cls._ctor, cls.collection, cls._preprocess_query(query), **kwargs
        )

    @classmethod
    def aggregate(cls, pipeline, query=None, **kwargs):
        if not query:
            query = {}
        pipeline = [{"$match": cls._preprocess_query(query)}] + pipeline
        return db.meta.get_aggregated(cls.collection, pipeline, **kwargs)

    @classmethod
    def find_projected(cls, query=None, projection=("_id",), **kwargs):
        if not query:
            query = {}
        return db.meta.get_objs_projected(
            cls.collection,
            cls._preprocess_query(query),
            projection=projection,
            **kwargs,
        )

    @classmethod
    def find_one(cls, query, **kwargs):
        return db.meta.get_obj(
            cls._ctor, cls.collection, cls._preprocess_query(query), **kwargs
        )

    @classmethod
    def get(cls, expression, raise_if_none=None):
        if expression is None:
            return None

        expression = resolve_id(expression)
        if isinstance(expression, ObjectId):
            query = {"_id": expression}
        else:
            expression = str(expression)
            query = {cls.KEY_FIELD: expression}
        res = cls.find_one(query)
        if res is None and raise_if_none is not None:
            if isinstance(raise_if_none, Exception):
                raise raise_if_none
            else:
                raise NotFound(f"{cls.__name__} not found")
        return res

    @classmethod
    def destroy_all(cls):
        db.meta.delete_query(cls.collection, cls._preprocess_query({}))

    @classmethod
    def destroy_many(cls, query):
        # warning: being a faster method than traditional model manipulation,
        # this method doesn't provide any lifecycle callback for independent
        # objects
        db.meta.delete_query(cls.collection, cls._preprocess_query(query))

    @classmethod
    def update_many(cls, query, attrs):
        # warning: being a faster method than traditional model manipulation,
        # this method doesn't provide any lifecycle callback for independent
        # objects
        db.meta.update_query(cls.collection, cls._preprocess_query(query), attrs)

    @classmethod
    def cache_get(cls, expression, raise_if_none=None):
        if expression is None:
            return None
        cache_key = f"{cls.collection}.{expression}"
        getter = partial(cls.get, expression, raise_if_none)
        return cls._cache_get(cache_key, getter)

    @classmethod
    def _cache_get(cls, cache_key, getter, ctor=None):
        t1 = time()
        if not ctor:
            ctor = cls

        if db.l1c.has(cache_key):
            data = db.l1c.get(cache_key)
            td = time() - t1
            ctx.log.debug(
                "%s L1 hit %s %.3f secs", db.l1c.__class__.__name__, cache_key, td
            )
            return ctor(data)

        if db.l2c.has(cache_key):
            data = db.l2c.get(cache_key)
            db.l1c.set(cache_key, data)
            td = time() - t1
            ctx.log.debug(
                "%s L2 hit %s %.3f secs", db.l2c.__class__.__name__, cache_key, td
            )
            return ctor(data)

        obj = getter()
        if obj:
            data = obj.to_dict()
            db.l2c.set(cache_key, data)
            db.l1c.set(cache_key, data)

        td = time() - t1
        ctx.log.debug("%s miss %s %.3f secs", db.l2c.__class__.__name__, cache_key, td)
        return obj

    def invalidate(self):
        if self.USE_INITIAL_STATE:
            for field in self.__cache_key_fields__:
                value = self._initial_state.get(field)
                if value:
                    self._invalidate(f"{self.collection}.{value}")

    @staticmethod
    def _invalidate(cache_key):
        if db.l1c.delete(cache_key):
            ctx.log.debug("%s delete %s", db.l1c.__class__.__name__, cache_key)
        if db.l2c.delete(cache_key):
            ctx.log.debug("%s delete %s", db.l2c.__class__.__name__, cache_key)
