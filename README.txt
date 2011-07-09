Introduction
============

By default all content types in Plone are indexed. Indexing is expensive
so indexing everything all the time can be very bad for the performance
of you application, especially if you have a number of auxilliary
content types that don't require indexing.

upfront.catalogblacklist gives you back control of what is being indexed
and uses a Generice Setup profile for configuration. An example
configuration might look like this:

    <?xml version="1.0"?>
    <blacklist>
        <type name="Document">
            <index name="object_provides" />
            <index name="Description" />
        </type>
        <type name="Folder">
            <index name="object_provides" />
        </type>
        <type name="Event">
            <index name="*" />
        </type>
        <interface name="Products.ATContentTypes.interfaces.IATFolder">
            <index name="object_provides" />
        </interface>
    </blacklist>

Note that you can blacklist by portal_type and by interface.

Usage
=====

Create a generic setup profile with a file named catalogblacklist.xml.
Use the format in the example above to blacklist indexes per portal_type
or interface.
