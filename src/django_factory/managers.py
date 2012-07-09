from django.db import models

class FactoryManager(models.Manager):
    """
        Custom manager to handle object fetching for subclasses of Factory
    """

    def acquire(self, **kwa):
        return self._get_leaf_class(**kwa).objects.get(**kwa)


    def acquire_object_or_404(self, **kwa):
        from django.shortcuts import get_object_or_404
        return get_object_or_404(self._get_leaf_class(**kwa), **kwa)


    def _get_leaf_class(self, **kwa):
        """
            If the lookup in question belongs to a specific class, return that
            class, otherwise just return the class this manager is managing.
        """

        from django.db import connection

        where_selector, where_val = kwa.items()[0]

        root = self._get_root() # The top-level class from which all factory methods were spawned
        qn = connection.ops.quote_name

        if where_selector == "pk":
            where_selector = root.pk.column

        query = """
            SELECT
                _factorypath
            FROM
                %(factory)s
            WHERE
                %(where_selector)s = %%s
        """ % {
            "where_selector": "%s.%s" % (root.db_table, qn(where_selector)),
            "factory": qn(root.db_table),
        }

        cursor = connection.cursor()
        cursor.execute(query, (where_val,))
        result = cursor.fetchone()
        if result and self.model.get_factorypaths():
            return self.model.get_factorypaths()[result[0]]

        return self.model


    def _get_root(self):

        from django_factory.models import Factory

        t = self.model
        while Factory not in t.__bases__:
            t = t.__base__

        return t._meta
