# django-factory

## Don't use this
I wrote this years ago to solve a polymorphism problem that wasn't really collectively solved by the wider django community yet.  This has long since changed however, so instead I recommend that you check out the excellent [django-polymorphic](https://github.com/chrisglass/django_polymorphic/) which appears to be the (well maintained) reigning champion in this sphere.

--

Sometimes basic model inheritance isn't enough.  Sometimes you want to do fun
stuff like fetch an object based on an id... without knowing the subclass for
that object.  That's what this does.  An example will probably help explain.


    # models.py

    class Product(Factory):

        name = models.CharField(max_length=128)

        def __unicode__(self):
            return self.name



    class Toy(Product):

        minimum_age = models.PositiveIntegerField()

        def __unicode__(self):
            return "%s:%d" % (self.name, self.minimum_age)



    class Cigar(Product):

        origin = models.ForeignKey(Country)

        def __unicode__(self):
            return "%s:%d" % (self.name, self.origin.name)




    # views.py

    def myview(request, id=None):

        Toy.objects.create(name="My Toy", minimum_age=7)
        Cigar.objects.create(name="Cubans", origin=Country.objects.get(slug="cuba"))

        Product.objects.get(pk=1)
        # <Product: "My Toy">

        Product.objects.acquire(pk=1)
        # <Toy: "My Toy:7">

        Product.objects.acquire(pk=2)
        # <Cigar: "Cubans:Cuba">

        products = Product.objects.all() # A list of product objects
        [<Product: "My Toy">, <Product: "Cubans">]

        products[1].get_meta()
        <Cigar: "Cubans:Cuba">


This sort of thing is handy when you want to attach additional properties to
different model classes, but want them all to be treated the same without
having to do complex detection.

An example of this might be a product checkout, where you would want to
allow a user to buy any number of products and don't much care what kind of
products they are, or a REST server where a user requests info on product X
without knowing its subclass.  This way, you can process all products as a
group with the checkout, but return specific extraneous data with the REST
call.
