from django.db import models
from django_factory.managers import FactoryManager

class Factory(models.Model):
	"""
		Class factory abstract parent class.
		Subclass this to create your own factory
	"""

	class Meta:
		abstract = True


	_paths = {} # Cache of paths to classes that subclass the parent factory

	_factorypath = models.CharField(max_length=255,db_index=True)

	objects = FactoryManager()

	def save(self, *a, **kwa):
		if not self._factorypath:
			self._factorypath = self.get_factorypath()
		super(Factory, self).save(*a, **kwa)


	def get_meta(self):
		"""
			Handy to run when you want to get all the properties of an object, not just its root information.
		"""
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

