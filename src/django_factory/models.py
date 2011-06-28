# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class FactoryManager(models.Manager):
    """
        Custom manager to handle object fetching for subclasses of Factory
    """

    def acquire(self, **kwa):

        where_selector, where_val = kwa.items()[0]

        from django.db import connection

        qn = connection.ops.quote_name

        if where_selector == "pk":
            where_selector = self.model._meta.pk.column

        query = """
            SELECT
                _factorypath
            FROM
                %(factory)s
            WHERE
                %(where_selector)s = %%s
        """ % {
            "where_selector": "%s.%s" % (self.model._meta.db_table, qn(where_selector)),
            "factory": qn(self.model._meta.db_table),
        }
        cursor = connection.cursor()
        cursor.execute(query, params=(where_val,))
        result = cursor.fetchone()
        if result:
            klass = self.model.get_factorypaths()[result[0]]
            return klass.objects.get(**kwa)

        return self.get(**kwa)



class Factory(models.Model):
    """
        Class factory abstract parent class.
        Subclass this to create your own factory
    """

    class Meta:
        abstract = True


    _paths = {} # Cache of paths to classes that subclass the parent factory

    _factorypath = models.CharField(max_length=255)

    objects = FactoryManager()

    def save(self, *a, **kwa):
        self._factorypath = self.get_factorypath()
        super(Factory, self).save(*a, **kwa)


    def get_meta(self):
        return self.__class__.objects.acquire(pk=self.pk)


    @classmethod
    def get_factorypath(cls):
        """
            Return the import path to this class.  We use this as the
            identifier for when the factory creates or acquires an instance of
            this class.
        """
        return cls.__module__ + "." + cls.__name__


    @classmethod
    def get_factorypaths(cls):
        """
            Return a list of all classes that subclass this factory.
        """

        if not cls._paths:
            cls._set_factorypaths()

        return cls._paths


    @classmethod
    def _set_factorypaths(cls):
        """
            Compiles a list of python paths to objects subclassed from this
            model which we then use to determine the model to instantiate for
            the data requested.
        """

        paths = {} # We don't use cls._paths because we recurse below
        for c in cls.__subclasses__():
            paths[c.get_factorypath()] = c

            # Recursion!
            if c.__subclasses__():
                paths.update(c.get_factorypaths())

        cls._paths = paths

